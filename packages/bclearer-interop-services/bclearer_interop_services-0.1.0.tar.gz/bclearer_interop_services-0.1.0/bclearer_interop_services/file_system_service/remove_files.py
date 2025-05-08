import os


def remove_all_files_from_folder(
    folder_name: str,
):
    for file_name in os.listdir(
        folder_name,
    ):
        file_path = os.path.join(
            folder_name,
            file_name,
        )
        try:
            if os.path.isfile(
                file_path,
            ):
                os.unlink(file_path)

        except Exception as exception:
            print(exception)
