from bclearer_interop_services.relational_database_services.postgresql.PostgresqlFacade import (
    PostgresqlFacade,
)


# Factory class to get the correct database implementation
class DatabaseFactory:
    @staticmethod
    def get_database(
        db_type,
        host,
        database,
        user,
        password,
    ):
        if db_type == "postgresql":
            return PostgresqlFacade(
                host,
                database,
                user,
                password,
            )
        # You can add more database types here (e.g., MySQL, SQLite)
        raise ValueError(
            f"Unsupported database type: {db_type}",
        )
