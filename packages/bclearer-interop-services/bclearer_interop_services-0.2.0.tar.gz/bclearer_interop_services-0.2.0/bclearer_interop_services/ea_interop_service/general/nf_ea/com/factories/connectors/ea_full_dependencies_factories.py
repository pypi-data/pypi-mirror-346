from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_connector_types import (
    EaConnectorTypes,
)
from pandas import DataFrame


class EaFullDependenciesFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_full_generalisations = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_full_generalisations()
        )

        ea_connectors = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_connectors()
        )

        ea_dependencies = ea_connectors.loc[
            ea_connectors[
                NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name
            ]
            == EaConnectorTypes.DEPENDENCY.type_name
        ]

        ea_dependencies = dataframe_filter_and_rename(
            dataframe=ea_dependencies,
            filter_and_rename_dictionary={
                NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name: "dependent",
                NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name: "provider",
            },
        )

        ea_full_dependencies = left_merge_dataframes(
            master_dataframe=ea_full_generalisations,
            master_dataframe_key_columns=[
                "specialisation"
            ],
            merge_suffixes=[
                "_generalisation",
                "_dependency",
            ],
            foreign_key_dataframe=ea_dependencies,
            foreign_key_dataframe_fk_columns=[
                "provider"
            ],
            foreign_key_dataframe_other_column_rename_dictionary={
                "dependent": "dependent"
            },
        )

        ea_full_dependencies = dataframe_filter_and_rename(
            dataframe=ea_full_dependencies,
            filter_and_rename_dictionary={
                "generalisation": "provider",
                "dependent": "dependent",
            },
        )

        ea_full_dependencies = (
            ea_full_dependencies.fillna(
                DEFAULT_NULL_VALUE
            )
        )

        ea_full_dependencies = (
            ea_full_dependencies.loc[
                ea_full_dependencies[
                    "dependent"
                ]
                != DEFAULT_NULL_VALUE
            ]
        )

        ea_full_dependencies = (
            ea_full_dependencies.drop_duplicates()
        )

        return ea_full_dependencies
