import os

from bclearer_interop_services.excel_services.interop.excel_write import (
    save_table_in_excel,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.graph_services.network_service.graph_to_nodes_and_edges_tables_converter import (
    convert_graph_to_nodes_and_edges_tables,
)


# TODO: move to graph services
def export_graph_to_excel(
    graph,
    graph_name: str,
    node_id_column_name: str,
    output_folder: Folders,
) -> None:
    nodes_table, edges_table = (
        convert_graph_to_nodes_and_edges_tables(
            graph=graph,
            node_id_column_name=node_id_column_name,
        )
    )

    graph_full_filename_root = (
        output_folder.absolute_path_string
        + os.sep
        + graph_name
    )

    save_table_in_excel(
        table=nodes_table,
        full_filename=graph_full_filename_root
        + "_nodes.xlsx",
        sheet_name=graph_name[:29],
    )

    save_table_in_excel(
        table=edges_table,
        full_filename=graph_full_filename_root
        + "_edges.xlsx",
        sheet_name=graph_name[:29],
    )
