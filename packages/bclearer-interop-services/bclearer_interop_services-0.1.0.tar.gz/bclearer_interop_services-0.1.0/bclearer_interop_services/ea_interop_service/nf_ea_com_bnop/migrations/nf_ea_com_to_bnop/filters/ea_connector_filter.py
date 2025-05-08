from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_com_bnop.migrations.nf_ea_com_to_bnop.filters.filter_helpers import (
    get_ea_object_nf_uuid_by_its_ea_guid,
)
from pandas import DataFrame


def filter_connectors_by_stereotype(
    ea_connectors: DataFrame,
    ea_stereotypes: DataFrame,
    ea_stereotype_usages: DataFrame,
    stereotype_ea_guid: str,
) -> DataFrame:
    stereotype_nf_uuid = get_ea_object_nf_uuid_by_its_ea_guid(
        ea_objects=ea_stereotypes,
        stereotype_ea_guid=stereotype_ea_guid,
    )

    ea_stereotype_usages = (
        ea_stereotype_usages[
            ea_stereotype_usages[
                "stereotype_nf_uuids"
            ]
            == stereotype_nf_uuid
        ]
    )

    ea_filtered_connectors = ea_connectors[
        ea_connectors[
            NfColumnTypes.NF_UUIDS.column_name
        ].isin(
            ea_stereotype_usages[
                NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name
            ]
        )
    ]

    return ea_filtered_connectors
