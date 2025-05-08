from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from pandas import DataFrame, concat


class EaNearestPackagesFactories:
    def __init__(
        self, nf_ea_com_universe
    ):
        self.nf_ea_com_universe = (
            nf_ea_com_universe
        )

    def create(self) -> DataFrame:
        child_column_name = (
            NfColumnTypes.NF_UUIDS.column_name
        )

        parent_column_name = (
            NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name
        )

        object_type_column_name = (
            NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name
        )

        ea_classifiers = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_classifiers()
        )

        ea_classifier_nearest_packages = dataframe_filter_and_rename(
            dataframe=ea_classifiers,
            filter_and_rename_dictionary={
                child_column_name: "child",
                parent_column_name: "parent",
                object_type_column_name: "object_type",
            },
        )

        ea_packages = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_packages()
        )

        ea_package_nearest_packages = dataframe_filter_and_rename(
            dataframe=ea_packages,
            filter_and_rename_dictionary={
                child_column_name: "child",
                parent_column_name: "parent",
                object_type_column_name: "object_type",
            },
        )

        ea_diagrams = (
            self.nf_ea_com_universe.nf_ea_com_registry.get_ea_diagrams()
        )

        ea_diagram_nearest_packages = dataframe_filter_and_rename(
            dataframe=ea_diagrams,
            filter_and_rename_dictionary={
                child_column_name: "child",
                parent_column_name: "parent",
                object_type_column_name: "object_type",
            },
        )

        ea_nearest_packages = concat(
            [
                ea_classifier_nearest_packages,
                ea_package_nearest_packages,
                ea_diagram_nearest_packages,
            ]
        )

        ea_nearest_packages = (
            ea_nearest_packages.fillna(
                DEFAULT_NULL_VALUE
            )
        )

        return ea_nearest_packages
