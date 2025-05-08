from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.common_knowledge.package_view_types import (
    PackageViewTypes,
)
from bclearer_interop_services.ea_interop_service.factories.i_dual_package_factory import (
    create_i_dual_package,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.maps.nf_uuids_to_com_objects_mappings import (
    NfUuidsToIDualObjectsMappings,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.packages.i_dual_package import (
    IDualPackage,
)
from pandas import DataFrame
from tqdm import tqdm


def load_ea_packages(
    ea_packages: DataFrame,
):
    ea_guid_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    nf_uuid_column_name = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    name_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
    )

    parent_column_name = (
        NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name
    )

    package_view_type_column_name = (
        NfEaComColumnTypes.PACKAGES_VIEW_TYPE.column_name
    )

    for index, ea_package_row in tqdm(
        ea_packages.iterrows(),
        total=ea_packages.shape[0],
    ):
        ea_package = __load_ea_package(
            nf_uuid=ea_package_row[
                nf_uuid_column_name
            ],
            ea_package_name=ea_package_row[
                name_column_name
            ],
            ea_package_parent_nf_uuid=ea_package_row[
                parent_column_name
            ],
            package_view_type=ea_package_row[
                package_view_type_column_name
            ],
        )

        ea_packages.at[
            index, ea_guid_column_name
        ] = ea_package.package_guid

    return ea_packages


def __load_ea_package(
    nf_uuid: str,
    ea_package_name: str,
    ea_package_parent_nf_uuid: str,
    package_view_type: PackageViewTypes,
) -> IDualPackage:
    ea_package_parent = NfUuidsToIDualObjectsMappings.get_i_dual_package(
        nf_uuid=ea_package_parent_nf_uuid
    )

    if not isinstance(
        ea_package_parent, IDualPackage
    ):
        raise TypeError

    if (
        package_view_type
        == DEFAULT_NULL_VALUE
    ):
        package_view_type = (
            PackageViewTypes.NOT_SET
        )

    ea_package = create_i_dual_package(
        containing_package=ea_package_parent,
        name=ea_package_name,
        package_view_type=package_view_type,
    )

    NfUuidsToIDualObjectsMappings.map_nf_uuid_to_i_dual_package(
        nf_uuid=nf_uuid,
        i_dual_package=ea_package,
    )

    return ea_package
