from bclearer_core.ckids.boro_object_ckids import (
    BoroObjectCkIds,
)
from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    inner_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_connector_types import (
    EaConnectorTypes,
)
from bnop.bnop_facades import (
    BnopFacades,
)
from bnop.core.object_model.bnop_repositories import (
    BnopRepositories,
)
from bnop.core.object_model.objects.bnop_objects import (
    BnopObjects,
)

INSTANCE_UML_NAMES_COLUMN = (
    "instance_uml_names"
)

TYPE_UML_NAMES_COLUMN = "type_uml_names"


def migrate_ea_connectors_in_scope_of_typing_pattern(
    nf_ea_com_universe: NfEaComUniverses,
    bnop_repository: BnopRepositories,
):
    typing_ea_connectors = __get_typing_connectors(
        nf_ea_com_universe=nf_ea_com_universe
    )

    __migrate_typing_connectors(
        ea_connectors=typing_ea_connectors,
        bnop_repository=bnop_repository,
    )


def __get_typing_connectors(
    nf_ea_com_universe: NfEaComUniverses,
) -> list:
    ea_connectors = nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
        NfEaComCollectionTypes.EA_CONNECTORS
    ]

    ea_classifiers = nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
        NfEaComCollectionTypes.EA_CLASSIFIERS
    ]

    typing_ea_connectors = ea_connectors[
        ea_connectors[
            NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name
        ]
        == EaConnectorTypes.DEPENDENCY.type_name
    ]

    typing_ea_connectors_with_uml_names_dataframe = inner_merge_dataframes(
        master_dataframe=typing_ea_connectors,
        master_dataframe_key_columns=[
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name
        ],
        merge_suffixes=[
            "",
            "_type_uml_names",
        ],
        foreign_key_dataframe=ea_classifiers,
        foreign_key_dataframe_fk_columns=[
            NfColumnTypes.NF_UUIDS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: TYPE_UML_NAMES_COLUMN
        },
    )

    typing_ea_connectors_with_uml_names_dataframe = inner_merge_dataframes(
        master_dataframe=typing_ea_connectors_with_uml_names_dataframe,
        master_dataframe_key_columns=[
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
        ],
        merge_suffixes=[
            "",
            "_instance_uml_names",
        ],
        foreign_key_dataframe=ea_classifiers,
        foreign_key_dataframe_fk_columns=[
            NfColumnTypes.NF_UUIDS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: INSTANCE_UML_NAMES_COLUMN
        },
    )

    typing_ea_connectors_with_uml_names_dataframe.fillna(
        value=DEFAULT_NULL_VALUE,
        inplace=True,
    )

    typing_ea_connectors_with_uml_names = typing_ea_connectors_with_uml_names_dataframe.to_dict(
        orient="records"
    )

    return typing_ea_connectors_with_uml_names


def __migrate_typing_connectors(
    ea_connectors: list,
    bnop_repository: BnopRepositories,
):
    for ea_connector in ea_connectors:
        __migrate_typing_connector(
            ea_connector=ea_connector,
            bnop_repository=bnop_repository,
        )


def __migrate_typing_connector(
    bnop_repository: BnopRepositories,
    ea_connector: dict,
):
    typing_tuple_nf_uuid = ea_connector[
        NfColumnTypes.NF_UUIDS.column_name
    ]

    instance_nf_uuid = ea_connector[
        NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
    ]

    instance_uml_name = ea_connector[
        INSTANCE_UML_NAMES_COLUMN
    ]

    type_nf_uuid = ea_connector[
        NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name
    ]

    type_uml_name = ea_connector[
        TYPE_UML_NAMES_COLUMN
    ]

    if (
        instance_nf_uuid
        in BnopObjects.registry_keyed_on_uuid
    ):
        bnop_instance = BnopObjects.registry_keyed_on_uuid[
            instance_nf_uuid
        ]
    else:
        bnop_instance = BnopFacades.create_bnop_object(
            object_uuid=instance_nf_uuid,
            owning_repository_uuid=bnop_repository.uuid,
            presentation_name=instance_uml_name,
        )

    if (
        type_nf_uuid
        in BnopObjects.registry_keyed_on_uuid
    ):
        bnop_type = BnopObjects.registry_keyed_on_uuid[
            type_nf_uuid
        ]
    else:
        bnop_type = BnopFacades.create_bnop_type(
            type_uuid=type_nf_uuid,
            owning_repository_uuid=bnop_repository.uuid,
            presentation_name=type_uml_name,
        )

    BnopFacades.create_bnop_tuple_from_two_placed_objects(
        tuple_uuid=typing_tuple_nf_uuid,
        placed1_object=bnop_type,
        placed2_object=bnop_instance,
        immutable_minor_composition_couple_type_boro_object_ckid=BoroObjectCkIds.TypesInstances,
        owning_repository_uuid=bnop_repository.uuid,
    )
