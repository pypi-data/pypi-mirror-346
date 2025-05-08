from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.common_extensions.nf_identity_extender import (
    extend_with_identities,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_stereotypes_column_types import (
    EaTStereotypesColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def create_extended_t_stereotypes_dataframe(
    nf_ea_sql_universe,
    universe_key: str,
) -> DataFrame:
    log_message(
        message="creating extended t_stereotypes dataframe"
    )

    t_stereotypes_dataframe = nf_ea_sql_universe.ea_tools_session_manager.ea_sql_stage_manager.ea_sql_universe_manager.get_ea_t_table_dataframe(
        ea_repository=nf_ea_sql_universe.ea_repository,
        ea_collection_type=EaCollectionTypes.T_STEREOTYPES,
    )

    extended_t_stereotypes_dataframe = extend_with_identities(
        dataframe=t_stereotypes_dataframe,
        universe_key=universe_key,
        collection_type_name=EaCollectionTypes.EXTENDED_T_STEREOTYPES.collection_name,
    )

    extended_t_stereotypes_dataframe = __extend_with_stereotype_groups(
        extended_t_stereotypes_dataframe=extended_t_stereotypes_dataframe
    )

    log_message(
        message="created extended t_stereotypes dataframe"
    )

    return (
        extended_t_stereotypes_dataframe
    )


def __extend_with_stereotype_groups(
    extended_t_stereotypes_dataframe: DataFrame,
) -> DataFrame:
    extended_t_stereotypes_dataframe = (
        extended_t_stereotypes_dataframe.copy()
    )

    t_stereotypes_styles_column_name = (
        EaTStereotypesColumnTypes.T_STEREOTYPES_STYLES.nf_column_name
    )

    extended_t_stereotypes_dataframe = __add_column_from_style(
        dataframe=extended_t_stereotypes_dataframe,
        from_column_name=t_stereotypes_styles_column_name,
        to_column_name="stereotype_group_names",
        prefix='groupname="',
        suffix='"',
    )

    extended_t_stereotypes_dataframe = __add_column_from_style(
        dataframe=extended_t_stereotypes_dataframe,
        from_column_name=t_stereotypes_styles_column_name,
        to_column_name="stereotype_style_fills",
        prefix='fill="',
        suffix='"',
    )

    extended_t_stereotypes_dataframe = __add_column_from_style(
        dataframe=extended_t_stereotypes_dataframe,
        from_column_name=t_stereotypes_styles_column_name,
        to_column_name="stereotype_style_texts",
        prefix='text="',
        suffix='"',
    )

    extended_t_stereotypes_dataframe = __add_column_from_style(
        dataframe=extended_t_stereotypes_dataframe,
        from_column_name=t_stereotypes_styles_column_name,
        to_column_name="stereotype_style_borders",
        prefix='border="',
        suffix='"',
    )

    extended_t_stereotypes_dataframe = __add_column_from_style(
        dataframe=extended_t_stereotypes_dataframe,
        from_column_name=t_stereotypes_styles_column_name,
        to_column_name="stereotype_style_types",
        prefix='type="',
        suffix='"',
    )

    extended_t_stereotypes_dataframe = __add_column_from_style(
        dataframe=extended_t_stereotypes_dataframe,
        from_column_name=t_stereotypes_styles_column_name,
        to_column_name="stereotype_style_fonts",
        prefix='Font="',
        suffix='"',
    )

    return (
        extended_t_stereotypes_dataframe
    )


def __add_column_from_style(
    dataframe,
    from_column_name,
    to_column_name,
    prefix,
    suffix,
):
    dataframe[
        to_column_name
    ] = dataframe[
        from_column_name
    ].apply(
        lambda string: __extract_value_from_string(
            string=string,
            prefix=prefix,
            suffix=suffix,
        )
    )

    return dataframe


def __extract_value_from_string(
    string: str,
    prefix: str,
    suffix: str,
) -> str:
    prefix_position = string.find(
        prefix
    )

    if prefix_position < 0:
        return DEFAULT_NULL_VALUE

    start_position = (
        prefix_position + len(prefix)
    )

    end_position = string.find(
        suffix, start_position
    )

    value = string[
        start_position:end_position
    ]

    return value
