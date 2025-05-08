import gzip


def export_xml_file_as_gzip_compressed_file(
    input_xml_file_path: str,
    output_file_path: str,
) -> None:
    with open(
        input_xml_file_path,
        "rb",
    ) as file_content, gzip.open(
        output_file_path,
        "wb",
    ) as file_writter:
        file_writter.writelines(
            file_content,
        )
