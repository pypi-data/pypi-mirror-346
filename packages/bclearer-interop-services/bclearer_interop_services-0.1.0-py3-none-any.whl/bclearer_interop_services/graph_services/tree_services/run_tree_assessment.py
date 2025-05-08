import pandas as pd
from graph_service.source.code.general_graph_services.tree_services.tree_level_assessment.tree_level_reporter import (
    check_tree_level,
)


def orchestrate_tree_level_reporting(
    tree_data_file_name,
    node_column_name,
    parent_node_column_name,
    output_file_name,
):
    file_read = pd.read_excel(
        tree_data_file_name,
    )

    df = check_tree_level(
        file_read,
        node_column_name,
        parent_node_column_name,
    )

    df.to_csv(output_file_name)
