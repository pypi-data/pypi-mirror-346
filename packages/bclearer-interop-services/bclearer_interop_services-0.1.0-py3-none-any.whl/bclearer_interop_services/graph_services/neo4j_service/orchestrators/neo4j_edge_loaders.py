import concurrent
import logging
import time
from concurrent.futures import (
    ThreadPoolExecutor,
)

import pandas as pd


class EdgeLoader:
    def __init__(
        self,
        neo4j_database,
        batch_size=1000,
        max_retries=3,
        retry_delay=1,
    ):

        self.neo4j_database = (
            neo4j_database
        )
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def load_edges(
        self,
        edge_data: pd.DataFrame,
        mapping_query: str,
    ):
        with ThreadPoolExecutor() as executor:

            futures = [
                executor.submit(
                    self._load_edge_batch,
                    edge_data[
                        i : i
                        + self.batch_size
                    ],
                    mapping_query,
                )
                for i in range(
                    0,
                    len(edge_data),
                    self.batch_size,
                )
            ]
            concurrent.futures.wait(
                futures,
            )

    def _load_edge_batch(
        self,
        batch_df,
        mapping_query,
    ):
        for attempt in range(
            self.max_retries,
        ):
            try:
                batch = batch_df.to_dict(
                    orient="records",
                )

                logging.debug(
                    f"Executing batch query with {len(batch)} rows.",
                )

                self.neo4j_database.run_query(
                    mapping_query,
                    parameters={
                        "batch": batch,
                    },
                )

            except Exception as e:
                logging.exception(
                    f"Error executing query: {e} \n Query: {mapping_query} \n Data: \n {batch}",
                )

                if (
                    "DeadlockDetected"
                    in str(e)
                ):
                    if (
                        attempt
                        < self.max_retries
                        - 1
                    ):
                        logging.warning(
                            f"Deadlock detected. Retrying in {self.retry_delay} seconds...",
                        )

                        time.sleep(
                            self.retry_delay,
                        )

                    else:
                        logging.exception(
                            "Max retries reached. Failing batch.",
                        )
                        raise
                else:
                    raise

    def _load_edge(
        self,
        row,
        edge_label,
        mapping_query,
    ):
        try:
            # query = mapping_query.format(
            #     **row)
            print(
                f"Executing query: {mapping_query}"
            )
            self.neo4j_database.run_query(
                query=mapping_query,
                parameters=row,
            )
        except Exception as e:
            print(
                f"Error loading edge with data {row}: {e}"
            )
