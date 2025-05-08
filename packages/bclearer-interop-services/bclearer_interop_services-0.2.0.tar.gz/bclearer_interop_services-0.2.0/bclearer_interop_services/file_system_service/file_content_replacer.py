from pathlib import Path

from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def replace_string_in_file(
    file_path: Path,
    source_string: str,
    target_string: str,
    file_extension: str,
):
    if not str(file_path).endswith(
        "." + file_extension,
    ):
        return

    file = open(str(file_path))

    file_content = file.read()

    file.close()

    find_count = file_content.count(
        source_string,
    )

    if find_count == 0:
        return

    log_message(
        "count: "
        + str(find_count)
        + " in file: "
        + str(file_path),
    )

    file_content = file_content.replace(
        source_string,
        target_string,
    )

    file = open(str(file_path), "w")

    file.write(file_content)

    file.close()
