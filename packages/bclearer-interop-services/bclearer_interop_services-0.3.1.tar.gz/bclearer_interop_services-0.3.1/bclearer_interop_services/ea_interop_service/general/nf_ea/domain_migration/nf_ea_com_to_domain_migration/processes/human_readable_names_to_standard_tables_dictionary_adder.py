from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.nf_domains.standard_connector_table_column_types import (
    StandardConnectorTableColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.nf_domains.standard_object_table_column_types import (
    StandardObjectTableColumnTypes,
)


def add_human_readable_names_to_standard_tables_dictionary(
    standard_tables_dictionary: dict,
) -> dict:
    standard_tables_dictionary = __add_package_names_to_objects(
        standard_tables_dictionary=standard_tables_dictionary,
        collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
    )

    standard_tables_dictionary = __add_package_names_to_objects(
        standard_tables_dictionary=standard_tables_dictionary,
        collection_type=NfEaComCollectionTypes.EA_PACKAGES,
    )

    standard_tables_dictionary = __add_object_names_to_connectors(
        standard_tables_dictionary=standard_tables_dictionary,
        place_nf_uuids_column_type=StandardConnectorTableColumnTypes.SUPPLIER_PLACE_1_NF_UUIDS,
        place_uml_names_column_type=StandardConnectorTableColumnTypes.SUPPLIER_PLACE_1_UML_NAMES,
    )

    standard_tables_dictionary = __add_object_names_to_connectors(
        standard_tables_dictionary=standard_tables_dictionary,
        place_nf_uuids_column_type=StandardConnectorTableColumnTypes.CLIENT_PLACE_2_NF_UUIDS,
        place_uml_names_column_type=StandardConnectorTableColumnTypes.CLIENT_PLACE_2_UML_NAMES,
    )

    return standard_tables_dictionary


def __add_package_names_to_objects(
    standard_tables_dictionary: dict,
    collection_type: NfEaComCollectionTypes,
) -> dict:
    objects_dataframe = standard_tables_dictionary[
        collection_type.collection_name
    ]

    packages_dataframe = standard_tables_dictionary[
        NfEaComCollectionTypes.EA_PACKAGES.collection_name
    ]

    objects_with_package_names_dataframe = left_merge_dataframes(
        master_dataframe=objects_dataframe,
        master_dataframe_key_columns=[
            StandardObjectTableColumnTypes.PARENT_PACKAGE_NF_UUIDS.column_name
        ],
        merge_suffixes=[
            "_master",
            "_packages",
        ],
        foreign_key_dataframe=packages_dataframe,
        foreign_key_dataframe_fk_columns=[
            StandardObjectTableColumnTypes.NF_UUIDS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            StandardObjectTableColumnTypes.UML_OBJECT_NAMES.column_name: StandardObjectTableColumnTypes.PARENT_PACKAGE_UML_NAMES.column_name
        },
    )

    objects_with_package_names_dataframe.fillna(
        DEFAULT_NULL_VALUE
    )

    standard_tables_dictionary[
        collection_type.collection_name
    ] = objects_with_package_names_dataframe

    return standard_tables_dictionary


def __add_object_names_to_connectors(
    standard_tables_dictionary: dict,
    place_nf_uuids_column_type: StandardConnectorTableColumnTypes,
    place_uml_names_column_type: StandardConnectorTableColumnTypes,
) -> dict:
    objects_dataframe = standard_tables_dictionary[
        NfEaComCollectionTypes.EA_CLASSIFIERS.collection_name
    ]

    connectors_dataframe = standard_tables_dictionary[
        NfEaComCollectionTypes.EA_CONNECTORS.collection_name
    ]

    connectors_with_place_names_dataframe = left_merge_dataframes(
        master_dataframe=connectors_dataframe,
        master_dataframe_key_columns=[
            place_nf_uuids_column_type.column_name
        ],
        merge_suffixes=[
            "_connectors",
            "_objects",
        ],
        foreign_key_dataframe=objects_dataframe,
        foreign_key_dataframe_fk_columns=[
            StandardObjectTableColumnTypes.NF_UUIDS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            StandardObjectTableColumnTypes.UML_OBJECT_NAMES.column_name: place_uml_names_column_type.column_name
        },
    )

    connectors_with_place_names_dataframe.fillna(
        DEFAULT_NULL_VALUE
    )

    standard_tables_dictionary[
        NfEaComCollectionTypes.EA_CONNECTORS.collection_name
    ] = connectors_with_place_names_dataframe

    return standard_tables_dictionary
