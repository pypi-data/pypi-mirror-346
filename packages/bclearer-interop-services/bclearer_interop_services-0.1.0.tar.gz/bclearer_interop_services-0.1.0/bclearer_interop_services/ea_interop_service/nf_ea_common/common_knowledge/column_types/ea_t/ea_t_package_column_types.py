from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_column_types import (
    EaTColumnTypes,
)


@unique
class EaTPackageColumnTypes(
    EaTColumnTypes
):
    T_PACKAGE_EA_GUIDS = auto()
    T_PACKAGE_IDS = auto()
    T_PACKAGE_NAMES = auto()
    T_PACKAGE_PARENT_IDS = auto()
    T_PACKAGE_PACKAGE_FLAGS = auto()

    def __column_name(self) -> str:
        column_name = (
            column_name_mapping[self]
        )

        return column_name

    def __nf_column_name(self) -> str:
        nf_column_name = (
            nf_column_name_mapping[self]
        )

        return nf_column_name

    column_name = property(
        fget=__column_name
    )

    nf_column_name = property(
        fget=__nf_column_name
    )


column_name_mapping = {
    EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS: "ea_guid",
    EaTPackageColumnTypes.T_PACKAGE_IDS: "Package_ID",
    EaTPackageColumnTypes.T_PACKAGE_NAMES: "Name",
    EaTPackageColumnTypes.T_PACKAGE_PARENT_IDS: "Parent_ID",
    EaTPackageColumnTypes.T_PACKAGE_PACKAGE_FLAGS: "PackageFlags",
}


nf_column_name_mapping = {
    EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS: "t_package_ea_guids",
    EaTPackageColumnTypes.T_PACKAGE_IDS: "t_package_ids",
    EaTPackageColumnTypes.T_PACKAGE_NAMES: "t_package_names",
    EaTPackageColumnTypes.T_PACKAGE_PARENT_IDS: "t_parent_ids",
    EaTPackageColumnTypes.T_PACKAGE_PACKAGE_FLAGS: "t_package_flags",
}
