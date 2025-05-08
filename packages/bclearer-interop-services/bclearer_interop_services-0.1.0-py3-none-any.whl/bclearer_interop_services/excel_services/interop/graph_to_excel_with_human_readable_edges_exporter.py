import os

from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
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
def export_graph_to_excel_with_human_readable_edges(
    graph,
    graph_name: str,
    output_folder: Folders,
    export_also_nodes_table: bool,
    node_id_column_name: str,
    node_name_column_name: str,
    edge_source_column_name: str = "bclearer_interop_services",
    edge_target_column_name: str = "target",
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

    if export_also_nodes_table:
        save_table_in_excel(
            table=nodes_table,
            full_filename=graph_full_filename_root
            + "_nodes.xlsx",
            sheet_name=graph_name[:23]
            + "_nodes",
        )

    source_name_column_name = (
        "source_"
        + node_name_column_name
    )

    human_readable_edges_table = left_merge_dataframes(
        master_dataframe=edges_table,
        master_dataframe_key_columns=[
            edge_source_column_name,
        ],
        merge_suffixes=["_1, _2"],
        foreign_key_dataframe=nodes_table,
        foreign_key_dataframe_fk_columns=[
            node_id_column_name,
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            node_name_column_name: source_name_column_name,
        },
    )

    target_name_column_name = (
        "target_"
        + node_name_column_name
    )

    human_readable_edges_table = left_merge_dataframes(
        master_dataframe=human_readable_edges_table,
        master_dataframe_key_columns=[
            edge_target_column_name,
        ],
        merge_suffixes=["_1, _2"],
        foreign_key_dataframe=nodes_table,
        foreign_key_dataframe_fk_columns=[
            node_id_column_name,
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            node_name_column_name: target_name_column_name,
        },
    )

    save_table_in_excel(
        table=human_readable_edges_table,
        full_filename=graph_full_filename_root
        + "_edges_hr.xlsx",
        sheet_name=graph_name[:20]
        + "_edges_hr",
    )
