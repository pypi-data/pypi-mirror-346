import sys

import bclearer_interop_services.graph_services.neo4j_service.object_models as neo4j_object_models

sys.modules["neo4j_object_models"] = (
    neo4j_object_models
)
