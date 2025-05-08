from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.common.nf_uuid_getter import (
    get_nf_uuid_from_ea_guid,
)
from pandas import DataFrame


class EaFullGeneralisationsOfTypeFactories:
    def __init__(
        self,
        nf_ea_com_universe,
        type_ea_guid: str,
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

        self.type_ea_guid = type_ea_guid

    def create(self) -> DataFrame:
        ea_full_generalisations = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_full_generalisations()
        )

        type_nf_uuid = get_nf_uuid_from_ea_guid(
            nf_ea_com_universe=self.nf_ea_com_universe,
            ea_guid=self.type_ea_guid,
        )

        ea_full_generalisations_of_type = ea_full_generalisations.loc[
            ea_full_generalisations[
                "generalisation"
            ]
            == type_nf_uuid
        ]

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        ea_full_generalisations_of_type = dataframe_filter_and_rename(
            dataframe=ea_full_generalisations_of_type,
            filter_and_rename_dictionary={
                "specialisation": nf_uuids_column_name
            },
        )

        return ea_full_generalisations_of_type
