# list_tree_node_superiors
def list_tree_node_superiors(
    tree_node,
    superior_node_list,
):
    """For a functional location, recursively search for all superior functional location
    Args:
        floc (str):
        d_floc_superior (dict):

    Returns
    -------
            list of superior functional locations

    """
    if (
        tree_node
        in superior_node_list.keys()
    ):
        parent = superior_node_list[
            tree_node
        ]

        if (
            parent
            and len(str(parent)) > 3
        ):
            list_of_superior_tree_nodes = [
                parent,
            ] + list_tree_node_superiors(
                parent,
                superior_node_list=superior_node_list,
            )

            return list_of_superior_tree_nodes
        return []
    return []


# report_tree_node_level
def report_tree_node_level(
    tree_dataframe,
    tree_node_column_name,
    superior_node_column_name,
):
    """For a tree, construct list of all ancestors, whose length indicates
    level
    Args:
        df (pd.DataFrame): tree data
        floc_col_name (str): column name of node
        superior_node_column_name (str): column name for parent node

    Returns
    -------
        df (pd.DataFrame): tree data with ancestor list and level

    """
    tree_node_superior = pd.Series(
        tree_dataframe[
            superior_node_column_name
        ].values,
        index=tree_dataframe[
            tree_node_column_name
        ],
    ).to_dict()

    tree_dataframe[
        "list_of_superior_nodes"
    ] = tree_dataframe[
        tree_node_column_name
    ].apply(
        lambda x: list_tree_node_superiors(
            tree_node=x,
            superior_node_list=tree_node_superior,
        ),
    )
    tree_dataframe[
        "num_list_superior_nodes"
    ] = tree_dataframe[
        "list_superior_nodes"
    ].apply(
        len,
    )

    return tree_dataframe
