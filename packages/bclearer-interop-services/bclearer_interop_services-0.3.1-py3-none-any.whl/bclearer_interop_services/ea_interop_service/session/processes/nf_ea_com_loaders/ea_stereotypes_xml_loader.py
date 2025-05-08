from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)
from bclearer_interop_services.ea_interop_service.session.ea_repository_mappers import (
    EaRepositoryMappers,
)


def load_ea_stereotypes_xml(
    ea_repository: EaRepositories,
    xml_string: str,
):
    i_dual_repository = EaRepositoryMappers.get_i_dual_repository(
        ea_repository=ea_repository
    )

    i_dual_repository.custom_command(
        "Repository",
        "ImportRefData",
        xml_string,
    )
