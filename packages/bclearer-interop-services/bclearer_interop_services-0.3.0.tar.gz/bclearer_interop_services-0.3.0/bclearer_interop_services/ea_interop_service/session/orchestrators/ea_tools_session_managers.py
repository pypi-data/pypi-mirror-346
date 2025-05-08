from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)
from bclearer_interop_services.ea_interop_service.session.ea_repository_mappers import (
    EaRepositoryMappers,
)
from bclearer_interop_services.ea_interop_service.session.ea_tools_session_service.ea_repository_factory import (
    get_empty_ea_repository_with_short_name,
    get_repository,
    get_repository_using_file_and_short_name,
)
from bclearer_interop_services.ea_interop_service.session.nf_ea_com_endpoint.orchestrators.endpoint_managers.ea_sql_stage_managers import (
    EaSqlStageManagers,
)
from bclearer_interop_services.ea_interop_service.session.nf_ea_com_endpoint.orchestrators.endpoint_managers.nf_ea_com_endpoint_managers import (
    NfEaComEndpointManagers,
)
from bclearer_interop_services.ea_interop_service.session.nf_ea_com_endpoint.orchestrators.endpoint_managers.nf_ea_sql_stage_managers import (
    NfEaSqlStageManagers,
)
from bclearer_interop_services.ea_interop_service.session.processes.nf_ea_com_loaders.ea_attributes_loader import (
    load_ea_attributes,
)
from bclearer_interop_services.ea_interop_service.session.processes.nf_ea_com_loaders.ea_classifiers_loader import (
    load_ea_classifiers,
)
from bclearer_interop_services.ea_interop_service.session.processes.nf_ea_com_loaders.ea_connectors_loader import (
    load_ea_connectors,
)
from bclearer_interop_services.ea_interop_service.session.processes.nf_ea_com_loaders.ea_packages_loader import (
    load_ea_packages,
)
from bclearer_interop_services.ea_interop_service.session.processes.nf_ea_com_loaders.ea_proxy_connectors_loader import (
    load_ea_proxy_connectors,
)
from bclearer_interop_services.ea_interop_service.session.processes.nf_ea_com_loaders.ea_stereotypes_loader import (
    load_ea_stereotypes,
)
from bclearer_interop_services.ea_interop_service.session.processes.nf_ea_com_loaders.ea_stereotypes_xml_loader import (
    load_ea_stereotypes_xml,
)
from bclearer_interop_services.ea_interop_service.session.processes.reorderers.ea_attributes_reorderer import (
    reorder_ea_attributes,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from pandas import DataFrame


class EaToolsSessionManagers:
    def __init__(self):
        self.ea_sql_stage_manager = (
            EaSqlStageManagers()
        )

        self.nf_ea_sql_stage_manager = (
            NfEaSqlStageManagers(self)
        )

        self.nf_ea_com_endpoint_manager = NfEaComEndpointManagers(
            self
        )

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type,
        exception_value,
        traceback,
    ):
        EaRepositoryMappers.close_all_ea_repositories()

        self.nf_ea_com_endpoint_manager.close()

    @staticmethod
    def create_ea_repository() -> (
        EaRepositories
    ):
        ea_repository = get_repository()

        return ea_repository

    @staticmethod
    def create_ea_repository_using_file_and_short_name(
        ea_repository_file: Files,
        short_name: str,
    ) -> EaRepositories:
        ea_repository = get_repository_using_file_and_short_name(
            ea_repository_file=ea_repository_file,
            short_name=short_name,
        )

        return ea_repository

    def create_empty_ea_repository_with_short_name(
        self, short_name: str
    ) -> EaRepositories:
        ea_repository = get_empty_ea_repository_with_short_name(
            short_name=short_name
        )

        nf_ea_com_universe_manager = (
            self.nf_ea_com_endpoint_manager.nf_ea_com_universe_manager
        )

        nf_ea_com_universe_manager.initialise_empty_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        return ea_repository

    @staticmethod
    def load_ea_packages(
        ea_packages: DataFrame,
    ):
        load_ea_packages(
            ea_packages=ea_packages
        )

    @staticmethod
    def load_ea_classifiers(
        ea_classifiers: DataFrame,
        stereotype_usage_with_names: DataFrame,
    ):
        load_ea_classifiers(
            ea_classifiers=ea_classifiers,
            stereotype_usage_with_names=stereotype_usage_with_names,
        )

    @staticmethod
    def load_ea_proxy_connectors(
        ea_proxy_connectors: DataFrame,
    ):
        load_ea_proxy_connectors(
            ea_proxy_connectors=ea_proxy_connectors
        )

    @staticmethod
    def load_ea_attributes(
        ea_attributes: DataFrame,
    ):
        load_ea_attributes(
            ea_attributes=ea_attributes
        )

    @staticmethod
    def load_ea_connectors(
        ea_connectors: DataFrame,
        stereotype_usage_with_names: DataFrame,
    ):
        load_ea_connectors(
            ea_connectors=ea_connectors,
            stereotype_usage_with_names=stereotype_usage_with_names,
        )

    @staticmethod
    def load_ea_stereotypes(
        ea_repository: EaRepositories,
        ea_stereotypes: DataFrame,
    ):
        load_ea_stereotypes(
            ea_repository=ea_repository,
            ea_stereotypes=ea_stereotypes,
        )

    @staticmethod
    def load_ea_stereotypes_xml(
        ea_repository: EaRepositories,
        xml_string: str,
    ):
        load_ea_stereotypes_xml(
            ea_repository=ea_repository,
            xml_string=xml_string,
        )

    @staticmethod
    def reorder_ea_attributes(
        classifier_id_order: dict,
    ):
        reorder_ea_attributes(
            classifier_id_order=classifier_id_order
        )
