import os


def build_structure(
    root_dir,
    structure=None,
    relative_path="",
):
    if structure is None:
        structure = {}

    for item in os.listdir(root_dir):
        item_path = os.path.join(
            root_dir,
            item,
        )

        item_relative_path = (
            os.path.join(
                relative_path,
                item,
            )
        )

        if os.path.isdir(item_path):
            if item not in structure:
                structure[item] = {}
            build_structure(
                item_path,
                structure[item],
                item_relative_path,
            )

        elif os.path.isfile(item_path):
            key = item.replace(
                ".csv",
                "",
            ).replace(".cypher", "")

            if key not in structure:
                structure[key] = {}

            if item.endswith(".csv"):
                structure[key][
                    "data"
                ] = item_relative_path

            elif item.endswith(
                ".cypher",
            ):
                structure[key][
                    "cypher"
                ] = item_relative_path

    return structure


def merge_structures(
    load_files_structure,
    queries_structure,
):
    merged_structure = {}

    def merge_recursive(
        load_dict,
        query_dict,
    ):
        merged = {}
        for key in load_dict:
            merged[key] = {}
            if key in query_dict:
                if isinstance(
                    load_dict[key],
                    dict,
                ) and isinstance(
                    query_dict[key],
                    dict,
                ):
                    merged[key] = (
                        merge_recursive(
                            load_dict[
                                key
                            ],
                            query_dict[
                                key
                            ],
                        )
                    )
                else:
                    merged[key] = {
                        "data": load_dict[
                            key
                        ].get(
                            "data",
                            None,
                        ),
                        "cypher": query_dict[
                            key
                        ].get(
                            "cypher",
                            None,
                        ),
                    }
            else:
                merged[key] = load_dict[
                    key
                ]
        for key in query_dict:
            if key not in merged:
                merged[key] = (
                    query_dict[key]
                )
        return merged

    merged_structure = merge_recursive(
        load_files_structure,
        queries_structure,
    )

    return merged_structure


def generate_load_dataset_from_folder(
    parent_folder,
):
    load_files_dir = os.path.join(
        parent_folder,
        "load_files",
    )
    queries_dir = os.path.join(
        parent_folder,
        "queries",
    )

    load_files_structure = (
        build_structure(load_files_dir)
    )
    queries_structure = build_structure(
        queries_dir,
    )
    merged_structure = merge_structures(
        load_files_structure,
        queries_structure,
    )

    return merged_structure


def iterate_structure(structure):
    """This function takes a nested dictionary structure and returns a list of dictionaries,
    each containing the paths of the CSV and Cypher query pairs.

    Args:
    structure (dict): The input nested dictionary structure

    Returns:
    -------
    list: A list of dictionaries with 'data' and 'cypher' keys.

    """
    result = []

    def recurse(structure):
        for (
            key,
            value,
        ) in structure.items():
            if isinstance(value, dict):
                if (
                    "data" in value
                    and "cypher"
                    in value
                ):
                    csv_path = value[
                        "data"
                    ]
                    cypher_path = value[
                        "cypher"
                    ]
                    result.append(
                        {
                            "data": csv_path,
                            "cypher": cypher_path,
                        },
                    )
                else:
                    recurse(value)

    recurse(structure)
    return result


def categorize_structure(structure):
    """This function takes a nested dictionary structure and returns two lists:
    one for node pairs and one for edge pairs.

    Args:
    structure (dict): The input nested dictionary structure

    Returns:
    -------
    tuple: A tuple containing two lists - one for node pairs and one for edge pairs.

    """
    nodes = []
    edges = []

    def recurse(structure, path=""):
        for (
            key,
            value,
        ) in structure.items():
            if isinstance(value, dict):
                new_path = os.path.join(
                    path,
                    key,
                )
                if (
                    "data" in value
                    and "cypher"
                    in value
                ):
                    pair = {
                        "data": value[
                            "data"
                        ],
                        "cypher": value[
                            "cypher"
                        ],
                    }

                    if (
                        "01_nodes"
                        in new_path
                    ):
                        nodes.append(
                            pair,
                        )

                    elif (
                        "02_edges"
                        in new_path
                    ):
                        edges.append(
                            pair,
                        )
                else:
                    recurse(
                        value,
                        new_path,
                    )

    recurse(structure)
    return nodes, edges


def get_load_dataset(parent_folder):
    structure = generate_load_dataset_from_folder(
        parent_folder,
    )
    load_dataset = iterate_structure(
        structure,
    )
    return load_dataset


def get_load_dataset_by_graph_object_type(
    parent_folder,
):
    structure = generate_load_dataset_from_folder(
        parent_folder,
    )

    nodes, edges = categorize_structure(
        structure,
    )

    return nodes, edges
