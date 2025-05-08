def read_file_content_as_string(
    file_path: str,
) -> str:
    with open(
        file_path,
    ) as current_file:
        file_content_as_string = (
            current_file.read()
        )

    return file_content_as_string
