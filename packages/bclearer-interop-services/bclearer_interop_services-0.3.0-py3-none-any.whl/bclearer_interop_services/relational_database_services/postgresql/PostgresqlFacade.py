import pandas as pd
import psycopg2
from bclearer_interop_services.relational_database_services.RelationaDatabaseFacade import (
    DatabaseFacade,
)


class PostgresqlFacade(DatabaseFacade):
    def connect(self):
        self.connection = (
            psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
            )
        )

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(
        self,
        query,
        params=None,
    ):
        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                params,
            )
            self.connection.commit()

    def fetch_results(
        self,
        query,
        params=None,
    ) -> pd.DataFrame:
        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                params,
            )
            columns = [
                desc[0]
                for desc in cursor.description
            ]
            results = cursor.fetchall()
        return pd.DataFrame(
            results,
            columns=columns,
        )

    def store_dataframe(
        self,
        dataframe,
        table_name,
    ):
        cursor = (
            self.connection.cursor()
        )

        # Check if table exists
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = %s
            );
        """,
            (table_name,),
        )

        table_exists = (
            cursor.fetchone()[0]
        )

        if table_exists:
            # Check schema conformity
            cursor.execute(
                """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s;
            """,
                (table_name,),
            )

            db_schema = (
                cursor.fetchall()
            )

            # Define a mapping from pandas dtype to SQL data type
            pandas_to_sql_dtype_map = {
                "object": "text",  # assuming 'object' type in pandas corresponds to 'text' in SQL
                "int64": "integer",
                "float64": "float",
                "bool": "boolean",
                # add other mappings as necessary
            }

            # Convert DataFrame schema to a dictionary with mapped SQL types
            df_schema = [
                (
                    col,
                    pandas_to_sql_dtype_map.get(
                        str(dtype),
                        str(dtype),
                    ),
                )  # Map pandas dtypes to SQL equivalent
                for col, dtype in zip(
                    dataframe.columns,
                    dataframe.dtypes,
                )
            ]

            db_schema_dict = {
                col: dtype
                for col, dtype in db_schema
            }

            df_schema_dict = {
                col: dtype
                for col, dtype in df_schema
            }

            if (
                db_schema_dict
                != df_schema_dict
            ):
                raise ValueError(
                    "Schema of DataFrame does not match schema of the table.",
                )

            # Insert DataFrame into the existing table
            for (
                row
            ) in dataframe.itertuples(
                index=False,
                name=None,
            ):
                cursor.execute(
                    f"INSERT INTO {table_name} ({', '.join(dataframe.columns)}) VALUES ({', '.join(['%s'] * len(dataframe.columns))})",
                    row,
                )
        else:
            # Create table and insert DataFrame
            col_defs = ", ".join(
                [
                    f"{col} {self._map_dtype(dtype)}"
                    for col, dtype in zip(
                        dataframe.columns,
                        dataframe.dtypes,
                    )
                ],
            )
            cursor.execute(
                f"CREATE TABLE {table_name} ({col_defs});",
            )

            for (
                row
            ) in dataframe.itertuples(
                index=False,
                name=None,
            ):
                cursor.execute(
                    f"INSERT INTO {table_name} ({', '.join(dataframe.columns)}) VALUES ({', '.join(['%s'] * len(dataframe.columns))})",
                    row,
                )

        self.connection.commit()
        cursor.close()

    def _map_dtype(self, dtype):
        if "int" in str(dtype):
            return "INTEGER"
        if "float" in str(dtype):
            return "REAL"
        if "object" in str(dtype):
            return "TEXT"
        if "datetime" in str(dtype):
            return "TIMESTAMP"
        raise ValueError(
            f"Unrecognized dtype: {dtype}",
        )
