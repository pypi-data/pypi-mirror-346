import pandas as pd


def report_ancestors(
    tree_node,
    parent_tree_nodes,
):
    if (
        tree_node
        in parent_tree_nodes.keys()
    ):
        parent = parent_tree_nodes[
            tree_node
        ]
        return [
            parent,
        ] + report_ancestors(
            parent,
            parent_tree_nodes=parent_tree_nodes,
        )
    return []


def check_tree_level(
    df,
    node_column_name,
    parent_column_name,
):
    d_parent_nodes = pd.Series(
        df[parent_column_name].values,
        index=df[node_column_name],
    ).to_dict()

    df["list_ancestors"] = df[
        node_column_name
    ].apply(
        lambda x: report_ancestors(
            tree_node=x,
            parent_tree_nodes=d_parent_nodes,
        ),
    )

    df["len_list_ancestors"] = df[
        "list_ancestors"
    ].apply(len)

    return df
