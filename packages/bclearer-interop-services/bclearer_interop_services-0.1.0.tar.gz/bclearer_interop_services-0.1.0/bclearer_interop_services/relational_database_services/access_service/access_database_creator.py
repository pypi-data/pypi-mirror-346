import msaccessdb


def create_access_database_in_folder(
    parent_folder_path: str,
    database_name: str,
) -> str:
    access_database_path = rf"{parent_folder_path}\\{database_name}.accdb"

    msaccessdb.create(
        access_database_path,
    )

    return access_database_path
