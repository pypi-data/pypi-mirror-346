from bclearer_core.constants.standard_constants import (
    DEFAULT_FOREIGN_TABLE_SUFFIX,
    DEFAULT_MASTER_TABLE_SUFFIX,
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    inner_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_connector_types import (
    EaConnectorTypes,
)
from pandas import DataFrame, concat


class EaFullGeneralisationsFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_connectors = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_connectors()
        )

        ea_full_generalisations = ea_connectors.loc[
            ea_connectors[
                NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name
            ]
            == EaConnectorTypes.GENERALIZATION.type_name
        ]

        ea_full_generalisations = dataframe_filter_and_rename(
            dataframe=ea_full_generalisations,
            filter_and_rename_dictionary={
                NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name: "specialisation",
                NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name: "generalisation",
            },
        )

        next_level = self.__get_next_level(
            ea_full_generalisations=ea_full_generalisations
        )

        while (
            next_level.shape[0]
            > ea_full_generalisations.shape[
                0
            ]
        ):
            ea_full_generalisations = (
                next_level
            )

            next_level = self.__get_next_level(
                ea_full_generalisations=ea_full_generalisations
            )

        ea_classifiers = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_classifiers()
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        transitive = dataframe_filter_and_rename(
            dataframe=ea_classifiers,
            filter_and_rename_dictionary={
                nf_uuids_column_name: "generalisation"
            },
        )

        transitive["specialisation"] = (
            transitive["generalisation"]
        )

        transitive = (
            transitive.drop_duplicates()
        )

        ea_full_generalisations = concat(
            [
                ea_full_generalisations,
                transitive,
            ]
        )

        return ea_full_generalisations

    @staticmethod
    def __get_next_level(
        ea_full_generalisations,
    ):
        next_level = inner_merge_dataframes(
            master_dataframe=ea_full_generalisations,
            master_dataframe_key_columns=[
                "specialisation"
            ],
            merge_suffixes=[
                DEFAULT_MASTER_TABLE_SUFFIX,
                DEFAULT_FOREIGN_TABLE_SUFFIX,
            ],
            foreign_key_dataframe=ea_full_generalisations,
            foreign_key_dataframe_fk_columns=[
                "generalisation"
            ],
            foreign_key_dataframe_other_column_rename_dictionary={
                "specialisation": "next_level_specialisation"
            },
        )

        next_level = dataframe_filter_and_rename(
            dataframe=next_level,
            filter_and_rename_dictionary={
                "generalisation": "generalisation",
                "next_level_specialisation": "specialisation",
            },
        )

        next_level = next_level.fillna(
            DEFAULT_NULL_VALUE
        )

        next_level = next_level.loc[
            next_level["specialisation"]
            != DEFAULT_NULL_VALUE
        ]

        next_level = concat(
            [
                ea_full_generalisations,
                next_level,
            ]
        )

        next_level = (
            next_level.drop_duplicates()
        )

        return next_level
