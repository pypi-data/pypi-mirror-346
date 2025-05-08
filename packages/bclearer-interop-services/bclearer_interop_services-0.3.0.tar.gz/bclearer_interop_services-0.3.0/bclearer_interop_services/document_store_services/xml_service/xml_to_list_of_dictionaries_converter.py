import re


def convert_xml_to_list_of_dictionaries(
    input_xml_tag_value_as_string: str,
    xml_tag_member_splitter_value: str,
) -> str:
    xml_tags = re.findall(
        r"<(.*?)>",
        input_xml_tag_value_as_string,
    )

    new_result = list()

    for xml_tag in xml_tags:
        members_dictionary = dict()

        xml_tag_members = xml_tag.split(
            " ",
        )

        for (
            xml_tag_member
        ) in xml_tag_members:
            if xml_tag_member.startswith(
                "xsc",
            ):
                continue

            if xml_tag_member.startswith(
                "xmlns",
            ):
                continue

            xml_tag_member_key_value = xml_tag_member.split(
                xml_tag_member_splitter_value,
            )

            members_dictionary[
                xml_tag_member_key_value[
                    0
                ]
            ] = xml_tag_member_key_value[
                1
            ]

        new_result.append(
            members_dictionary,
        )

    if not new_result:
        return ""

    return str(new_result)
