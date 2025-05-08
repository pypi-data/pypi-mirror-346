from bclearer_interop_services.ea_interop_service.i_dual_objects.collections.i_dual_collection import (
    IDualCollection,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.i_dual_repository import (
    IDualRepository,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.packages.i_dual_package import (
    IDualPackage,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.projects.i_dual_project import (
    IDualProject,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_element_types import (
    EaElementTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)
from bclearer_interop_services.ea_interop_service.session.ea_repository_mappers import (
    EaRepositoryMappers,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def load_ea_xml_file_to_ea_repository(
    ea_repository: EaRepositories,
    load_xml_file_full_path: str,
):
    log_message(
        message="Loading "
        + load_xml_file_full_path
        + " to EA repository"
    )

    i_dual_repository = EaRepositoryMappers.get_i_dual_repository(
        ea_repository
    )

    load_package_ea_guid = (
        __get_load_package_ea_guid(
            i_dual_repository
        )
    )

    project_interface = (
        i_dual_repository.get_project_interface()
    )

    if not isinstance(
        project_interface, IDualProject
    ):
        raise TypeError

    project_interface.import_package_xmi(
        package_guid=load_package_ea_guid,
        filename=load_xml_file_full_path,
        import_diagrams=-1,
        strip_guid=0,
    )


def __get_load_package_ea_guid(
    i_dual_repository: IDualRepository,
) -> str:
    top_level_model = (
        i_dual_repository.models.get_at(
            0
        )
    )

    model_packages = (
        top_level_model.packages
    )

    if model_packages.count == 0:
        load_package_ea_guid = __create_load_package_and_get_its_ea_guid(
            model_packages=model_packages
        )
    else:
        top_level_package = top_level_model.packages.get_at(
            0
        )

        load_package_ea_guid = (
            top_level_package.package_guid
        )

    return load_package_ea_guid


def __create_load_package_and_get_its_ea_guid(
    model_packages: IDualCollection,
) -> str:
    default_import_package = IDualPackage(
        model_packages.add_new(
            ea_object_name="Default Import Package",
            ea_object_type=EaElementTypes.PACKAGE.type_name,
        )
    )

    default_import_package.update()

    load_package_ea_guid = (
        default_import_package.package_guid
    )

    log_message(
        message="Default import package was added to the model."
    )

    return load_package_ea_guid
