from bclearer_core.nf.types.column_types import (
    ColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)
from bclearer_interop_services.ea_interop_service.session.nf_ea_com_endpoint.orchestrators.nf_managers import (
    NfManagers,
)
from pandas import DataFrame


class NfEaComUniverseManagers(
    NfManagers
):
    def __init__(
        self, ea_tools_session_manager
    ):
        NfManagers.__init__(self)

        self.ea_tools_session_manager = (
            ea_tools_session_manager
        )

        self.nf_ea_com_universe_dictionary = (
            dict()
        )

    def initialise_empty_nf_ea_com_universe(
        self,
        ea_repository: EaRepositories,
    ) -> None:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        nf_ea_com_universe.nf_ea_com_registry.initialise_empty_nf_ea_com_universe()

    def get_ea_classifiers(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_classifiers = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_classifiers()
        )

        return ea_classifiers

    def get_ea_packages(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_packages = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_packages()
        )

        return ea_packages

    def get_ea_diagrams(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_diagrams = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_diagrams()
        )

        return ea_diagrams

    def get_ea_connectors(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_connectors = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_connectors()
        )

        return ea_connectors

    def get_ea_stereotype_groups(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_stereotype_groups = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_stereotype_groups()
        )

        return ea_stereotype_groups

    def get_ea_stereotypes(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_stereotypes = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_stereotypes()
        )

        return ea_stereotypes

    def get_ea_attributes(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_attributes = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_attributes()
        )

        return ea_attributes

    def get_ea_operations(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_operations = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_operations()
        )

        return ea_operations

    def get_ea_object_stereotypes(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_object_stereotypes = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_object_stereotypes()
        )

        return ea_object_stereotypes

    def get_ea_connector_types(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_connector_types = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_connector_types()
        )

        return ea_connector_types

    def get_ea_element_types(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_element_types = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_element_types()
        )

        return ea_element_types

    def get_ea_diagram_types(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_diagram_types = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_diagram_types()
        )

        return ea_diagram_types

    def get_ea_cardinalities(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_cardinalities = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_cardinalities()
        )

        return ea_cardinalities

    def get_ea_full_generalisations(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_full_generalisations = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_full_generalisations()
        )

        return ea_full_generalisations

    def get_ea_full_dependencies(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_full_dependencies = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_full_dependencies()
        )

        return ea_full_dependencies

    def get_ea_nearest_packages(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_nearest_packages = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_nearest_packages()
        )

        return ea_nearest_packages

    def get_ea_full_packages(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_full_packages = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_full_packages()
        )

        return ea_full_packages

    def get_ea_package_contents_summary(
        self,
        ea_repository: EaRepositories,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_package_contents_summary = (
            nf_ea_com_universe.nf_ea_com_registry.get_ea_package_contents_summary()
        )

        return (
            ea_package_contents_summary
        )

    def get_ea_full_generalisations_of_type(
        self,
        ea_repository: EaRepositories,
        type_ea_guid: str,
        table_name: str,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_full_generalisations_of_type = nf_ea_com_universe.nf_ea_com_registry.get_ea_full_generalisations_of_type(
            type_ea_guid=type_ea_guid,
            table_name=table_name,
        )

        return ea_full_generalisations_of_type

    def get_ea_full_dependencies_of_type(
        self,
        ea_repository: EaRepositories,
        type_ea_guid: str,
        table_name: str,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_full_dependencies_of_type = nf_ea_com_universe.nf_ea_com_registry.get_ea_full_dependencies_of_type(
            type_ea_guid=type_ea_guid,
            table_name=table_name,
        )

        return (
            ea_full_dependencies_of_type
        )

    def get_ea_full_dependencies_of_list_of_types(
        self,
        ea_repository: EaRepositories,
        list_of_types: DataFrame,
        table_name: str,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_full_dependencies_of_list_of_types = nf_ea_com_universe.nf_ea_com_registry.get_ea_full_dependencies_of_list_of_types(
            list_of_types=list_of_types,
            table_name=table_name,
        )

        return ea_full_dependencies_of_list_of_types

    def get_intersection_and_symmetric_difference(
        self,
        ea_repository: EaRepositories,
        input_table_1: DataFrame,
        input_table_2: DataFrame,
        output_table_name: str,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        intersection_and_symmetric_difference = nf_ea_com_universe.nf_ea_com_registry.get_intersection_and_symmetric_difference(
            input_table_1=input_table_1,
            input_table_2=input_table_2,
            output_table_name=output_table_name,
        )

        return intersection_and_symmetric_difference

    def get_stereotype_instances(
        self,
        ea_repository: EaRepositories,
        stereotype_ea_guid: str,
        table_name: str,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        stereotype_instances = nf_ea_com_universe.nf_ea_com_registry.get_stereotype_instances(
            stereotype_ea_guid=stereotype_ea_guid,
            table_name=table_name,
        )

        return stereotype_instances

    def get_relative_complement(
        self,
        ea_repository: EaRepositories,
        full_table: DataFrame,
        exception_table: DataFrame,
        table_name: str,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        relative_complement = nf_ea_com_universe.nf_ea_com_registry.get_relative_complement(
            full_table=full_table,
            exception_table=exception_table,
            table_name=table_name,
        )

        return relative_complement

    def get_table_sub_types(
        self,
        ea_repository: EaRepositories,
        table: DataFrame,
        type_column: ColumnTypes,
        object_types: list,
        table_name: str,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        table_sub_types = nf_ea_com_universe.nf_ea_com_registry.get_table_sub_types(
            table=table,
            type_column=type_column,
            object_types=object_types,
            table_name=table_name,
        )

        return table_sub_types

    def get_ea_stereotypes_of_group(
        self,
        ea_repository: EaRepositories,
        stereotype_group_name: str,
        table_name: str,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        ea_stereotypes_of_group = nf_ea_com_universe.nf_ea_com_registry.get_ea_stereotypes_of_group(
            stereotype_group_name=stereotype_group_name,
            table_name=table_name,
        )

        return ea_stereotypes_of_group

    def get_stereotyped_objects_of_group(
        self,
        ea_repository: EaRepositories,
        stereotype_group_name: str,
        table_name: str,
    ) -> DataFrame:
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        stereotyped_objects_of_group = nf_ea_com_universe.nf_ea_com_registry.get_stereotyped_objects_of_group(
            stereotype_group_name=stereotype_group_name,
            table_name=table_name,
        )

        return (
            stereotyped_objects_of_group
        )

    def create_stereotyped_objects_universe_from_group(
        self,
        ea_repository: EaRepositories,
        stereotype_group_name: str,
    ):
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        nf_ea_com_universe.nf_ea_com_registry.create_stereotyped_objects_universe_from_group(
            stereotype_group_name=stereotype_group_name
        )

    def add_table(
        self,
        ea_repository: EaRepositories,
        table: DataFrame,
        table_name: str,
    ):
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        nf_ea_com_universe.nf_ea_com_registry.add_table(
            table=table,
            table_name=table_name,
        )

    def export_all_registries(
        self, output_folder_name: str
    ):
        for (
            ea_repository,
            nf_ea_com_universe,
        ) in (
            self.nf_ea_com_universe_dictionary.items()
        ):
            nf_ea_com_universe.nf_ea_com_registry.export_dataframes_to_new_database(
                short_name=ea_repository.short_name,
                output_folder_name=output_folder_name,
                database_basename="nf_ea_com",
            )

    def create_or_update_summary_table(
        self,
        ea_repository: EaRepositories,
    ):
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        nf_ea_com_universe.nf_ea_com_registry.create_or_update_summary_table()

    def create_or_update_nf_ea_com_summary_table(
        self,
        ea_repository: EaRepositories,
    ):
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        nf_ea_com_universe.nf_ea_com_registry.create_or_update_nf_ea_com_summary_table()

    def create_model_stats_tables(
        self,
        ea_repository: EaRepositories,
    ):
        nf_ea_com_universe = self.__get_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        nf_ea_com_universe.nf_ea_com_registry.create_model_stats_tables()

    def __get_nf_ea_com_universe(
        self,
        ea_repository: EaRepositories,
    ) -> NfEaComUniverses:
        if (
            ea_repository
            in self.nf_ea_com_universe_dictionary
        ):
            return self.nf_ea_com_universe_dictionary[
                ea_repository
            ]

        nf_ea_com_universe = self.__create_nf_ea_com_universe(
            ea_repository=ea_repository
        )

        self.nf_ea_com_universe_dictionary[
            ea_repository
        ] = nf_ea_com_universe

        return nf_ea_com_universe

    def __create_nf_ea_com_universe(
        self,
        ea_repository: EaRepositories,
    ) -> NfEaComUniverses:
        nf_ea_com_universe = NfEaComUniverses(
            self.ea_tools_session_manager,
            ea_repository=ea_repository,
        )

        return nf_ea_com_universe

    def close(self):
        pass
