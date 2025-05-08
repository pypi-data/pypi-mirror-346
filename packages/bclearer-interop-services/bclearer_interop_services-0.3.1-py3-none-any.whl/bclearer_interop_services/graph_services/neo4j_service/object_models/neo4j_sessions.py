import pandas as pd
from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_connections import (
    Neo4jConnections,
)
from neo4j import (
    READ_ACCESS,
    WRITE_ACCESS,
    Driver,
    GraphDatabase,
)


class Neo4jSessions:

    def __init__(
        self,
        connection: Neo4jConnections,
        access_mode=WRITE_ACCESS,
    ):

        self.connection = connection
        self.database_name = (
            self.connection.database_name
        )
        self.access_mode = access_mode

    def execute_cypher_query(
        self,
        query,
    ):
        try:
            with GraphDatabase.driver(
                uri=self.connection.uri,
                auth=self.connection.auth,
                max_connection_pool_size=self.connection.max_connection_pool_size,
            ) as driver:

                result = driver.execute_query(
                    query
                )
                records = list(result)

            return records
        finally:
            if driver:
                driver.close()

    def execute_cypher_query_with_parameters(
        self,
        query,
        params={},
        output="all",
    ):
        if output not in [
            "all",
            "none",
            "summary",
        ]:
            print(
                "ERROR: output parameter must have one of the follwing values :'all','none','summary' ",
            )
            return

        show_summary = True
        show_data = True

        if output != "all":
            show_data = False

        if output == "none":
            show_summary = False

        qq = query.strip()

        if len(qq) > 50:
            qq = (
                qq[0:76].replace(
                    "\n",
                    "",
                )
                + "..."
            )

        if show_summary:
            print(f"run_cypher : {qq}")

        with GraphDatabase.driver(
            uri=self.connection.uri,
            auth=self.connection.auth,
            max_connection_pool_size=self.connection.max_connection_pool_size,
        ) as driver:

            with driver.session() as session:

                result = session.run(
                    query.strip(),
                    params,
                )

                # If the query does not return records (e.g., it's a write operation), return the summary or similar
                if result.keys():
                    return [
                        record
                        for record in result
                    ]  # Ensure result is a list of Neo4j records

            df = pd.DataFrame(
                [
                    r.values()
                    for r in result
                ],
                columns=result.keys(),
            )

            # Get query summary
            results_summary = (
                result.consume()
            )
            summary_counters = (
                results_summary.counters
            )

            if (
                df.size > 0
                and show_summary
            ):
                print(
                    f"Results available after {results_summary.result_available_after}ms, "
                    f"finished query after {results_summary.result_consumed_after}ms"
                )

            # Prepare report based on summary counters
            query_execution_report = (
                self.prepare_report(
                    df,
                    show_data,
                    show_summary,
                    summary_counters,
                )
            )
            return (
                query_execution_report
            )

    def prepare_report(
        self,
        df,
        show_data,
        show_summary,
        summary_counters,
    ):
        # Dynamically generate the report for summary counters
        counters = {
            "nodes_created": summary_counters.nodes_created,
            "nodes_deleted": summary_counters.nodes_deleted,
            "relationships_created": summary_counters.relationships_created,
            "relationships_deleted": summary_counters.relationships_deleted,
            "properties_set": summary_counters.properties_set,
            "labels_added": summary_counters.labels_added,
            "labels_removed": summary_counters.labels_removed,
            "indexes_added": summary_counters.indexes_added,
            "indexes_removed": summary_counters.indexes_removed,
            "constraints_added": summary_counters.constraints_added,
            "constraints_removed": summary_counters.constraints_removed,
            "system_updates": summary_counters.system_updates,
        }

        df2 = pd.DataFrame(
            columns=["counter", "value"]
        )

        for (
            counter,
            value,
        ) in counters.items():
            if value > 0:
                df2.loc[
                    len(df2.index)
                ] = [counter, value]

        # Output results if requested
        if show_data and df.size > 0:
            print(df)
        if (
            show_summary
            and df2.size > 0
        ):
            print(df2)
        if (
            show_summary
            and df2.size == 0
            and df.size == 0
        ):
            print(
                "(no changes, no records)"
            )

        return df2

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):
        pass
