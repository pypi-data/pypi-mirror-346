import importlib
import os

from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)


def get_resource_file(
    resource_namespace: str,
    resource_name: str,
) -> Files:
    module = importlib.import_module(
        name=resource_namespace,
    )

    module_path_string = (
        module.__path__[0]
    )

    resource_full_file_name = (
        os.path.join(
            module_path_string,
            resource_name,
        )
    )

    resource_file = Files(
        absolute_path_string=resource_full_file_name,
    )

    return resource_file
