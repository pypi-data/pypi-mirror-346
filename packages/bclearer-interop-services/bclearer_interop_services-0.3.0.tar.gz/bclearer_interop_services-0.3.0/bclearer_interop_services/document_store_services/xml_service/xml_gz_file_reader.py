import gzip

from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from lxml import etree


def read_xml_gz_file(
    input_xml_file: Files,
) -> str:
    xml_file_gzip_reader = gzip.open(
        filename=input_xml_file.absolute_path_string,
        mode="r",
    )

    xml_input_file_gzip_content = (
        xml_file_gzip_reader.read()
    )

    xml_file_gzip_reader.close()

    xml_input_file_gzip_content = (
        etree.fromstring(
            xml_input_file_gzip_content,
            parser=etree.XMLParser(
                encoding="UTF-8",
            ),
        )
    )

    return xml_input_file_gzip_content
