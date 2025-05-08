from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_connections import (
    Neo4jConnections,
)
from bclearer_interop_services.graph_services.neo4j_service.object_models.neo4j_sessions import (
    Neo4jSessions,
)
from neo4j import GraphDatabase


class Neo4jDatabases:

    def __init__(
        self,
        uri=None,
        user=None,
        password=None,
        database_name="neo4j",
        external_connection=None,
    ):
        if external_connection is None:
            self.connection = Neo4jConnections(
                uri=uri,
                database_name=database_name,
                user_name=user,
                password=password,
            )
        else:
            self.connection = (
                external_connection
            )
        self._driver = None  # Driver will be lazily instantiated

    def _get_driver(self):
        # Lazy instantiation of the driver
        if self._driver is None:
            self._driver = (
                self.connection.get_driver()
            )
        return self._driver

    def get_new_session(
        self, database: str = "neo4j"
    ):

        session = Neo4jSessions(
            connection=self.connection
        )
        return session

    def run_query(
        self, query, parameters=None
    ):

        session = self.get_new_session()
        result = session.execute_cypher_query_with_parameters(
            query, parameters
        )
        return [
            record.data()
            for record in result
        ]

    def close(self):
        if self._driver:
            self._driver.close()

    def __exit__(
        self, exc_type, exc_val, exc_tb
    ):
        self.close()
