from tkinter import Tk, filedialog

from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


def select_folder(
    title="Please select a directory",
) -> Folders:
    root = Tk()

    root.lift()

    file_path = filedialog.askdirectory(
        parent=root,
        initialdir="/",
        title=title,
    )

    root.withdraw()

    folder = Folders(
        absolute_path_string=file_path,
    )

    return folder
