import pyodbc


class RelationalDatabaseClient:
    def __init__(
        self,
        connection_string,
    ):
        self.conn = pyodbc.connect(
            connection_string,
        )
        self.cursor = self.conn.cursor()

    def execute_query(
        self,
        query_string,
    ):
        self.cursor.execute(
            query_string,
        )

        rows = self.cursor.fetchall()

        return rows

        def close(self):
            self.conn.close()
