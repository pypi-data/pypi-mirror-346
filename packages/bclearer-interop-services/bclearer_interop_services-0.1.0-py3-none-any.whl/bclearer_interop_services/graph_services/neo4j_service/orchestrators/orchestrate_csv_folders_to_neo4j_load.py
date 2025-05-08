import os

from bclearer_interop_services.graph_services.neo4j_service.configurations.neo4j_loader_configurations import (
    Neo4jLoaderConfigurations,
)
from bclearer_interop_services.graph_services.neo4j_service.constants import (
    LoaderDataFolderNames,
)
from bclearer_interop_services.graph_services.neo4j_service.constants.GraphDataObjectTypes import (
    GraphObjectTypes,
)
from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_connections import (
    Neo4jConnections,
)
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.helpers.prepare_dataset_dictionary_from_folder import (
    get_load_dataset_by_graph_object_type,
)
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.orchestrate_csv_file_to_neo4j_data_load import (
    orchestrate_csv_to_neo4j_data_load,
)


def orchestrate_csv_folders_to_neo4j_load(
    neo4j_loader_configuration_path,
    neo4j_connection,
):
    neo4j_loader_configuration = Neo4jLoaderConfigurations(
        configuration_file=neo4j_loader_configuration_path,
    )

    (
        node_load_dataset,
        edge_load_dataset,
    ) = get_load_dataset_by_graph_object_type(
        neo4j_loader_configuration.data_input_folder_absolute_path,
    )

    orchestrate_graph_object_load(
        neo4j_connection=neo4j_connection,
        neo4j_loader_configuration=neo4j_loader_configuration,
        graph_object_load_dataset=node_load_dataset,
        graph_object_type=GraphObjectTypes.NODES,
    )

    orchestrate_graph_object_load(
        neo4j_connection=neo4j_connection,
        neo4j_loader_configuration=neo4j_loader_configuration,
        graph_object_load_dataset=edge_load_dataset,
        graph_object_type=GraphObjectTypes.EDGES,
    )


def orchestrate_graph_object_load(
    neo4j_connection: Neo4jConnections,
    neo4j_loader_configuration: Neo4jLoaderConfigurations,
    graph_object_load_dataset,
    graph_object_type: GraphObjectTypes,
):
    for (
        pair
    ) in graph_object_load_dataset:
        csv_relative_path = os.path.join(
            LoaderDataFolderNames.DATA,
            pair["data"],
        )

        cypher_relative_path = os.path.join(
            LoaderDataFolderNames.QUERIES,
            pair["cypher"],
        )

        print(
            "loading dataset: \n",
            pair,
        )

        neo4j_loader_configuration.load_data_and_query_configurations(
            data_csv=csv_relative_path,
            cypher_query_file=cypher_relative_path,
        )

        orchestrate_csv_to_neo4j_data_load(
            neo4j_connection=neo4j_connection,
            neo4j_loader_configuration=neo4j_loader_configuration,
            object_type=graph_object_type,
        )
