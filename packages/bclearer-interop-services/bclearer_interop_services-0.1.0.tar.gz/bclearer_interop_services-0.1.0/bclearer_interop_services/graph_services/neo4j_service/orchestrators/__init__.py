import sys

import bclearer_interop_services.graph_services.neo4j_service.configurations as neo4j_configurations
import bclearer_interop_services.graph_services.neo4j_service.constants as neo4j_constants
import bclearer_interop_services.graph_services.neo4j_service.object_models as neo4j_object_models
import bclearer_interop_services.graph_services.neo4j_service.orchestrators as neo4j_orchestrators

sys.modules["neo4j_object_models"] = (
    neo4j_object_models
)
sys.modules["neo4j_orchestrators"] = (
    neo4j_orchestrators
)
sys.modules["neo4j_constants"] = (
    neo4j_constants
)
sys.modules["neo4j_configurations"] = (
    neo4j_configurations
)
