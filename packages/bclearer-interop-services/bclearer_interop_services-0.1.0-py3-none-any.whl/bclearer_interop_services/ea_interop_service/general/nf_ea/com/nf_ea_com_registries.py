from bclearer_core.nf.python_extensions.collections.nf_registries import (
    NfRegistries,
)
from bclearer_core.nf.types.column_types import (
    ColumnTypes,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.dataframe_service.dataframe_mergers import (
    left_merge_dataframes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.connectors.ea_full_dependencies_factories import (
    EaFullDependenciesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.connectors.ea_full_generalisations_factories import (
    EaFullGeneralisationsFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.connectors.ea_full_packages_factories import (
    EaFullPackagesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.connectors.ea_nearest_packages_factories import (
    EaNearestPackagesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.ea_attributes_factories import (
    EaAttributesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.ea_classifiers_factories import (
    EaClassifiersFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.ea_connectors_factories import (
    EaConnectorsFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.ea_diagrams_factories import (
    EaDiagramsFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.ea_operations_factories import (
    EaOperationsFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.ea_packages_factories import (
    EaPackagesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.ea_stererotypes_factories import (
    EaStereotypesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.thin.thin_ea_attributes_factories import (
    ThinEaAttributesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.thin.thin_ea_classifiers_factories import (
    ThinEaClassifiersFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.thin.thin_ea_connectors_factories import (
    ThinEaConnectorsFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.thin.thin_ea_diagrams_factories import (
    ThinEaDiagramsFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.thin.thin_ea_element_components_factories import (
    ThinEaElementComponentsFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.thin.thin_ea_elements_factories import (
    ThinEaElementsFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.thin.thin_ea_explicit_objects_factories import (
    ThinEaExplicitObjectsFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.thin.thin_ea_operations_factories import (
    ThinEaOperationsFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.thin.thin_ea_packageable_objects_factories import (
    ThinEaPackageableObjectsFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.thin.thin_ea_packages_factories import (
    ThinEaPackagesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.thin.thin_ea_repositoried_objects_factories import (
    ThinEaRepositoriedObjectsFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.thin.thin_ea_stereotype_factories import (
    ThinEaStereotypesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.explicit_objects.thin.thin_ea_stereotypeable_objects_factories import (
    ThinEaStereotypeableObjectsFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.non_explicit_objects.ea_cardinalities_factories import (
    EaCardinalitiesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.non_explicit_objects.ea_connector_types_factories import (
    EaConnectorTypesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.non_explicit_objects.ea_diagram_types_factories import (
    EaDiagramTypesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.non_explicit_objects.ea_element_types_factories import (
    EaElementTypesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.non_explicit_objects.ea_object_stereotypes_factories import (
    EaObjectStereotypesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.objects.non_explicit_objects.ea_stererotype_group_factories import (
    EaStereotypeGroupFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.sub_universes.ea_full_dependencies_of_list_of_types_factories import (
    EaFullDependenciesOfListOfTypesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.sub_universes.ea_full_dependencies_of_type_factories import (
    EaFullDependenciesOfTypeFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.sub_universes.ea_full_generalisations_of_type_factories import (
    EaFullGeneralisationsOfTypeFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.sub_universes.intersection_and_symmetric_difference_factories import (
    IntersectionAndSymmetricDifferenceFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.sub_universes.relative_complement_factories import (
    RelativeComplementFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.sub_universes.stereotype_instances_factories import (
    StereotypeInstancesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.sub_universes.stereotyped_objects_of_group_factories import (
    StereotypedObjectsOfGroupFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.sub_universes.stereotyped_objects_universe_from_group_factories import (
    StereotypedObjectsUniverseFromGroupFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.sub_universes.stereotypes_of_group_factories import (
    StereotypesOfGroupFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.sub_universes.table_sub_types_factories import (
    TableSubTypesFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.factories.summaries.ea_package_contents_summary_factories import (
    EaPackageContentsSummaryFactories,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.common.common_data_visualisation.model_stats_tables_to_nf_ea_com_registry_adder import (
    add_model_stats_tables_to_nf_ea_com_registry,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.model_stats.orchestrators.get_model_stats_orchestrator import (
    orchestrate_get_model_stats,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.populators.empty_nf_ea_com_universe_initialiser import (
    create_empty_nf_ea_com_dictionary_of_collections,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.hdf5_service.dataframe_dictionary_from_hdf5_file_reader import (
    read_dataframe_dictionary_from_hdf5_file,
)
from bclearer_interop_services.hdf5_service.dataframe_dictionary_to_hdf5_file_writer import (
    write_dataframe_dictionary_to_hdf5_file,
)
from pandas import DataFrame, concat


class NfEaComRegistries(NfRegistries):
    def __init__(
        self, owning_nf_ea_com_universe
    ):
        NfRegistries.__init__(self)

        self.owning_nf_ea_com_universe = (
            owning_nf_ea_com_universe
        )

    def copy(self):
        self_copy = NfEaComRegistries(
            owning_nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        self_copy.dictionary_of_collections = (
            self.dictionary_of_collections.copy()
        )

        return self_copy

    def create_model_stats_tables(self):
        model_stats_tables = (
            orchestrate_get_model_stats(
                nf_ea_com_registry=self
            )
        )

        add_model_stats_tables_to_nf_ea_com_registry(
            nf_ea_com_registry=self,
            model_stats_tables=model_stats_tables,
        )

    def create_or_update_nf_ea_com_summary_table(
        self,
    ):
        summary_table = DataFrame()

        summary_table = self.__add_counts_to_table(
            summary_table=summary_table,
            collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
            main_type="Element",
            minor_type_column_name=NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name,
            type_collection_type=NfEaComCollectionTypes.EA_ELEMENT_TYPES,
        )

        summary_table = self.__add_counts_to_table(
            summary_table=summary_table,
            collection_type=NfEaComCollectionTypes.EA_PACKAGES,
            main_type="Element",
            minor_type_column_name=NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name,
        )

        summary_table = self.__add_counts_to_table(
            summary_table=summary_table,
            collection_type=NfEaComCollectionTypes.EA_CONNECTORS,
            main_type="Connector",
            minor_type_column_name=NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME.column_name,
            type_collection_type=NfEaComCollectionTypes.EA_CONNECTOR_TYPES,
        )

        summary_table = self.__add_counts_to_table(
            summary_table=summary_table,
            collection_type=NfEaComCollectionTypes.EA_DIAGRAMS,
            main_type="Diagram",
            minor_type_column_name=NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name,
            type_collection_type=NfEaComCollectionTypes.EA_DIAGRAM_TYPES,
        )

        summary_table = self.__add_counts_to_table(
            summary_table=summary_table,
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            main_type="Stereotype",
        )

        summary_table = self.__add_counts_to_table(
            summary_table=summary_table,
            collection_type=NfEaComCollectionTypes.EA_ATTRIBUTES,
            main_type="Attribute",
        )

        summary_table = self.__add_counts_to_table(
            summary_table=summary_table,
            collection_type=NfEaComCollectionTypes.EA_OPERATIONS,
            main_type="Operation",
        )

        summary_table = self.__add_counts_to_table(
            summary_table=summary_table,
            collection_type=NfEaComCollectionTypes.STEREOTYPE_USAGE,
            main_type="Stereotype_usage",
        )

        self.dictionary_of_collections[
            NfEaComCollectionTypes.SUMMARY_TABLE_BY_TYPE
        ] = summary_table

    def __add_counts_to_table(
        self,
        summary_table: DataFrame,
        collection_type: NfEaComCollectionTypes,
        main_type: str,
        minor_type_column_name: str = None,
        type_collection_type: NfEaComCollectionTypes = None,
    ) -> DataFrame:
        table = self.dictionary_of_collections[
            collection_type
        ]

        if (
            minor_type_column_name
            is None
        ):
            data = {
                "main_types": [
                    main_type
                ],
                "minor_types": [
                    main_type
                ],
                "row_count": table.shape[
                    0
                ],
            }

            grouped_by_table = (
                DataFrame(
                    data,
                    columns=[
                        "main_types",
                        "minor_types",
                        "row_count",
                    ],
                )
            )

        else:
            grouped_by_table = (
                table.groupby(
                    [
                        minor_type_column_name
                    ]
                )[
                    NfColumnTypes.NF_UUIDS.column_name
                ]
                .count()
                .reset_index()
            )

            grouped_by_table = grouped_by_table.rename(
                columns={
                    minor_type_column_name: "minor_types",
                    NfColumnTypes.NF_UUIDS.column_name: "row_count",
                }
            )

            if (
                type_collection_type
                is not None
            ):
                type_table = self.dictionary_of_collections[
                    type_collection_type
                ]

                grouped_by_table = left_merge_dataframes(
                    master_dataframe=type_table,
                    master_dataframe_key_columns=[
                        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
                    ],
                    merge_suffixes=[
                        "_type_table",
                        "_count_table",
                    ],
                    foreign_key_dataframe=grouped_by_table,
                    foreign_key_dataframe_fk_columns=[
                        "minor_types"
                    ],
                    foreign_key_dataframe_other_column_rename_dictionary={
                        "row_count": "row_count"
                    },
                )

                grouped_by_table = dataframe_filter_and_rename(
                    dataframe=grouped_by_table,
                    filter_and_rename_dictionary={
                        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: "minor_types",
                        "row_count": "row_count",
                    },
                )

                grouped_by_table = grouped_by_table.fillna(
                    "0.0"
                )

            grouped_by_table[
                "main_types"
            ] = main_type

            grouped_by_table = (
                grouped_by_table[
                    [
                        "main_types",
                        "minor_types",
                        "row_count",
                    ]
                ]
            )

        summary_table = concat(
            [
                summary_table,
                grouped_by_table,
            ]
        )

        return summary_table

    def get_thin_ea_explicit_objects(
        self,
    ) -> DataFrame:
        thin_ea_explicit_objects_factory = ThinEaExplicitObjectsFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        thin_ea_explicit_objects = self.get_collection(
            collection_type=NfEaComCollectionTypes.THIN_EA_EXPLICIT_OBJECTS,
            collection_factory=thin_ea_explicit_objects_factory,
        )

        return thin_ea_explicit_objects

    def get_thin_ea_repositoried_objects(
        self,
    ) -> DataFrame:
        thin_ea_repositoried_objects_factory = ThinEaRepositoriedObjectsFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        thin_ea_repositoried_objects = self.get_collection(
            collection_type=NfEaComCollectionTypes.THIN_EA_REPOSITORIED_OBJECTS,
            collection_factory=thin_ea_repositoried_objects_factory,
        )

        return (
            thin_ea_repositoried_objects
        )

    def get_thin_ea_stereotypeable_objects(
        self,
    ) -> DataFrame:
        thin_ea_stereotypeable_objects_factory = ThinEaStereotypeableObjectsFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        thin_ea_stereotypeable_objects = self.get_collection(
            collection_type=NfEaComCollectionTypes.THIN_EA_STEREOTYPEABLE_OBJECTS,
            collection_factory=thin_ea_stereotypeable_objects_factory,
        )

        return thin_ea_stereotypeable_objects

    def get_thin_ea_packageable_objects(
        self,
    ) -> DataFrame:
        thin_ea_packageable_objects_factory = ThinEaPackageableObjectsFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        thin_ea_packageable_objects = self.get_collection(
            collection_type=NfEaComCollectionTypes.THIN_EA_PACKAGEABLE_OBJECTS,
            collection_factory=thin_ea_packageable_objects_factory,
        )

        return (
            thin_ea_packageable_objects
        )

    def get_thin_ea_elements(
        self,
    ) -> DataFrame:
        thin_ea_elements_factory = ThinEaElementsFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        thin_ea_elements = self.get_collection(
            collection_type=NfEaComCollectionTypes.THIN_EA_ELEMENTS,
            collection_factory=thin_ea_elements_factory,
        )

        return thin_ea_elements

    def get_thin_ea_classifiers(
        self,
    ) -> DataFrame:
        thin_ea_classifiers_factory = ThinEaClassifiersFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        thin_ea_classifiers = self.get_collection(
            collection_type=NfEaComCollectionTypes.THIN_EA_CLASSIFIERS,
            collection_factory=thin_ea_classifiers_factory,
        )

        return thin_ea_classifiers

    def get_thin_ea_packages(
        self,
    ) -> DataFrame:
        thin_ea_packages_factory = ThinEaPackagesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        thin_ea_packages = self.get_collection(
            collection_type=NfEaComCollectionTypes.THIN_EA_PACKAGES,
            collection_factory=thin_ea_packages_factory,
        )

        return thin_ea_packages

    def get_thin_ea_diagrams(
        self,
    ) -> DataFrame:
        thin_ea_diagrams_factory = ThinEaDiagramsFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        thin_ea_diagrams = self.get_collection(
            collection_type=NfEaComCollectionTypes.THIN_EA_DIAGRAMS,
            collection_factory=thin_ea_diagrams_factory,
        )

        return thin_ea_diagrams

    def get_thin_ea_connectors(
        self,
    ) -> DataFrame:
        thin_ea_connectors_factory = ThinEaConnectorsFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        thin_ea_connectors = self.get_collection(
            collection_type=NfEaComCollectionTypes.THIN_EA_CONNECTORS,
            collection_factory=thin_ea_connectors_factory,
        )

        return thin_ea_connectors

    def get_thin_ea_stereotypes(
        self,
    ) -> DataFrame:
        thin_ea_stereotypes_factory = ThinEaStereotypesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        thin_ea_stereotypes = self.get_collection(
            collection_type=NfEaComCollectionTypes.THIN_EA_STEREOTYPES,
            collection_factory=thin_ea_stereotypes_factory,
        )

        return thin_ea_stereotypes

    def get_thin_ea_attributes(
        self,
    ) -> DataFrame:
        thin_ea_attributes_factory = ThinEaAttributesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        thin_ea_attributes = self.get_collection(
            collection_type=NfEaComCollectionTypes.THIN_EA_ATTRIBUTES,
            collection_factory=thin_ea_attributes_factory,
        )

        return thin_ea_attributes

    def get_thin_ea_element_components(
        self,
    ) -> DataFrame:
        ea_element_components_factory = ThinEaElementComponentsFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        thin_ea_element_components = self.get_collection(
            collection_type=NfEaComCollectionTypes.THIN_EA_ELEMENT_COMPONENTS,
            collection_factory=ea_element_components_factory,
        )

        return (
            thin_ea_element_components
        )

    def get_thin_ea_operations(
        self,
    ) -> DataFrame:
        ea_operations_factory = ThinEaOperationsFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        thin_ea_operations = self.get_collection(
            collection_type=NfEaComCollectionTypes.THIN_EA_OPERATIONS,
            collection_factory=ea_operations_factory,
        )

        return thin_ea_operations

    def initialise_empty_nf_ea_com_universe(
        self,
    ) -> None:
        dictionary_of_collections = (
            create_empty_nf_ea_com_dictionary_of_collections()
        )

        self.dictionary_of_collections = (
            dictionary_of_collections
        )

    def get_ea_classifiers(
        self,
    ) -> DataFrame:
        ea_classifiers_factory = EaClassifiersFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_classifiers = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_CLASSIFIERS,
            collection_factory=ea_classifiers_factory,
        )

        return ea_classifiers

    def get_ea_packages(
        self,
    ) -> DataFrame:
        ea_packages_factory = EaPackagesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_packages = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_PACKAGES,
            collection_factory=ea_packages_factory,
        )

        return ea_packages

    def get_ea_diagrams(
        self,
    ) -> DataFrame:
        ea_diagrams_factory = EaDiagramsFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_diagrams = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_DIAGRAMS,
            collection_factory=ea_diagrams_factory,
        )

        return ea_diagrams

    def get_ea_stereotypes(
        self,
    ) -> DataFrame:
        ea_stereotype_factory = EaStereotypesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_stereotypes = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPES,
            collection_factory=ea_stereotype_factory,
        )

        return ea_stereotypes

    def get_ea_stereotype_groups(
        self,
    ) -> DataFrame:
        ea_stereotype_group_factory = EaStereotypeGroupFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_stereotype_groups = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_STEREOTYPE_GROUPS,
            collection_factory=ea_stereotype_group_factory,
        )

        return ea_stereotype_groups

    def get_ea_connectors(
        self,
    ) -> DataFrame:
        ea_connectors_factory = EaConnectorsFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_connectors = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_CONNECTORS,
            collection_factory=ea_connectors_factory,
        )

        return ea_connectors

    def get_ea_attributes(
        self,
    ) -> DataFrame:
        ea_attributes_factory = EaAttributesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_attributes = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_ATTRIBUTES,
            collection_factory=ea_attributes_factory,
        )

        return ea_attributes

    def get_ea_operations(
        self,
    ) -> DataFrame:
        ea_operations_factory = EaOperationsFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_operations = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_OPERATIONS,
            collection_factory=ea_operations_factory,
        )

        return ea_operations

    def get_ea_object_stereotypes(
        self,
    ) -> DataFrame:
        ea_object_stereotypes_factory = EaObjectStereotypesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_object_stereotypes = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_OBJECT_STEREOTYPES,
            collection_factory=ea_object_stereotypes_factory,
        )

        return ea_object_stereotypes

    def get_ea_connector_types(
        self,
    ) -> DataFrame:
        ea_connector_types_factory = EaConnectorTypesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_connector_types = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_CONNECTOR_TYPES,
            collection_factory=ea_connector_types_factory,
        )

        return ea_connector_types

    def get_ea_element_types(
        self,
    ) -> DataFrame:
        ea_element_types_factory = EaElementTypesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_element_types = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_ELEMENT_TYPES,
            collection_factory=ea_element_types_factory,
        )

        return ea_element_types

    def get_ea_diagram_types(
        self,
    ) -> DataFrame:
        ea_diagram_types_factory = EaDiagramTypesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_diagram_types = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_DIAGRAM_TYPES,
            collection_factory=ea_diagram_types_factory,
        )

        return ea_diagram_types

    def get_ea_cardinalities(
        self,
    ) -> DataFrame:
        ea_cardinalities_factory = EaCardinalitiesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_cardinalities = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_CARDINALITIES,
            collection_factory=ea_cardinalities_factory,
        )

        return ea_cardinalities

    def get_ea_full_generalisations(
        self,
    ) -> DataFrame:
        ea_full_generalisations_factory = EaFullGeneralisationsFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_full_generalisations = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_FULL_GENERALISATIONS,
            collection_factory=ea_full_generalisations_factory,
        )

        return ea_full_generalisations

    def get_ea_full_dependencies(
        self,
    ) -> DataFrame:
        ea_full_dependencies_factory = EaFullDependenciesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_full_dependencies = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_FULL_DEPENDENCIES,
            collection_factory=ea_full_dependencies_factory,
        )

        return ea_full_dependencies

    def get_ea_nearest_packages(
        self,
    ) -> DataFrame:
        ea_nearest_packages_factory = EaNearestPackagesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_nearest_packages = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_NEAREST_PACKAGES,
            collection_factory=ea_nearest_packages_factory,
        )

        return ea_nearest_packages

    def get_ea_full_packages(
        self,
    ) -> DataFrame:
        ea_full_packages_factory = EaFullPackagesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_full_packages = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_FULL_PACKAGES,
            collection_factory=ea_full_packages_factory,
        )

        return ea_full_packages

    def get_ea_package_contents_summary(
        self,
    ) -> DataFrame:
        ea_package_contents_summary_factory = EaPackageContentsSummaryFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe
        )

        ea_package_contents_summary = self.get_collection(
            collection_type=NfEaComCollectionTypes.EA_PACKAGE_CONTENTS_SUMMARY,
            collection_factory=ea_package_contents_summary_factory,
        )

        return (
            ea_package_contents_summary
        )

    def get_ea_full_generalisations_of_type(
        self, type_ea_guid: str
    ) -> DataFrame:
        ea_full_generalisations_of_type_factory = EaFullGeneralisationsOfTypeFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe,
            type_ea_guid=type_ea_guid,
        )

        ea_full_generalisations_of_type = (
            ea_full_generalisations_of_type_factory.create()
        )

        return ea_full_generalisations_of_type

    def get_ea_full_dependencies_of_type(
        self, type_ea_guid: str
    ) -> DataFrame:
        ea_full_dependencies_of_type_factory = EaFullDependenciesOfTypeFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe,
            type_ea_guid=type_ea_guid,
        )

        ea_full_dependencies_of_type = (
            ea_full_dependencies_of_type_factory.create()
        )

        return (
            ea_full_dependencies_of_type
        )

    def get_ea_full_dependencies_of_list_of_types(
        self, list_of_types: DataFrame
    ) -> DataFrame:
        ea_full_dependencies_of_type_factory = EaFullDependenciesOfListOfTypesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe,
            list_of_types=list_of_types,
        )

        ea_full_dependencies_of_type = (
            ea_full_dependencies_of_type_factory.create()
        )

        return (
            ea_full_dependencies_of_type
        )

    def get_intersection_and_symmetric_difference(
        self,
        input_table_1: DataFrame,
        input_table_2: DataFrame,
    ) -> DataFrame:
        intersection_and_symmetric_difference_factory = IntersectionAndSymmetricDifferenceFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe,
            input_table_1=input_table_1,
            input_table_2=input_table_2,
        )

        intersection_and_symmetric_difference = (
            intersection_and_symmetric_difference_factory.create()
        )

        return intersection_and_symmetric_difference

    def get_stereotype_instances(
        self, stereotype_ea_guid: str
    ) -> DataFrame:
        stereotype_instances_factory = StereotypeInstancesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe,
            stereotype_ea_guid=stereotype_ea_guid,
        )

        stereotype_instances = (
            stereotype_instances_factory.create()
        )

        return stereotype_instances

    def get_relative_complement(
        self,
        full_table: DataFrame,
        exception_table: DataFrame,
    ) -> DataFrame:
        relative_complement_factory = RelativeComplementFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe,
            full_table=full_table,
            exception_table=exception_table,
        )

        relative_complement = (
            relative_complement_factory.create()
        )

        return relative_complement

    def get_table_sub_types(
        self,
        table: DataFrame,
        type_column: ColumnTypes,
        object_types: list,
    ) -> DataFrame:
        table_sub_types_factory = TableSubTypesFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe,
            table=table,
            type_column=type_column,
            object_types=object_types,
        )

        table_sub_types = (
            table_sub_types_factory.create()
        )

        return table_sub_types

    def get_ea_stereotypes_of_group(
        self, stereotype_group_name: str
    ) -> DataFrame:
        ea_stereotypes_of_group_factory = StereotypesOfGroupFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe,
            stereotype_group_name=stereotype_group_name,
        )

        ea_stereotypes_of_group = (
            ea_stereotypes_of_group_factory.create()
        )

        return ea_stereotypes_of_group

    def get_stereotyped_objects_of_group(
        self, stereotype_group_name: str
    ) -> DataFrame:
        stereotyped_objects_of_group_factory = StereotypedObjectsOfGroupFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe,
            stereotype_group_name=stereotype_group_name,
        )

        stereotyped_objects_of_group = (
            stereotyped_objects_of_group_factory.create()
        )

        return (
            stereotyped_objects_of_group
        )

    def create_stereotyped_objects_universe_from_group(
        self, stereotype_group_name: str
    ):
        ea_stereotypes_of_group_factory = StereotypedObjectsUniverseFromGroupFactories(
            nf_ea_com_universe=self.owning_nf_ea_com_universe,
            stereotype_group_name=stereotype_group_name,
        )

        ea_stereotypes_of_group_factory.create()

    def import_registry_from_hdf5(
        self, hdf5_file: Files
    ):
        dictionary_of_collections_keyed_with_string = read_dataframe_dictionary_from_hdf5_file(
            hdf_store_filename=hdf5_file.absolute_path_string
        )

        for (
            collection_name,
            collection,
        ) in (
            dictionary_of_collections_keyed_with_string.items()
        ):
            self.__replace_using_collection_name(
                collection_name=collection_name,
                collection=collection,
            )

    def export_registry_to_hdf5(
        self, hdf5_file: Files
    ):
        dictionary_of_collections_keyed_with_string = (
            {}
        )

        for (
            collection_type,
            collection,
        ) in (
            self.dictionary_of_collections.items()
        ):
            dictionary_of_collections_keyed_with_string[
                collection_type.collection_name
            ] = collection

        write_dataframe_dictionary_to_hdf5_file(
            hdf5_file_name=hdf5_file.absolute_path_string,
            dataframes_dictionary=dictionary_of_collections_keyed_with_string,
        )

    def __replace_using_collection_name(
        self,
        collection_name: str,
        collection: DataFrame,
    ):
        collection_type = NfEaComCollectionTypes.get_collection_type_from_name(
            name=collection_name
        )

        self.replace_collection(
            collection_type=collection_type,
            collection=collection,
        )
