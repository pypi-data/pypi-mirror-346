import json
import os

from neo4j_orchestrator_helpers.read_cypher_queries import (
    read_cypher_query_from_file,
)


class CSVConfigurations:
    def __init__(self, config: dict):
        self.csv_path: str = ""
        self.csv_file_delimiter: str = (
            config.get(
                "csv_file_delimiter",
                ",",
            )
        )
        self.csv_file_quote_character: (
            str
        ) = config.get(
            "csv_file_quote_character",
            '"',
        )
        self.csv_file_encoding: str = (
            config.get(
                "csv_file_encoding",
                "utf-8",
            )
        )
        self.csv_escape_character: (
            str
        ) = config.get(
            "csv_escape_character",
            "\\",
        )


class Neo4jLoaderConfigurations:
    def __init__(
        self,
        configuration_file: str,
    ):
        with open(
            configuration_file,
        ) as file:
            json_model = json.load(file)
            self.batch_size: int = (
                json_model.get(
                    "batch_size",
                    1000,
                )
            )
            self.concurrency: int = (
                json_model.get(
                    "concurrency",
                    4,
                )
            )
            self.data_input_folder_absolute_path = json_model.get(
                "data_input_folder_absolute_path",
                "",
            )
            self.csv_configurations: (
                CSVConfigurations
            ) = CSVConfigurations(
                json_model.get(
                    "csv_configurations",
                    {},
                ),
            )
            self.emptyIsNull: bool = (
                json_model.get(
                    "emptyIsNull",
                    False,
                )
            )
            self.debug: bool = (
                json_model.get(
                    "debug",
                    False,
                )
            )

    def load_data_and_query_configurations(
        self,
        data_csv,
        cypher_query_file,
    ):
        self.csv_configurations.csv_path = os.path.join(
            self.data_input_folder_absolute_path,
            data_csv,
        )

        self.cypher_query_path = os.path.join(
            self.data_input_folder_absolute_path,
            cypher_query_file,
        )

        print(
            f"Cypher Query Path: {self.cypher_query_path}\n",
        )
        self.load_cypher_query = (
            read_cypher_query_from_file(
                self.cypher_query_path,
            )
        )

        print(
            f"Cypher Query:\n {self.load_cypher_query}\n",
        )

    def print_configuration(self):
        print(
            "loadCSVToNeo4j started file: "
            + self.csv_configurations.csv_path,
        )
        print(
            f"               concurrency: {self.concurrency}",
        )
        print(
            f"                 batchSize: {self.batch_size} ",
        )
        print(
            f"                 delimiter: {self.csv_configurations.csv_file_delimiter} ",
        )
        print(
            f"                 quotechar: {self.csv_configurations.csv_file_quote_character} ",
        )
        print(
            f"                escapechar: {self.csv_configurations.csv_escape_character} ",
        )
        if self.debug:
            print(
                f"                     query: {self.load_cypher_query}",
            )


# Example configuration JSON file content
example_configuration = {
    "batch_size": 2000,
    "concurrency": 8,
    "csv_configurations": {
        "csv_file_delimiter": ";",
        "csv_file_quote_character": "'",
        "csv_file_encoding": "utf-8",
        "csv_escape_character": "\\",
    },
    "emptyIsNull": True,
    "debug": True,
}
