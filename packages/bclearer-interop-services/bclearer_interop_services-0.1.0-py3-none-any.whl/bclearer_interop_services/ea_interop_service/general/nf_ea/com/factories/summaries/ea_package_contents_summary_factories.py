from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_from_list_factory import (
    create_uuid_from_list,
)
from pandas import (
    DataFrame,
    crosstab,
    merge,
)


class EaPackageContentsSummaryFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        ea_package_contents_summary = (
            self.create_ea_package_contents_summary()
        )

        ea_package_contents_summary = self.__add_ea_package_contents_counts(
            ea_package_contents_summary=ea_package_contents_summary
        )

        ea_package_contents_summary = self.__add_hash(
            ea_package_contents_summary=ea_package_contents_summary
        )

        ea_package_contents_summary = self.__reorder(
            ea_package_contents_summary=ea_package_contents_summary
        )

        return (
            ea_package_contents_summary
        )

    def create_ea_package_contents_summary(
        self,
    ) -> DataFrame:
        ea_package_contents_summary = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_packages()
        )

        items = [
            NfColumnTypes.NF_UUIDS.column_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name,
            "ea_package_path",
            "parent_package_ea_guid",
            "parent_package_name",
        ]

        ea_package_contents_summary = ea_package_contents_summary.filter(
            items=items
        )

        return (
            ea_package_contents_summary
        )

    def __add_ea_package_contents_counts(
        self,
        ea_package_contents_summary: DataFrame,
    ) -> DataFrame:
        ea_full_packages = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_full_packages()
        )

        ea_package_full_contents_counts = self.__create_contents_counts(
            ea_parent_child_packages=ea_full_packages,
            prefix="full",
        )

        ea_full_nearest_packages = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_nearest_packages()
        )

        ea_package_nearest_contents_counts = self.__create_contents_counts(
            ea_parent_child_packages=ea_full_nearest_packages,
            prefix="nearest",
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        ea_package_contents_counts = merge(
            left=ea_package_nearest_contents_counts,
            right=ea_package_full_contents_counts,
            on=nf_uuids_column_name,
        )

        columns_to_add_dictionary = {}

        for (
            column
        ) in ea_package_contents_counts:
            columns_to_add_dictionary[
                column
            ] = column

        del columns_to_add_dictionary[
            nf_uuids_column_name
        ]

        ea_package_contents_summary = left_merge_dataframes(
            master_dataframe=ea_package_contents_summary,
            master_dataframe_key_columns=[
                nf_uuids_column_name
            ],
            merge_suffixes=[
                "_summary",
                "_counts",
            ],
            foreign_key_dataframe=ea_package_contents_counts,
            foreign_key_dataframe_fk_columns=[
                nf_uuids_column_name
            ],
            foreign_key_dataframe_other_column_rename_dictionary=columns_to_add_dictionary,
        )

        ea_package_contents_summary = ea_package_contents_summary.fillna(
            0
        )

        return (
            ea_package_contents_summary
        )

    @staticmethod
    def __create_contents_counts(
        ea_parent_child_packages: DataFrame,
        prefix: str,
    ) -> DataFrame:
        ea_package_contents_counts = crosstab(
            ea_parent_child_packages[
                "parent"
            ],
            ea_parent_child_packages[
                "object_type"
            ],
        )

        nf_uuids_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        column_rename_dictionary = {
            "parent": nf_uuids_column_name
        }

        for (
            column
        ) in ea_package_contents_counts:
            column_rename_dictionary[
                column
            ] = (
                "type_"
                + prefix
                + "_"
                + column
            )

        ea_package_contents_counts = (
            ea_package_contents_counts.reset_index()
        )

        ea_package_contents_counts = ea_package_contents_counts.rename(
            columns=column_rename_dictionary
        )

        return (
            ea_package_contents_counts
        )

    @staticmethod
    def __add_hash(
        ea_package_contents_summary: DataFrame,
    ) -> DataFrame:
        ea_package_contents_summary[
            "immutable_hash"
        ] = ea_package_contents_summary.apply(
            lambda row: EaPackageContentsSummaryFactories.__get_composite_ea_guid(
                row
            ),
            axis=1,
        )

        return (
            ea_package_contents_summary
        )

    @staticmethod
    def __get_composite_ea_guid(
        row,
    ) -> str:
        package_ea_guid = row[
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
        ]

        package_name = row[
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
        ]

        objects = [
            package_ea_guid,
            package_name,
        ]

        row_index = row.index

        ordered_row_index = (
            row_index.sort_values()
        )

        for (
            column_name
        ) in ordered_row_index:
            if column_name.startswith(
                "type_full"
            ):
                type_full_count = row[
                    column_name
                ]

                if type_full_count > 0:
                    objects.append(
                        column_name
                        + "="
                        + str(
                            type_full_count
                        )
                    )

        composite_ea_guid = (
            create_uuid_from_list(
                objects=objects
            )
        )

        return composite_ea_guid

    @staticmethod
    def __reorder(
        ea_package_contents_summary: DataFrame,
    ) -> DataFrame:
        ea_package_contents_summary = ea_package_contents_summary.sort_values(
            "ea_package_path"
        )

        return (
            ea_package_contents_summary
        )
