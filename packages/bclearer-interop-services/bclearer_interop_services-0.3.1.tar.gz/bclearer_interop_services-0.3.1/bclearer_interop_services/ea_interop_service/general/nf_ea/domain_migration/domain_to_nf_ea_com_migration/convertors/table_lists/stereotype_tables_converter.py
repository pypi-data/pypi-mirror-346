from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.convertors.tables.standard_stereotypes_converter import (
    convert_standard_stereotype_table_to_stereotypes,
)


def convert_stereotype_tables(
    standard_tables_dictionary: dict,
    stereotype_base_names: list,
    nf_ea_com_dictionary: dict,
) -> dict:
    for (
        stereotype_base_name
    ) in stereotype_base_names:
        nf_ea_com_dictionary = __convert_stereotype_table(
            standard_tables_dictionary=standard_tables_dictionary,
            stereotype_base_name=stereotype_base_name,
            nf_ea_com_dictionary=nf_ea_com_dictionary,
        )

    return nf_ea_com_dictionary


def __convert_stereotype_table(
    standard_tables_dictionary: dict,
    stereotype_base_name: str,
    nf_ea_com_dictionary: dict,
) -> dict:
    nf_ea_com_dictionary = convert_standard_stereotype_table_to_stereotypes(
        standard_table_dictionary=standard_tables_dictionary,
        nf_ea_com_dictionary=nf_ea_com_dictionary,
        input_stereotype_table_name=stereotype_base_name,
    )

    return nf_ea_com_dictionary
