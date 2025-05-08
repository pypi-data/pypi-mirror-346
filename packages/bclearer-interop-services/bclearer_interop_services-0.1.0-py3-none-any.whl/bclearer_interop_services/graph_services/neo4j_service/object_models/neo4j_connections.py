from neo4j import GraphDatabase


class Neo4jConnections:

    def __init__(
        self,
        uri=None,
        database_name=None,
        user_name=None,
        password=None,
        max_connection_pool_size=None,
    ):
        self.uri = uri
        self.auth = (
            user_name,
            password,
        )
        self.database_name = (
            database_name
        )
        self.max_connection_pool_size = (
            max_connection_pool_size
        )
        self._driver = None  # Driver will be lazily instantiated

    def get_driver(self):
        # Lazy instantiation of the driver
        if self._driver is None:
            self._driver = GraphDatabase.driver(
                uri=self.uri,
                auth=self.auth,
                max_connection_pool_size=self.max_connection_pool_size,
            )
        return self._driver

    def close(self):
        if self._driver:
            self._driver.close()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        self._driver.close()
        self.close()
