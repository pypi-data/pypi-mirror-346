import json


class Neo4jConfigurations:
    uri: str
    database_name: str
    username: str
    password: str

    def __init__(
        self,
        configuration_file: str,
    ):
        with open(
            configuration_file,
        ) as file:
            json_model = json.load(file)
            self.uri = json_model["uri"]
            self.database_name = (
                json_model[
                    "database_name"
                ]
            )
            self.username = json_model[
                "username"
            ]
            self.password = json_model[
                "password"
            ]


example_configuration = {
    "uri": "neo4j:<ip address>",
    "database_name": "<database name>",
    "username": "<user name>",
    "password": "<password>",
}
