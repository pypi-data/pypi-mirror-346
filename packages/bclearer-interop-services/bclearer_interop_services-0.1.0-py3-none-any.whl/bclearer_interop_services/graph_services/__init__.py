import sys

from bclearer_interop_services.graph_services import (
    neo4j_service,
)

sys.modules["neo4j_service"] = (
    neo4j_service
)
