import matplotlib.pyplot as plt
import networkx as nx


class Networks:
    def __init__(self):
        self.network_graph = nx.Graph()

    def add_node_list(self, nodes):
        self.network_graph.add_nodes_from(
            nodes_for_adding=nodes,
        )

    def add_edge_list(self):
        for node in list(
            self.network_graph.nodes,
        ):
            for (
                connected_node
            ) in node.connected_nodes:
                self.network_graph.add_edge(
                    node,
                    connected_node,
                )

    def report_connected_nodes(self):
        connected_node_list = (
            nx.connected_components(
                self.network_graph,
            )
        )

        return connected_node_list

    def show_graph(self):
        print("drawing graph_service")

        nx.draw(self.network_graph)

        plt.draw()
        plt.show()
