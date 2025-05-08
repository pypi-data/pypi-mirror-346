import os
from datetime import datetime


def generate_parent_folder(
    parent_folder_path: str,
    stage_name: str,
) -> str:
    today_time = datetime.today()

    folder_name = f'{stage_name}_{today_time.strftime("%b%d%Y%H%M%S")}\\'

    folder_path = os.path.join(
        parent_folder_path, folder_name
    )

    try:
        os.mkdir(folder_path)

    except FileExistsError:
        print(
            "Target folder already exists."
        )

    return folder_path
