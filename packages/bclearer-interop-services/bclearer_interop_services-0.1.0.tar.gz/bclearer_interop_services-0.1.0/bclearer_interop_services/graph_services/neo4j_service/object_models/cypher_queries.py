import re


class CypherQueryWrapper:
    def __init__(self, query=""):
        self.query = query

    # Read Cypher query from file
    def read_from_file(self, file_path):
        try:
            with open(
                file_path,
            ) as file:
                self.query = file.read()
            print(
                "Query successfully read from file.",
            )
        except FileNotFoundError:
            print(
                f"Error: {file_path} not found.",
            )
        except Exception as e:
            print(
                f"Error reading file: {e}",
            )

    # Write Cypher query to file
    def write_to_file(self, file_path):
        try:
            with open(
                file_path,
                "w",
            ) as file:
                file.write(self.query)
            print(
                f"Query successfully written to {file_path}.",
            )
        except Exception as e:
            print(
                f"Error writing to file: {e}",
            )

    # Validate the Cypher query structure using a simple regex pattern
    def validate(self):
        # Basic validation to check if it's a valid Cypher query structure
        pattern = r"MATCH|CREATE|RETURN|WITH|SET|DELETE|MERGE"
        if re.search(
            pattern,
            self.query,
            re.IGNORECASE,
        ):
            print("Query is valid.")
            return True
        print("Invalid Cypher query.")
        return False

    # Generate Cypher query to find all nodes of a specific label
    @staticmethod
    def generate_find_all_nodes(label):
        return f"MATCH (n:{label}) RETURN n"

    # Generate Cypher query to find all edges of a specific type
    @staticmethod
    def generate_find_all_edges(
        edge_type,
    ):
        return f"MATCH ()-[r:{edge_type}]->() RETURN r"

    # Generate Cypher query to create a node with properties
    @staticmethod
    def generate_create_node(
        label,
        properties,
    ):
        prop_string = ", ".join(
            [
                f"{key}: '{value}'"
                for key, value in properties.items()
            ],
        )
        return f"CREATE (n:{label} {{ {prop_string} }}) RETURN n"
