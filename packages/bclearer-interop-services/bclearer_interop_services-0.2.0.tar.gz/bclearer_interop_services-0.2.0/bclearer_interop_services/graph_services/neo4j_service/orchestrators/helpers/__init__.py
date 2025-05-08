import sys

import bclearer_interop_services.graph_services.neo4j_service.constants as neo4j_constants
import bclearer_interop_services.graph_services.neo4j_service.orchestrators.helpers as neo4j_orchestrator_helpers
from bclearer_interop_services.graph_services import (
    neo4j_service,
)

sys.modules["neo4j_constants"] = (
    neo4j_constants
)
sys.modules["neo4j_service"] = (
    neo4j_service
)
