import re

from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)


class StereotypedObjectsUniverseFromGroupFactories:
    def __init__(
        self,
        nf_ea_com_universe,
        stereotype_group_name: str,
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

        self.stereotype_group_name = (
            stereotype_group_name
        )

    def create(self):
        ea_stereotype_groups = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_stereotype_groups()
        )

        object_name_column_name = (
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
        )

        ea_stereotype_group = ea_stereotype_groups.loc[
            ea_stereotype_groups[
                object_name_column_name
            ]
            == self.stereotype_group_name
        ]

        ea_stereotypes = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_stereotypes()
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        stereotype_ea_stereotype_group_column_name = (
            NfEaComColumnTypes.STEREOTYPE_EA_STEREOTYPE_GROUP.column_name
        )

        object_guid_column_name = (
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
        )

        ea_stereotypes_of_group = left_merge_dataframes(
            master_dataframe=ea_stereotype_group,
            master_dataframe_key_columns=[
                nf_uuids_column_name
            ],
            merge_suffixes=[
                "_local",
                "_common",
            ],
            foreign_key_dataframe=ea_stereotypes,
            foreign_key_dataframe_fk_columns=[
                stereotype_ea_stereotype_group_column_name
            ],
            foreign_key_dataframe_other_column_rename_dictionary={
                object_guid_column_name: "stereotype_ea_guids",
                object_name_column_name: NfEaComColumnTypes.STEREOTYPE_NAMES.column_name,
            },
        )

        ea_stereotypes_of_group_dictionary = ea_stereotypes_of_group.to_dict(
            "index"
        )

        for (
            row,
            value_dictionary,
        ) in (
            ea_stereotypes_of_group_dictionary.items()
        ):
            self.__create_table(
                stereotype_ea_guid=value_dictionary[
                    "stereotype_ea_guids"
                ],
                stereotype_name=value_dictionary[
                    NfEaComColumnTypes.STEREOTYPE_NAMES.column_name
                ],
            )

    def __create_table(
        self,
        stereotype_ea_guid: str,
        stereotype_name: str,
    ):
        formatted_stereotype_name = stereotype_name.lower().replace(
            " ", "_"
        )

        formatted_stereotype_name = re.sub(
            r"[^A-Za-z0-9_]",
            "",
            formatted_stereotype_name,
        )

        table_name = (
            formatted_stereotype_name
            + "_stereotyped_objects_universe"
        )

        self.nf_ea_com_universe.nf_ea_com_registry.get_stereotype_instances(
            stereotype_ea_guid=stereotype_ea_guid,
            table_name=table_name,
        )
