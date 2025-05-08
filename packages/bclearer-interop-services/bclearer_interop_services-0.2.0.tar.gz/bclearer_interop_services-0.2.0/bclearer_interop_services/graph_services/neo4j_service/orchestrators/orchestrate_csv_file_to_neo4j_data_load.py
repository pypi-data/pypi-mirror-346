from bclearer_interop_services.graph_services.neo4j_service.configurations.neo4j_loader_configurations import (
    Neo4jLoaderConfigurations,
)
from bclearer_interop_services.graph_services.neo4j_service.constants.GraphDataObjectTypes import (
    GraphObjectTypes,
)
from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_connections import (
    Neo4jConnections,
)
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.helpers.nodes_load_information_getter import (
    get_graph_object_load_information,
)
from bclearer_interop_services.graph_services.neo4j_service.orchestrators.neo4j_data_load_orchestrators import (
    Neo4jDataLoadOrchestrators,
)


def orchestrate_csv_to_neo4j_data_load(
    neo4j_connection: Neo4jConnections,
    neo4j_loader_configuration: Neo4jLoaderConfigurations,
    object_type: GraphObjectTypes,
):
    load_object_information = get_graph_object_load_information(
        csv_file_path=neo4j_loader_configuration.csv_configurations.csv_path,
        query_file_path=neo4j_loader_configuration.cypher_query_path,
        graph_object_type=object_type,
    )

    data_load_orchestrator = Neo4jDataLoadOrchestrators(
        neo4j_connection=neo4j_connection,
        batch_size=1000,
    )

    data_load_orchestrator.orchestrate_neo4j_data_load_from_csv(
        load_object_information,
    )
