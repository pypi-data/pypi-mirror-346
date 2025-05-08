import glob


def get_first_level_folder_children_paths(
    folder_name_as_string: str,
    root_folder_path_as_string: str,
) -> list:
    root_folder_children_paths = (
        glob.glob(
            root_folder_path_as_string
            + "/"
            + folder_name_as_string
            + "/*",
            recursive=True,
        )
    )

    return root_folder_children_paths
