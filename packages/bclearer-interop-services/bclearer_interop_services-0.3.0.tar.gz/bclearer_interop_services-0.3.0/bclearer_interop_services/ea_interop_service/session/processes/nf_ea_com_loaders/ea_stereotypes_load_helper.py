from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from pandas import DataFrame


def get_ea_stereotype_ex(
    client_nf_uuid: str,
    stereotype_usage_with_names: DataFrame,
) -> str:
    client_stereotypes = stereotype_usage_with_names.loc[
        stereotype_usage_with_names[
            NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name
        ]
        == client_nf_uuid
    ]

    client_stereotypes_as_list = []

    for (
        index,
        client_stereotype_row,
    ) in client_stereotypes.iterrows():
        client_stereotypes_as_list.append(
            client_stereotype_row[
                NfEaComColumnTypes.STEREOTYPE_NAMES.column_name
            ]
        )

    stereotype_ex = ",".join(
        client_stereotypes_as_list
    )

    return stereotype_ex
