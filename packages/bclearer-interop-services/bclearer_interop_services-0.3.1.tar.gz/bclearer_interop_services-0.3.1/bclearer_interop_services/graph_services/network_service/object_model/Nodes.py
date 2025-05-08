class Node:
    _registry = (
        {}
    )  # registry for keeping a list of nodes

    def __init__(
        self,
        node_uuid,
        connected_nodes,
    ):
        self.node_uuid = node_uuid  # node property for storing the node id taken from the sameAsList uuids
        self._registry.update(
            {self.node_uuid: self},
        )  # node property for adding the node to the Node class registry
        self.connected_nodes = (
            set()
        )  # node property for storing the set of connected node objects

    def add_connected_nodes(
        self,
        node_uuid_for_appending,
    ):  # adds a node and node luid to the nodes connected nodes list
        node_for_appending = (
            self.convert_uuid_to_node(
                node_uuid_for_appending,
            )
        )  # retreive node using uuid

        self.connected_nodes.add(
            node_for_appending,
        )  # add node to connected node set

    @classmethod
    def get_node_list(cls):
        node_list = []
        for (
            key,
            node_in_focus,
        ) in Node._registry.items():
            node_list.append(
                node_in_focus,
            )
        return node_list

    def convert_uuid_to_node(
        node_uuid_for_appending,
    ):
        if (
            node_uuid_for_appending
            in Node._registry
        ):  # check nodes exists
            return Node._registry[
                node_uuid_for_appending
            ]  # return node if found
        return Node(
            node_uuid_for_appending,
            [],
        )  # retrun newly created node if not found
