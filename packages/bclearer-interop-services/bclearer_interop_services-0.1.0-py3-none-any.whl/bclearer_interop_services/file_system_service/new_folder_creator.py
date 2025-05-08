import os


def create_new_folder(
    parent_folder_path: str,
    new_folder_name: str,
) -> str:
    new_folder_path = os.path.join(
        parent_folder_path,
        new_folder_name,
    )

    try:
        os.mkdir(new_folder_path)

    except FileExistsError:
        print(
            "Target folder already exists.",
        )

    return new_folder_path
