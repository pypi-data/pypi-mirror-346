from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.common_knowledge.package_view_types import (
    PackageViewTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.maps.nf_uuids_to_ea_guids_mappings import (
    NfUuidsToEaGuidsMappings,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.constants.nf_ea_model_constants import (
    DEFAULT_MODEL_NAME,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)


def add_default_migration_package(
    nf_ea_com_dictionary: dict,
    default_model_package_ea_guid: str,
    package_name: str,
    migration_register: type,
):
    ea_packages = nf_ea_com_dictionary[
        NfEaComCollectionTypes.EA_PACKAGES
    ]

    default_package_uuid = (
        create_new_uuid()
    )

    migration_register.default_package_nf_uuid = (
        default_package_uuid
    )

    ea_packages = ea_packages.append(
        {
            NfColumnTypes.NF_UUIDS.column_name: default_package_uuid,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name: DEFAULT_NULL_VALUE,
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: package_name,
            NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name: default_model_package_ea_guid,
            NfEaComColumnTypes.PACKAGES_VIEW_TYPE.column_name: PackageViewTypes.CLASS_VIEW,
        },
        ignore_index=True,
    )

    if (
        not default_model_package_ea_guid
        == DEFAULT_NULL_VALUE
    ):
        NfUuidsToEaGuidsMappings.add_single_map(
            nf_uuid=default_model_package_ea_guid,
            ea_guid=default_model_package_ea_guid,
        )

        ea_packages = ea_packages.append(
            {
                NfColumnTypes.NF_UUIDS.column_name: default_model_package_ea_guid,
                NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name: default_model_package_ea_guid,
                NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: DEFAULT_MODEL_NAME,
            },
            ignore_index=True,
        )

    nf_ea_com_dictionary[
        NfEaComCollectionTypes.EA_PACKAGES
    ] = ea_packages
