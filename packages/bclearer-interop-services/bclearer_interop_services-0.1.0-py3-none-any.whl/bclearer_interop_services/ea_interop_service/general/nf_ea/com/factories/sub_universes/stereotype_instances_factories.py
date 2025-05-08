from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.common.nf_uuid_getter import (
    get_nf_uuid_from_ea_guid,
)
from pandas import DataFrame


class StereotypeInstancesFactories:
    def __init__(
        self,
        nf_ea_com_universe,
        stereotype_ea_guid: str,
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

        self.stereotype_ea_guid = (
            stereotype_ea_guid
        )

    def create(self) -> DataFrame:
        stereotype_usage = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_stereotype_usage()
        )

        stereotype_nf_uuid = get_nf_uuid_from_ea_guid(
            nf_ea_com_universe=self.nf_ea_com_universe,
            ea_guid=self.stereotype_ea_guid,
        )

        stereotype_instances = stereotype_usage.loc[
            stereotype_usage[
                "stereotype_nf_uuids"
            ]
            == stereotype_nf_uuid
        ]

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        stereotype_instances = dataframe_filter_and_rename(
            dataframe=stereotype_instances,
            filter_and_rename_dictionary={
                NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name: nf_uuids_column_name
            },
        )

        return stereotype_instances
