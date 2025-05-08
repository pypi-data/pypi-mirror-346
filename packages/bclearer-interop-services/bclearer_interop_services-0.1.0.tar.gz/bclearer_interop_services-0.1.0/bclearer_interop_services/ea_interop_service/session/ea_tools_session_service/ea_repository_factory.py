import tkinter as tk
from tkinter import simpledialog

from bclearer_interop_services.ea_interop_service.general.ea.com.ea_com_managers import (
    EaComManagers,
)
from bclearer_interop_services.ea_interop_service.general.ea.com.ea_repository_factory import (
    create_ea_repository,
    create_empty_ea_repository,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)


def get_repository() -> EaRepositories:
    with EaComManagers() as ea_com_manager:
        ea_repository_file = (
            ea_com_manager.get_ea_repository_file()
        )

        short_name = __get_short_name()

        ea_repository = get_repository_using_file_and_short_name(
            ea_repository_file=ea_repository_file,
            short_name=short_name,
        )

        return ea_repository


def get_repository_using_file_and_short_name(
    ea_repository_file: Files,
    short_name: str,
) -> EaRepositories:
    ea_repository = create_ea_repository(
        ea_repository_file=ea_repository_file,
        short_name=short_name,
    )

    return ea_repository


def get_empty_ea_repository_with_short_name(
    short_name: str,
) -> EaRepositories:
    ea_repository = (
        create_empty_ea_repository(
            short_name=short_name
        )
    )

    return ea_repository


def __get_short_name():
    root = tk.Tk()

    root.withdraw()

    short_name = simpledialog.askstring(
        title="Input",
        prompt="Enter The Repository's Short Name",
    )

    return short_name
