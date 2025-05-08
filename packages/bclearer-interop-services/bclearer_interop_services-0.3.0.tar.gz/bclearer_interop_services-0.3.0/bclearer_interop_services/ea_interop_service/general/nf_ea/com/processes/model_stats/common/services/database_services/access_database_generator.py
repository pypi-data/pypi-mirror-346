from datetime import datetime

import msaccessdb


def create_access_db(
    parent_folder_path: str,
    database_name: str,
) -> str:
    today_time = datetime.today()

    access_database_path = rf'{parent_folder_path}\{database_name}_{today_time.strftime("%b%d%Y%H%M%S")}.accdb'

    msaccessdb.create(
        access_database_path
    )

    return access_database_path
