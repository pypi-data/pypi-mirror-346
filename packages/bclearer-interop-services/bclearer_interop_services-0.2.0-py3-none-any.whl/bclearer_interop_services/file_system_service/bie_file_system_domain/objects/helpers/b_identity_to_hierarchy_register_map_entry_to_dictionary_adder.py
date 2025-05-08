from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_files import (
    BIdentityFiles,
)
from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_folders import (
    BIdentityFolders,
)
from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_file_system_objects import (
    HierarchyFileSystemObjects,
)
from bclearer_interop_services.file_system_service.objects.wrappers.hierarchy.hierarchy_folders import (
    HierarchyFolders,
)


def add_b_identity_to_hierarchy_register_map_entry_to_dictionary(
    b_identity_file_system_object_universe_register,
    hierarchy_file_system_object: HierarchyFileSystemObjects,
    file_system_object: FileSystemObjects,
) -> None:
    from bclearer_interop_services.file_system_service.bie_file_system_domain.objects.b_identity_file_system_object_universe_registers import (
        BIdentityFileSystemObjectUniverseRegisters,
    )

    if not isinstance(
        b_identity_file_system_object_universe_register,
        BIdentityFileSystemObjectUniverseRegisters,
    ):
        raise TypeError

    if (
        hierarchy_file_system_object
        == b_identity_file_system_object_universe_register.hierarchy_file_system_object_register.root
    ):
        return

    if isinstance(
        hierarchy_file_system_object,
        HierarchyFolders,
    ) and isinstance(
        file_system_object,
        Folders,
    ):
        b_identity_file_system_object = BIdentityFolders(
            folder=file_system_object,
        )

        b_identity_file_system_object.b_identity_component_immutable_stage_sum = (
            hierarchy_file_system_object.hierarchy_folder_immutable_stage_hash_sum
        )

        b_identity_file_system_object_universe_register.add_b_identity_file_system_object_to_hierarchy_file_system_objects_map_to_register(
            b_identity_file_system_object=b_identity_file_system_object,
            hierarchy_file_system_object=hierarchy_file_system_object,
        )

    elif isinstance(
        file_system_object,
        Files,
    ):
        b_identity_file_system_object = BIdentityFiles(
            file=file_system_object,
        )

        b_identity_file_system_object.b_identity_immutable_stage = (
            file_system_object.file_immutable_stage_hash
        )

        b_identity_file_system_object_universe_register.add_b_identity_file_system_object_to_hierarchy_file_system_objects_map_to_register(
            b_identity_file_system_object=b_identity_file_system_object,
            hierarchy_file_system_object=hierarchy_file_system_object,
        )

    else:
        raise NotImplementedError
