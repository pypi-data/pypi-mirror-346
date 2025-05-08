from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)


def get_nf_uuid_from_ea_guid(
    nf_ea_com_universe, ea_guid: str
) -> str:
    thin_ea_explicit_objects = (
        nf_ea_com_universe.nf_ea_com_registry.get_thin_ea_explicit_objects()
    )

    nf_uuids_column_name = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    object_guid_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    thin_ea_explicit_object = (
        thin_ea_explicit_objects.loc[
            thin_ea_explicit_objects[
                object_guid_column_name
            ]
            == ea_guid
        ]
    )

    if (
        thin_ea_explicit_object.shape[0]
        == 0
    ):
        return ""

    nf_uuid = (
        thin_ea_explicit_object.iloc[0][
            nf_uuids_column_name
        ]
    )

    return nf_uuid
