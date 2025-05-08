from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.convertors.tables.standard_stereotype_usage_converter import (
    convert_standard_stereotype_usage_table_to_stereotype_usage,
)


def convert_stereotype_usage_tables(
    standard_tables_dictionary: dict,
    stereotype_usage_base_names: list,
    nf_ea_com_dictionary: dict,
) -> dict:
    for (
        stereotype_usage_base_name
    ) in stereotype_usage_base_names:
        nf_ea_com_dictionary = __convert_stereotype_usage_table(
            standard_tables_dictionary=standard_tables_dictionary,
            stereotype_usage_base_name=stereotype_usage_base_name,
            nf_ea_com_dictionary=nf_ea_com_dictionary,
        )

    return nf_ea_com_dictionary


def __convert_stereotype_usage_table(
    standard_tables_dictionary: dict,
    stereotype_usage_base_name: str,
    nf_ea_com_dictionary: dict,
) -> dict:
    nf_ea_com_dictionary = convert_standard_stereotype_usage_table_to_stereotype_usage(
        standard_table_dictionary=standard_tables_dictionary,
        nf_ea_com_dictionary=nf_ea_com_dictionary,
        input_stereotype_usage_table_name=stereotype_usage_base_name,
    )

    return nf_ea_com_dictionary
