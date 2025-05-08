import csv
import json
import os

import yaml
from pymongo import MongoClient


class MongoDBWrapper:
    def __init__(
        self,
        uri="mongodb://localhost:27017",
        database_name="default",
    ):
        self.client = MongoClient(uri)

        self.db = self.client[
            database_name
        ]

    def access_collection(
        self,
        collection_name,
    ):
        collection = self.db[
            collection_name
        ]

        return collection

    def insert_documents(
        self,
        collection_name,
        documents,
    ):
        collection = (
            self.access_collection(
                collection_name,
            )
        )

        if isinstance(documents, list):
            result = (
                collection.insert_many(
                    documents,
                )
            )
            return result.inserted_ids

        else:
            result = (
                collection.insert_one(
                    documents,
                )
            )
            return result.inserted_id

    def insert_documents_from_json(
        self,
        collection_name,
        json_file,
        encoding="utf-8",
    ):
        with open(
            json_file,
            encoding=encoding,
        ) as file:
            documents = json.load(file)

        result = self.insert_documents(
            collection_name,
            documents,
        )

        return result

    def upsert_documents_from_json(
        self,
        collection_name,
        json_file,
        primary_key_field="_id",
        encoding="utf-8",
    ):
        with open(
            json_file,
            encoding=encoding,
        ) as file:
            documents = json.load(file)

        result = self.upsert_documents(
            collection_name,
            documents,
            primary_key_field=primary_key_field,
        )

        return result

    def upsert_document(
        self,
        collection_name,
        document,
        primary_key_field,
    ):
        collection = (
            self.access_collection(
                collection_name,
            )
        )

        filter_query = {
            primary_key_field: document[
                primary_key_field
            ],
        }

        update_operation = {
            "$set": document,
        }

        result = collection.update_one(
            filter_query,
            update_operation,
            upsert=True,
        )

        upserted_id_or_match_count = (
            result.upserted_id
            if result.upserted_id
            else result.matched_count
        )

        return (
            upserted_id_or_match_count
        )

    def upsert_documents(
        self,
        collection_name,
        documents,
        primary_key_field,
    ):
        collection = (
            self.access_collection(
                collection_name,
            )
        )

        for document in documents:
            filter_query = {
                primary_key_field: document[
                    primary_key_field
                ],
            }

            update_operation = {
                "$set": document,
            }

            collection.update_one(
                filter_query,
                update_operation,
                upsert=True,
            )

        return True

    def find_documents(
        self,
        collection_name,
        query={},
    ):
        collection = (
            self.access_collection(
                collection_name,
            )
        )

        documents = list(
            collection.find(query),
        )

        return documents

    def export_documents_to_json(
        self,
        collection_name,
        query={},
        output_file="output.json",
    ):
        documents = self.find_documents(
            collection_name,
            query,
        )

        os.makedirs(
            os.path.dirname(
                output_file
            ),
            exist_ok=True,
        )

        with open(
            output_file,
            "w",
        ) as file:
            json.dump(
                documents,
                file,
                default=str,
                indent=4,
            )

        print(
            f"Exported {len(documents)} documents to {output_file}",
        )

    def run_aggregation(
        self,
        collection_name,
        pipeline,
    ):
        collection = (
            self.access_collection(
                collection_name,
            )
        )

        results = list(
            collection.aggregate(
                pipeline,
            ),
        )

        return results

    def _read_pipeline_from_json(
        self,
        file_path,
        file_type="json",
    ):
        if file_type == "json":
            with open(
                file_path,
            ) as file:
                pipeline = json.load(
                    file,
                )
        elif file_type == "yaml":
            with open(
                file_path,
            ) as file:
                pipeline = (
                    yaml.safe_load(file)
                )
        else:
            raise ValueError(
                "Unsupported file type. Use 'json' or 'yaml'.",
            )

        return pipeline

    def _get_group_by_field(
        self,
        pipeline,
    ):
        # Loop through the pipeline stages
        for stage in pipeline:
            # Check if the stage is a $group stage
            if "$group" in stage:
                group_stage = stage[
                    "$group"
                ]
                # The group by column is the "_id" field in the $group stage
                group_by_field = (
                    group_stage["_id"]
                )
                # Clean up the group by field to remove the leading "$"
                if isinstance(
                    group_by_field,
                    str,
                ) and group_by_field.startswith(
                    "$",
                ):
                    return group_by_field[
                        1:
                    ]  # Remove the leading '$'
                return group_by_field

    def run_aggregation_from_file(
        self,
        collection_name,
        file_path,
        file_type="json",
    ):
        pipeline = self._read_pipeline_from_json(
            file_path,
        )

        group_by_field = (
            self._get_group_by_field(
                pipeline,
            )
        )

        results = self.run_aggregation(
            collection_name,
            pipeline,
        )

        return results, group_by_field

    def export_aggregation_to_csv(
        self,
        results,
        output_file="output.csv",
    ):
        if not results:
            print(
                "No results to export.",
            )
            return

        keys = set()

        for doc in results:
            keys.update(doc.keys())

        keys = list(
            keys,
        )  # Convert the set to a list for CSV header

        # TODO use csv service.
        with open(
            output_file,
            mode="w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=keys,
            )
            writer.writeheader()
            for doc in results:
                writer.writerow(doc)

        print(
            f"Exported {len(results)} documents to {output_file}",
        )

    def close_connection(self):
        self.client.close()
