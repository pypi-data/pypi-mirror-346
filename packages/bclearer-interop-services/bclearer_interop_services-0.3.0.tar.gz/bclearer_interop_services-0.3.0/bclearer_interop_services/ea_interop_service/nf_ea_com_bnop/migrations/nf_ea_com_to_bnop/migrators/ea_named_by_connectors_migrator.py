from bclearer_core.ckids.boro_object_ckids import (
    BoroObjectCkIds,
)
from bclearer_core.common_knowledge.bclearer_matched_ea_objects import (
    BclearerMatchedEaObjects,
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
from bclearer_interop_services.ea_interop_service.nf_ea_com_bnop.migrations.nf_ea_com_to_bnop.filters.ea_connector_filter import (
    filter_connectors_by_stereotype,
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

EXEMPLARS_COLUMN = "exemplars"

NAMED_OBJECT_UML_NAMES_COLUMN = (
    "named_object_uml_names"
)

NAME_UML_NAMES_COLUMN = "name_uml_names"


def migrate_ea_connectors_in_scope_of_naming_pattern(
    nf_ea_com_universe: NfEaComUniverses,
    bnop_repository: BnopRepositories,
):
    named_by_connectors_with_exemplars = __get_named_by_connectors_with_exemplars(
        nf_ea_com_universe=nf_ea_com_universe
    )

    __migrate_named_by_connectors(
        named_by_connectors_with_exemplars=named_by_connectors_with_exemplars,
        bnop_repository=bnop_repository,
    )


def __get_named_by_connectors_with_exemplars(
    nf_ea_com_universe: NfEaComUniverses,
) -> list:
    ea_classifiers = nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
        NfEaComCollectionTypes.EA_CLASSIFIERS
    ]

    ea_connectors = nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
        NfEaComCollectionTypes.EA_CONNECTORS
    ]

    ea_stereotypes = nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
        NfEaComCollectionTypes.EA_STEREOTYPES
    ]

    ea_stereotype_usages = nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
        NfEaComCollectionTypes.STEREOTYPE_USAGE
    ]

    named_by_connectors_dataframe = filter_connectors_by_stereotype(
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usages=ea_stereotype_usages,
        stereotype_ea_guid=BclearerMatchedEaObjects.NAMED_BY_STEREOTYPE.ea_guid,
    )

    name_type_instances_connectors_dataframe = filter_connectors_by_stereotype(
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usages=ea_stereotype_usages,
        stereotype_ea_guid=BclearerMatchedEaObjects.NAME_TYPES_INSTANCES_STEREOTYPE.ea_guid,
    )

    exemplified_by_instances_connectors_dataframe = filter_connectors_by_stereotype(
        ea_connectors=ea_connectors,
        ea_stereotypes=ea_stereotypes,
        ea_stereotype_usages=ea_stereotype_usages,
        stereotype_ea_guid=BclearerMatchedEaObjects.EXEMPLIFIED_BY_STEREOTYPE.ea_guid,
    )

    named_by_name_type_instances_connectors_dataframe = inner_merge_dataframes(
        master_dataframe=named_by_connectors_dataframe,
        master_dataframe_key_columns=[
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
        ],
        merge_suffixes=[
            "_names",
            "_instances",
        ],
        foreign_key_dataframe=name_type_instances_connectors_dataframe,
        foreign_key_dataframe_fk_columns=[
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name: NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
            + "_instances"
        },
    )

    named_by_name_exemplified_by_instances_connectors_dataframe = inner_merge_dataframes(
        master_dataframe=named_by_name_type_instances_connectors_dataframe,
        master_dataframe_key_columns=[
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
            + "_instances"
        ],
        merge_suffixes=[
            "",
            "_exemplified",
        ],
        foreign_key_dataframe=exemplified_by_instances_connectors_dataframe,
        foreign_key_dataframe_fk_columns=[
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name: NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
            + "_exemplified"
        },
    )

    named_by_connectors_with_exemplars_dataframe = inner_merge_dataframes(
        master_dataframe=named_by_name_exemplified_by_instances_connectors_dataframe,
        master_dataframe_key_columns=[
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
            + "_exemplified"
        ],
        merge_suffixes=[
            "",
            "_exemplars",
        ],
        foreign_key_dataframe=ea_classifiers,
        foreign_key_dataframe_fk_columns=[
            NfColumnTypes.NF_UUIDS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: EXEMPLARS_COLUMN
        },
    )

    named_by_connectors_with_exemplars_and_uml_names_dataframe = inner_merge_dataframes(
        master_dataframe=named_by_connectors_with_exemplars_dataframe,
        master_dataframe_key_columns=[
            NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name
        ],
        merge_suffixes=[
            "",
            "_uml_names",
        ],
        foreign_key_dataframe=ea_classifiers,
        foreign_key_dataframe_fk_columns=[
            NfColumnTypes.NF_UUIDS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: NAMED_OBJECT_UML_NAMES_COLUMN
        },
    )

    named_by_connectors_with_exemplars_and_uml_names_dataframe = inner_merge_dataframes(
        master_dataframe=named_by_connectors_with_exemplars_and_uml_names_dataframe,
        master_dataframe_key_columns=[
            NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
        ],
        merge_suffixes=[
            "",
            "_uml_names",
        ],
        foreign_key_dataframe=ea_classifiers,
        foreign_key_dataframe_fk_columns=[
            NfColumnTypes.NF_UUIDS.column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: NAME_UML_NAMES_COLUMN
        },
    )

    named_by_connectors_with_exemplars_and_uml_names_dataframe.fillna(
        value=DEFAULT_NULL_VALUE,
        inplace=True,
    )

    named_by_connectors_with_exemplars = named_by_connectors_with_exemplars_and_uml_names_dataframe.to_dict(
        orient="records"
    )

    return named_by_connectors_with_exemplars


def __migrate_named_by_connectors(
    named_by_connectors_with_exemplars: list,
    bnop_repository: BnopRepositories,
):
    for (
        named_by_connector
    ) in named_by_connectors_with_exemplars:
        __migrate_named_by_connector(
            named_by_connector=named_by_connector,
            bnop_repository=bnop_repository,
        )


def __migrate_named_by_connector(
    named_by_connector: dict,
    bnop_repository: BnopRepositories,
):
    named_by_nf_uuid = named_by_connector[
        NfColumnTypes.NF_UUIDS.column_name
    ]

    named_object_nf_uuid = named_by_connector[
        NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name
    ]

    named_object_uml_name = named_by_connector[
        NAMED_OBJECT_UML_NAMES_COLUMN
    ]

    name_nf_uuid = named_by_connector[
        NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name
    ]

    name_uml_name = named_by_connector[
        NAME_UML_NAMES_COLUMN
    ]

    name_exemplar = named_by_connector[
        EXEMPLARS_COLUMN
    ]

    if (
        named_object_nf_uuid
        in BnopObjects.registry_keyed_on_uuid
    ):
        named_object = BnopObjects.registry_keyed_on_uuid[
            named_object_nf_uuid
        ]
    else:
        named_object = BnopFacades.create_bnop_object(
            object_uuid=named_object_nf_uuid,
            owning_repository_uuid=bnop_repository.uuid,
            presentation_name=named_object_uml_name,
        )

    if (
        name_nf_uuid
        in BnopObjects.registry_keyed_on_uuid
    ):
        name = BnopObjects.registry_keyed_on_uuid[
            name_nf_uuid
        ]
    else:
        name = BnopFacades.create_bnop_name(
            name_uuid=name_nf_uuid,
            owning_repository_uuid=bnop_repository.uuid,
            exemplar_representation=name_exemplar,
            presentation_name=name_uml_name,
        )

    BnopFacades.create_bnop_tuple_from_two_placed_objects(
        tuple_uuid=named_by_nf_uuid,
        placed1_object=named_object,
        placed2_object=name,
        immutable_minor_composition_couple_type_boro_object_ckid=BoroObjectCkIds.NamedBy,
        owning_repository_uuid=bnop_repository.uuid,
    )
