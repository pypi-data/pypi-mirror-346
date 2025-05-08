from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.common_extensions.nf_identity_extender import (
    extend_with_identities,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_diagram_column_types import (
    EaTDiagramColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_diagramobjects_column_types import (
    EaTDiagramobjectsColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_object_column_types import (
    EaTObjectColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.extended_t.extended_t_diagramobjects_column_types import (
    ExtendedTDiagramobjectsColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.extended_t.extended_t_object_column_types import (
    ExtendedTObjectColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_from_list_factory import (
    create_uuid_from_list,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def create_extended_t_diagramobjects_dataframe(
    nf_ea_sql_universe,
    universe_key: str,
) -> DataFrame:
    collection_type_name = (
        EaCollectionTypes.EXTENDED_T_DIAGRAMOBJECTS.collection_name
    )

    log_message(
        message="creating "
        + collection_type_name
        + " dataframe"
    )

    t_diagramobjects_dataframe = nf_ea_sql_universe.ea_tools_session_manager.ea_sql_stage_manager.ea_sql_universe_manager.get_ea_t_table_dataframe(
        ea_repository=nf_ea_sql_universe.ea_repository,
        ea_collection_type=EaCollectionTypes.T_DIAGRAMOBJECTS,
    )

    extended_t_diagramobjects_dataframe = extend_with_identities(
        dataframe=t_diagramobjects_dataframe,
        universe_key=universe_key,
        collection_type_name=collection_type_name,
    )

    extended_t_diagram_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_DIAGRAM
    )

    extended_t_diagramobjects_dataframe = __extend_with_extended_t_diagram_data(
        extended_t_diagramobjects_dataframe=extended_t_diagramobjects_dataframe,
        extended_t_diagram_dataframe=extended_t_diagram_dataframe,
    )

    extended_t_object_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_OBJECT
    )

    extended_t_diagramobjects_dataframe = __extend_with_extended_t_object_data(
        extended_t_diagramobjects_dataframe=extended_t_diagramobjects_dataframe,
        extended_t_object_dataframe=extended_t_object_dataframe,
    )

    extended_t_diagramobjects_dataframe = __extend_with_composite_data(
        extended_t_diagramobjects_dataframe=extended_t_diagramobjects_dataframe
    )

    log_message(
        message="created "
        + collection_type_name
        + " dataframe"
    )

    return extended_t_diagramobjects_dataframe


def __extend_with_extended_t_diagram_data(
    extended_t_diagramobjects_dataframe: DataFrame,
    extended_t_diagram_dataframe: DataFrame,
) -> DataFrame:
    extended_t_diagramobjects_dataframe = left_merge_dataframes(
        master_dataframe=extended_t_diagramobjects_dataframe,
        master_dataframe_key_columns=[
            EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_DIAGRAM_IDS.to_string()
        ],
        merge_suffixes=[
            "_diagramobjects",
            "_diagram",
        ],
        foreign_key_dataframe=extended_t_diagram_dataframe,
        foreign_key_dataframe_fk_columns=[
            EaTDiagramColumnTypes.T_DIAGRAM_IDS.nf_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            EaTDiagramColumnTypes.T_DIAGRAM_EA_GUIDS.nf_column_name: EaTDiagramColumnTypes.T_DIAGRAM_EA_GUIDS.nf_column_name,
            "t_diagram_package_ea_guids": "t_diagram_package_ea_guids",
            "t_diagram_ea_human_readable_names": "t_diagram_ea_human_readable_names",
        },
    )

    return extended_t_diagramobjects_dataframe


def __extend_with_extended_t_object_data(
    extended_t_diagramobjects_dataframe: DataFrame,
    extended_t_object_dataframe: DataFrame,
) -> DataFrame:
    extended_t_diagramobjects_dataframe = left_merge_dataframes(
        master_dataframe=extended_t_diagramobjects_dataframe,
        master_dataframe_key_columns=[
            EaTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_OBJECT_IDS.to_string()
        ],
        merge_suffixes=[
            "_diagramobjects",
            "_object",
        ],
        foreign_key_dataframe=extended_t_object_dataframe,
        foreign_key_dataframe_fk_columns=[
            EaTObjectColumnTypes.T_OBJECT_IDS.nf_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name: EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name,
            ExtendedTObjectColumnTypes.T_OBJECT_EA_HUMAN_READABLE_NAMES.column_name: ExtendedTObjectColumnTypes.T_OBJECT_EA_HUMAN_READABLE_NAMES.column_name,
        },
    )

    return extended_t_diagramobjects_dataframe


def __extend_with_composite_data(
    extended_t_diagramobjects_dataframe: DataFrame,
) -> DataFrame:
    if (
        extended_t_diagramobjects_dataframe.shape[
            0
        ]
        > 0
    ):
        extended_t_diagramobjects_dataframe[
            ExtendedTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_COMPOSITE_EA_GUIDS.to_string()
        ] = extended_t_diagramobjects_dataframe.apply(
            lambda row: __get_composite_ea_guid(
                row
            ),
            axis=1,
        )

    else:
        extended_t_diagramobjects_dataframe[
            ExtendedTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_COMPOSITE_EA_GUIDS.to_string()
        ] = DEFAULT_NULL_VALUE

    extended_t_diagramobjects_dataframe[
        ExtendedTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_EA_HUMAN_READABLE_NAMES.to_string()
    ] = (
        extended_t_diagramobjects_dataframe[
            ExtendedTObjectColumnTypes.T_OBJECT_EA_HUMAN_READABLE_NAMES.column_name
        ]
        + " in "
        + extended_t_diagramobjects_dataframe[
            "t_diagram_ea_human_readable_names"
        ]
    )

    return extended_t_diagramobjects_dataframe


def __get_composite_ea_guid(row) -> str:
    diagram_ea_guid = row[
        EaTDiagramColumnTypes.T_DIAGRAM_EA_GUIDS.nf_column_name
    ]

    object_ea_guid = row[
        EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name
    ]

    composite_ea_guid = (
        create_uuid_from_list(
            objects=[
                diagram_ea_guid,
                object_ea_guid,
            ]
        )
    )

    return composite_ea_guid
