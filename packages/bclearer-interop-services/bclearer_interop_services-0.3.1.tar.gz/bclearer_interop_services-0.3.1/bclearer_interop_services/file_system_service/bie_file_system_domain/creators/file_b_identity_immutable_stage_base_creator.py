import os.path

from bclearer_orchestration_services.identification_services.b_identity_service.b_identity_creators.b_identity_base_from_bytes_creator import (
    create_b_identity_base_from_bytes,
)


def create_file_b_identity_immutable_stage_base(
    file,
) -> int:
    from bclearer_interop_services.file_system_service.objects.files import (
        Files,
    )

    if not isinstance(file, Files):
        raise TypeError

    if not os.path.exists(
        file.absolute_path_string,
    ):
        return None

    with open(
        file.absolute_path_string,
        mode="rb",
    ) as python_native_file:
        file_content_as_bytes = (
            python_native_file.read()
        )

    hash_as_integer = create_b_identity_base_from_bytes(
        input_bytes=file_content_as_bytes,
    )

    return hash_as_integer
