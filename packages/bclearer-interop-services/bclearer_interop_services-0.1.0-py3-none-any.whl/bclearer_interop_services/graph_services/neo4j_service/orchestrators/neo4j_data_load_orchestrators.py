import pandas as pd
from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_databases import (
    Neo4jDatabases,
)
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.neo4j_edge_loaders import (
    EdgeLoader,
)
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.neo4j_node_loaders import (
    NodeLoader,
)


class Neo4jDataLoadOrchestrators:

    def __init__(
        self,
        neo4j_database: Neo4jDatabases,
    ):
        self.neo4j_database = (
            neo4j_database
        )

        self.node_loader = NodeLoader(
            neo4j_database=self.neo4j_database
        )
        self.edge_loader = EdgeLoader(
            neo4j_database=self.neo4j_database
        )

    def load_data(
        self,
        nodes_info=None,
        edges_info=None,
    ):

        if (
            nodes_info
            and "nodes_info"
            in nodes_info
        ):
            for node in nodes_info[
                "nodes_info"
            ]:
                node_dataframe = (
                    pd.read_csv(
                        node[
                            "csv_file"
                        ],
                    )
                )

                node_dataframe.fillna(
                    value="",
                    inplace=True,
                )

                self.node_loader.load_nodes(
                    node_dataframe,
                    node["query"],
                )

        if edges_info:
            for edge in edges_info[
                "edges_info"
            ]:
                edge_dataframe = (
                    pd.read_csv(
                        edge[
                            "csv_file"
                        ],
                    )
                )

                edge_dataframe.fillna(
                    value="",
                    inplace=True,
                )

                self.edge_loader.load_edges(
                    edge_dataframe,
                    edge["query"],
                )

    def orchestrate_neo4j_data_load_from_csv(
        self,
        object_info,
    ):
        # Determine the type of information provided (nodes, edges, or both)
        nodes_info = object_info.get(
            "nodes_info",
        )
        edges_info = object_info.get(
            "edges_info",
        )

        # Load the data
        self.load_data(
            nodes_info=nodes_info,
            edges_info=edges_info,
        )

        # Close the connection
        self.neo4j_database.close()
