import os
import shutil
import stat

from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


def remove_folder_contents(
    folder: Folders,
):
    for directory in os.listdir(
        folder.absolute_path_string,
    ):
        shutil.rmtree(
            folder.absolute_path_string
            + os.sep
            + directory,
            onerror=onerror,
        )


def onerror(func, path, exc_info):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise
