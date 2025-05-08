from bclearer_interop_services.delimited_text.table_as_dictionary_to_csv_exporter import (
    export_table_as_dictionary_to_csv,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from networkx import (
    DiGraph,
    simple_cycles,
)


def check_directed_graph_cycles(
    directed_graph: DiGraph,
    graph_name: str,
    output_folder: Folders = None,
) -> list:
    cycle_nodes_list = list(
        simple_cycles(G=directed_graph),
    )

    if output_folder:
        __export_cycle_nodes_list(
            cycle_nodes_list=cycle_nodes_list,
            output_folder=output_folder,
            graph_name=graph_name,
        )

    return cycle_nodes_list


def __export_cycle_nodes_list(
    cycle_nodes_list: list,
    output_folder: Folders,
    graph_name: str,
) -> None:
    simple_cycles_dictionary = dict()

    for cycle_nodes in cycle_nodes_list:
        simple_cycles_dictionary[
            str(cycle_nodes)
        ] = {
            "cycle_nodes": cycle_nodes,
        }

    export_table_as_dictionary_to_csv(
        table_as_dictionary=simple_cycles_dictionary,
        output_folder=output_folder,
        output_file_base_name=graph_name
        + "_simple_cycles_report",
    )


#  ONLY FOR STANDALONE TESTING  ################################
# if __name__ == '__main__':
#     graph_service = DiGraph([
#         (1, 2), (2, 3), (1, 4), (4, 5), (5, 6), (6, 4), (3, 1)
#     ])
#
#     check_directed_graph_cycles(
#         directed_graph=graph_service,
#         graph_name='test_graph',
#         output_folder=Folders(r'C:\S\OXi\FDM\apps\unit_tests'))
###################################################
