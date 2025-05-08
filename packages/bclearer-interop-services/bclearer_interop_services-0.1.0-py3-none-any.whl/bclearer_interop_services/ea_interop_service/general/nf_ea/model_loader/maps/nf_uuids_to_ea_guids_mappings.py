from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from pandas import DataFrame


class NfUuidsToEaGuidsMappings:
    __map = dict()

    def __init__(self):
        pass

    @staticmethod
    def map_objects_from_dataframe(
        dataframe: DataFrame,
    ):
        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        ea_guid_column_name = (
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
        )

        new_map = dataframe.set_index(
            nf_uuids_column_name
        ).to_dict()[ea_guid_column_name]

        NfUuidsToEaGuidsMappings.__map.update(
            new_map
        )

    @staticmethod
    def add_single_map(
        nf_uuid: str, ea_guid: str
    ):
        NfUuidsToEaGuidsMappings.__map.update(
            {nf_uuid: ea_guid}
        )

    @staticmethod
    def get_ea_guid(nf_uuid: str):
        ea_guid = NfUuidsToEaGuidsMappings.__map[
            nf_uuid
        ]

        return ea_guid

    @staticmethod
    def get_nf_uuid(ea_guid: str):
        for (
            nf_uuid,
            value,
        ) in (
            NfUuidsToEaGuidsMappings.__map.items()
        ):
            if ea_guid == value:
                return nf_uuid

        return (
            "nf_uuid does not exist for EA GUID "
            + ea_guid
        )

    @staticmethod
    def get_map():
        return (
            NfUuidsToEaGuidsMappings.__map
        )
