from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.common_extensions.nf_identity_extender import (
    extend_with_identities,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_connector_column_types import (
    EaTConnectorColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_diagram_column_types import (
    EaTDiagramColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_diagramlinks_column_types import (
    EaTDiagramlinksColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.extended_t.extended_t_connector_column_types import (
    ExtendedTConnectorColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.extended_t.extended_t_diagramlinks_column_types import (
    ExtendedTDiagramlinksColumnTypes,
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


def create_extended_t_diagramlinks_dataframe(
    nf_ea_sql_universe,
    universe_key: str,
) -> DataFrame:
    collection_type_name = (
        EaCollectionTypes.EXTENDED_T_DIAGRAMLINKS.collection_name
    )

    log_message(
        message="creating "
        + collection_type_name
        + " dataframe"
    )

    t_diagramlinks_dataframe = nf_ea_sql_universe.ea_tools_session_manager.ea_sql_stage_manager.ea_sql_universe_manager.get_ea_t_table_dataframe(
        ea_repository=nf_ea_sql_universe.ea_repository,
        ea_collection_type=EaCollectionTypes.T_DIAGRAMLINKS,
    )

    extended_t_diagramlinks_dataframe = extend_with_identities(
        dataframe=t_diagramlinks_dataframe,
        universe_key=universe_key,
        collection_type_name=collection_type_name,
    )

    extended_t_diagram_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_DIAGRAM
    )

    extended_t_diagramlinks_dataframe = __extend_with_extended_t_diagram_data(
        extended_t_diagramlinks_dataframe=extended_t_diagramlinks_dataframe,
        extended_t_diagram_dataframe=extended_t_diagram_dataframe,
    )

    extended_t_connector_dataframe = nf_ea_sql_universe.get_extended_ea_t_table_dataframe(
        ea_collection_type=EaCollectionTypes.EXTENDED_T_CONNECTOR
    )

    extended_t_diagramlinks_dataframe = __extend_with_extended_t_connector_data(
        extended_t_diagramlinks_dataframe=extended_t_diagramlinks_dataframe,
        extended_t_connector_dataframe=extended_t_connector_dataframe,
    )

    extended_t_diagramlinks_dataframe = __extend_with_composite_data(
        extended_t_diagramlinks_dataframe=extended_t_diagramlinks_dataframe
    )

    log_message(
        message="created "
        + collection_type_name
        + " dataframe"
    )

    return extended_t_diagramlinks_dataframe


def __extend_with_extended_t_diagram_data(
    extended_t_diagramlinks_dataframe: DataFrame,
    extended_t_diagram_dataframe: DataFrame,
) -> DataFrame:
    extended_t_diagramlinks_dataframe = left_merge_dataframes(
        master_dataframe=extended_t_diagramlinks_dataframe,
        master_dataframe_key_columns=[
            EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_DIAGRAM_IDS.to_string()
        ],
        merge_suffixes=[
            "_diagramlinks",
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

    return extended_t_diagramlinks_dataframe


def __extend_with_extended_t_connector_data(
    extended_t_diagramlinks_dataframe: DataFrame,
    extended_t_connector_dataframe: DataFrame,
) -> DataFrame:
    extended_t_diagramlinks_dataframe = left_merge_dataframes(
        master_dataframe=extended_t_diagramlinks_dataframe,
        master_dataframe_key_columns=[
            EaTDiagramlinksColumnTypes.T_DIAGRAMLINKS_CONNECTOR_IDS.to_string()
        ],
        merge_suffixes=[
            "_diagramlinks",
            "_connector",
        ],
        foreign_key_dataframe=extended_t_connector_dataframe,
        foreign_key_dataframe_fk_columns=[
            EaTConnectorColumnTypes.T_CONNECTOR_IDS.nf_column_name
        ],
        foreign_key_dataframe_other_column_rename_dictionary={
            EaTConnectorColumnTypes.T_CONNECTOR_EA_GUIDS.nf_column_name: EaTConnectorColumnTypes.T_CONNECTOR_EA_GUIDS.nf_column_name,
            ExtendedTConnectorColumnTypes.T_CONNECTOR_EA_HUMAN_READABLE_NAMES.column_name: ExtendedTConnectorColumnTypes.T_CONNECTOR_EA_HUMAN_READABLE_NAMES.column_name,
        },
    )

    return extended_t_diagramlinks_dataframe


def __extend_with_composite_data(
    extended_t_diagramlinks_dataframe: DataFrame,
) -> DataFrame:
    if (
        extended_t_diagramlinks_dataframe.shape[
            0
        ]
        > 0
    ):
        extended_t_diagramlinks_dataframe[
            ExtendedTDiagramlinksColumnTypes.T_DIAGRAMLINKS_COMPOSITE_EA_GUIDS.to_string()
        ] = extended_t_diagramlinks_dataframe.apply(
            lambda row: __get_composite_ea_guid(
                row
            ),
            axis=1,
        )

    else:
        extended_t_diagramlinks_dataframe[
            ExtendedTDiagramlinksColumnTypes.T_DIAGRAMLINKS_COMPOSITE_EA_GUIDS.to_string()
        ] = DEFAULT_NULL_VALUE

    extended_t_diagramlinks_dataframe[
        ExtendedTDiagramlinksColumnTypes.T_DIAGRAMLINKS_EA_HUMAN_READABLE_NAMES.to_string()
    ] = (
        extended_t_diagramlinks_dataframe[
            ExtendedTConnectorColumnTypes.T_CONNECTOR_EA_HUMAN_READABLE_NAMES.column_name
        ]
        + " in "
        + extended_t_diagramlinks_dataframe[
            "t_diagram_ea_human_readable_names"
        ]
    )

    return extended_t_diagramlinks_dataframe


def __get_composite_ea_guid(row) -> str:
    diagram_ea_guid = row[
        EaTDiagramColumnTypes.T_DIAGRAM_EA_GUIDS.nf_column_name
    ]

    connector_ea_guid = row[
        EaTConnectorColumnTypes.T_CONNECTOR_EA_GUIDS.nf_column_name
    ]

    composite_ea_guid = (
        create_uuid_from_list(
            objects=[
                diagram_ea_guid,
                connector_ea_guid,
            ]
        )
    )

    return composite_ea_guid
