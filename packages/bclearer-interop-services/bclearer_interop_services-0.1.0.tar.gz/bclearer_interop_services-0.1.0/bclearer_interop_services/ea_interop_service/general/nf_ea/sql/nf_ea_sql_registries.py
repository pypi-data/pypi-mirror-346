from bclearer_core.nf.python_extensions.collections.nf_registries import (
    NfRegistries,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.common_knowledge.maps.ea_guids_to_ea_identifiers_for_objects_mappings import (
    EaGuidsToEaIdentifiersForObjectsMappings,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.common_knowledge.maps.ea_guids_to_ea_identifiers_for_packages_mappings import (
    EaGuidsToEaIdentifiersForPackagesMappings,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.derived_dataframe_creators.object_stereotypes_dataframe_creator import (
    create_object_stereotypes_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.extended_t_attribute_dataframe_creator import (
    create_extended_t_attribute_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.extended_t_cardinality_dataframe_creator import (
    create_extended_t_cardinality_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.extended_t_connector_dataframe_creator import (
    create_extended_t_connector_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.extended_t_connector_types_dataframe_creator import (
    create_extended_t_connector_types_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.extended_t_diagram_dataframe_creator import (
    create_extended_t_diagram_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.extended_t_diagramlinks_dataframe_creator import (
    create_extended_t_diagramlinks_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.extended_t_diagramobjects_dataframe_creator import (
    create_extended_t_diagramobjects_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.extended_t_diagramtypes_dataframe_creator import (
    create_extended_t_diagramtypes_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.extended_t_object_dataframe_classifier_column_adder import (
    add_classifier_column_to_extended_t_object_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.extended_t_object_dataframe_creator import (
    create_extended_t_object_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.extended_t_objecttypes_dataframe_creator import (
    create_extended_t_objecttypes_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.extended_t_operations_dataframe_creator import (
    create_extended_t_operation_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.extended_t_stereotypes_dataframe_creator import (
    create_extended_t_stereotypes_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.extended_t_table_dataframe_creators.extended_t_xref_dataframe_creator import (
    create_extended_t_xref_dataframe,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.sql.hierarchy_constructors.package_hierarchy_constructor import (
    construct_package_hierarchy_dataframe,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_attribute_column_types import (
    EaTAttributeColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_object_column_types import (
    EaTObjectColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_package_column_types import (
    EaTPackageColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from pandas import DataFrame


class NfEaSqlRegistries(NfRegistries):
    def __init__(
        self, owning_nf_ea_sql_universe
    ):
        NfRegistries.__init__(self)

        self.owning_nf_ea_sql_universe = (
            owning_nf_ea_sql_universe
        )

        self.universe_key = (
            owning_nf_ea_sql_universe.ea_repository.short_name
        )

    def get_extended_ea_t_table_dataframe(
        self,
        ea_collection_type: EaCollectionTypes,
    ) -> DataFrame:
        if (
            ea_collection_type
            == EaCollectionTypes.EXTENDED_T_OBJECT
        ):
            return (
                self.get_extended_t_object_dataframe()
            )

        if (
            ea_collection_type
            == EaCollectionTypes.EXTENDED_T_ATTRIBUTE
        ):
            return (
                self.get_extended_t_attribute_dataframe()
            )

        if (
            ea_collection_type
            == EaCollectionTypes.EXTENDED_T_OPERATION
        ):
            return (
                self.get_extended_t_operation_dataframe()
            )

        if (
            ea_collection_type
            == EaCollectionTypes.EXTENDED_T_PACKAGE
        ):
            return (
                self.get_package_hierarchy_dataframe()
            )

        if (
            ea_collection_type
            == EaCollectionTypes.EXTENDED_T_CONNECTOR
        ):
            return (
                self.get_extended_t_connector_dataframe()
            )

        if (
            ea_collection_type
            == EaCollectionTypes.EXTENDED_T_XREF
        ):
            return (
                self.get_extended_t_xref_dataframe()
            )

        if (
            ea_collection_type
            == EaCollectionTypes.EXTENDED_T_STEREOTYPES
        ):
            return (
                self.get_extended_t_stereotypes_dataframe()
            )

        if (
            ea_collection_type
            == EaCollectionTypes.EXTENDED_T_DIAGRAM
        ):
            return (
                self.get_extended_t_diagram_dataframe()
            )

        if (
            ea_collection_type
            == EaCollectionTypes.EXTENDED_T_DIAGRAMOBJECTS
        ):
            return (
                self.get_extended_t_diagramobjects_dataframe()
            )

        if (
            ea_collection_type
            == EaCollectionTypes.EXTENDED_T_DIAGRAMLINKS
        ):
            return (
                self.get_extended_t_diagramlinks_dataframe()
            )

        if (
            ea_collection_type
            == EaCollectionTypes.EXTENDED_T_OBJECTTYPES
        ):
            return (
                self.get_extended_t_objecttypes_dataframe()
            )

        if (
            ea_collection_type
            == EaCollectionTypes.EXTENDED_T_CONNECTORTYPES
        ):
            return (
                self.get_extended_t_connector_types_dataframe()
            )

        if (
            ea_collection_type
            == EaCollectionTypes.EXTENDED_T_DIAGRAMTYPES
        ):
            return (
                self.get_extended_t_diagramtypes_dataframe()
            )

        if (
            ea_collection_type
            == EaCollectionTypes.EXTENDED_T_CARDINALITY
        ):
            return (
                self.get_extended_t_cardinality_dataframe()
            )

        if (
            ea_collection_type
            == EaCollectionTypes.OBJECT_STEREOTYPES
        ):
            return (
                self.get_object_stereotypes_dataframe()
            )

    def get_extended_t_object_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.EXTENDED_T_OBJECT
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.EXTENDED_T_OBJECT
            ]

        extended_t_object_dataframe = create_extended_t_object_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe,
            universe_key=self.universe_key,
        )

        self.dictionary_of_collections[
            EaCollectionTypes.EXTENDED_T_OBJECT
        ] = extended_t_object_dataframe

        extended_t_object_dataframe = add_classifier_column_to_extended_t_object_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe
        )

        self.dictionary_of_collections[
            EaCollectionTypes.EXTENDED_T_OBJECT
        ] = extended_t_object_dataframe

        return (
            extended_t_object_dataframe
        )

    def get_extended_t_attribute_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.EXTENDED_T_ATTRIBUTE
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.EXTENDED_T_ATTRIBUTE
            ]

        extended_t_attribute_dataframe = create_extended_t_attribute_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe,
            universe_key=self.universe_key,
        )

        self.dictionary_of_collections[
            EaCollectionTypes.EXTENDED_T_ATTRIBUTE
        ] = extended_t_attribute_dataframe

        return extended_t_attribute_dataframe

    def get_extended_t_xref_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.EXTENDED_T_XREF
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.EXTENDED_T_XREF
            ]

        extended_t_xref_dataframe = create_extended_t_xref_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe
        )

        self.dictionary_of_collections[
            EaCollectionTypes.EXTENDED_T_XREF
        ] = extended_t_xref_dataframe

        return extended_t_xref_dataframe

    def get_extended_t_connector_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.EXTENDED_T_CONNECTOR
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.EXTENDED_T_CONNECTOR
            ]

        extended_t_connector_dataframe = create_extended_t_connector_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe,
            universe_key=self.universe_key,
        )

        self.dictionary_of_collections[
            EaCollectionTypes.EXTENDED_T_CONNECTOR
        ] = extended_t_connector_dataframe

        return extended_t_connector_dataframe

    def get_extended_t_diagram_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.EXTENDED_T_DIAGRAM
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.EXTENDED_T_DIAGRAM
            ]

        extended_t_diagram_dataframe = create_extended_t_diagram_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe,
            universe_key=self.universe_key,
        )

        self.dictionary_of_collections[
            EaCollectionTypes.EXTENDED_T_DIAGRAM
        ] = extended_t_diagram_dataframe

        return (
            extended_t_diagram_dataframe
        )

    def get_extended_t_diagramlinks_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.EXTENDED_T_DIAGRAMLINKS.collection_name
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.EXTENDED_T_DIAGRAMLINKS.collection_name
            ]

        extended_t_diagramlinks_dataframe = create_extended_t_diagramlinks_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe,
            universe_key=self.universe_key,
        )

        self.dictionary_of_collections[
            EaCollectionTypes.EXTENDED_T_DIAGRAMLINKS.collection_name
        ] = extended_t_diagramlinks_dataframe

        return extended_t_diagramlinks_dataframe

    def get_extended_t_diagramobjects_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.EXTENDED_T_DIAGRAMOBJECTS
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.EXTENDED_T_DIAGRAMOBJECTS
            ]

        extended_t_diagramobjects_dataframe = create_extended_t_diagramobjects_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe,
            universe_key=self.universe_key,
        )

        self.dictionary_of_collections[
            EaCollectionTypes.EXTENDED_T_DIAGRAMOBJECTS
        ] = extended_t_diagramobjects_dataframe

        return extended_t_diagramobjects_dataframe

    def get_extended_t_stereotypes_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.EXTENDED_T_STEREOTYPES
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.EXTENDED_T_STEREOTYPES
            ]

        extended_t_stereotypes_dataframe = create_extended_t_stereotypes_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe,
            universe_key=self.universe_key,
        )

        self.dictionary_of_collections[
            EaCollectionTypes.EXTENDED_T_STEREOTYPES
        ] = extended_t_stereotypes_dataframe

        return extended_t_stereotypes_dataframe

    def get_extended_t_operation_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.EXTENDED_T_OPERATION
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.EXTENDED_T_OPERATION
            ]

        extended_t_operation_dataframe = create_extended_t_operation_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe,
            universe_key=self.universe_key,
        )

        self.dictionary_of_collections[
            EaCollectionTypes.EXTENDED_T_OPERATION
        ] = extended_t_operation_dataframe

        return extended_t_operation_dataframe

    def get_extended_t_connector_types_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.EXTENDED_T_CONNECTORTYPES
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.EXTENDED_T_CONNECTORTYPES
            ]

        extended_t_connector_types_dataframe = create_extended_t_connector_types_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe,
            universe_key=self.universe_key,
        )

        self.dictionary_of_collections[
            EaCollectionTypes.EXTENDED_T_CONNECTORTYPES
        ] = extended_t_connector_types_dataframe

        return extended_t_connector_types_dataframe

    def get_extended_t_objecttypes_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.EXTENDED_T_OBJECTTYPES
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.EXTENDED_T_OBJECTTYPES
            ]

        extended_t_objecttypes_dataframe = create_extended_t_objecttypes_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe,
            universe_key=self.universe_key,
        )

        self.dictionary_of_collections[
            EaCollectionTypes.EXTENDED_T_OBJECTTYPES
        ] = extended_t_objecttypes_dataframe

        return extended_t_objecttypes_dataframe

    def get_extended_t_diagramtypes_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.EXTENDED_T_DIAGRAMTYPES
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.EXTENDED_T_DIAGRAMTYPES
            ]

        extended_t_diagramtypes_dataframe = create_extended_t_diagramtypes_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe,
            universe_key=self.universe_key,
        )

        self.dictionary_of_collections[
            EaCollectionTypes.EXTENDED_T_DIAGRAMTYPES
        ] = extended_t_diagramtypes_dataframe

        return extended_t_diagramtypes_dataframe

    def get_extended_t_cardinality_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.EXTENDED_T_CARDINALITY
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.EXTENDED_T_CARDINALITY
            ]

        extended_t_cardinality_dataframe = create_extended_t_cardinality_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe,
            universe_key=self.universe_key,
        )

        self.dictionary_of_collections[
            EaCollectionTypes.EXTENDED_T_CARDINALITY
        ] = extended_t_cardinality_dataframe

        return extended_t_cardinality_dataframe

    def get_object_stereotypes_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.OBJECT_STEREOTYPES
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.OBJECT_STEREOTYPES
            ]

        object_stereotypes_dataframe = create_object_stereotypes_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe
        )

        self.dictionary_of_collections[
            EaCollectionTypes.OBJECT_STEREOTYPES
        ] = object_stereotypes_dataframe

        return (
            object_stereotypes_dataframe
        )

    def get_package_hierarchy_dataframe(
        self,
    ) -> DataFrame:
        if (
            EaCollectionTypes.PACKAGE_HIERARCHY
            in self.dictionary_of_collections
        ):
            return self.dictionary_of_collections[
                EaCollectionTypes.PACKAGE_HIERARCHY
            ]

        package_hierarchy_dataframe = construct_package_hierarchy_dataframe(
            nf_ea_sql_universe=self.owning_nf_ea_sql_universe
        )

        self.dictionary_of_collections[
            EaCollectionTypes.PACKAGE_HIERARCHY
        ] = package_hierarchy_dataframe

        return (
            package_hierarchy_dataframe
        )

    def add_ea_guids_to_ea_identifiers_for_objects(
        self,
    ):
        objects_dataframe = (
            self.get_extended_t_object_dataframe()
        )

        # ea_guids_to_object_identifiers_dataframe = \
        #     objects_dataframe[EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.column_name, EaTObjectColumnTypes.T_OBJECT_IDS.column_name()]

        ea_guids_to_object_identifiers_dataframe = DataFrame(
            objects_dataframe[
                [
                    EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name,
                    EaTObjectColumnTypes.T_OBJECT_IDS.nf_column_name,
                ]
            ]
        )

        ea_guids_to_object_identifiers_map = ea_guids_to_object_identifiers_dataframe.set_index(
            EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.nf_column_name
        )[
            EaTObjectColumnTypes.T_OBJECT_IDS.nf_column_name
        ].to_dict()

        EaGuidsToEaIdentifiersForObjectsMappings.map.set_map(
            ea_guids_to_object_identifiers_map
        )

    def add_ea_guids_to_ea_identifiers_for_packages(
        self,
    ):
        packages_dataframe = self.owning_nf_ea_sql_universe.ea_tools_session_manager.ea_sql_stage_manager.ea_sql_universe_manager.get_ea_t_table_dataframe(
            ea_repository=self.owning_nf_ea_sql_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.T_PACKAGE,
        )

        ea_guids_to_package_identifiers_dataframe = DataFrame(
            packages_dataframe[
                [
                    EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS.nf_column_name,
                    EaTPackageColumnTypes.T_PACKAGE_IDS.nf_column_name,
                ]
            ]
        )

        ea_guids_to_package_identifiers_map = ea_guids_to_package_identifiers_dataframe.set_index(
            EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS.nf_column_name
        )[
            EaTPackageColumnTypes.T_PACKAGE_IDS.nf_column_name
        ].to_dict()

        EaGuidsToEaIdentifiersForPackagesMappings.map.set_map(
            ea_guids_to_package_identifiers_map
        )

    def get_last_ea_identifier_for_objects(
        self,
    ) -> int:
        objects_dataframe = (
            self.get_extended_t_object_dataframe()
        )

        ea_object_identifiers_dataframe = objects_dataframe[
            [
                EaTObjectColumnTypes.T_OBJECT_IDS.nf_column_name
            ]
        ]

        sorted_ea_object_identifiers_dataframe = ea_object_identifiers_dataframe.sort_values(
            by=EaTObjectColumnTypes.T_OBJECT_IDS.nf_column_name,
            ascending=False,
        )

        if len(objects_dataframe) == 0:
            return 0

        last_ea_identifier_for_objects = int(
            sorted_ea_object_identifiers_dataframe[
                EaTObjectColumnTypes.T_OBJECT_IDS.nf_column_name
            ].iloc[
                0
            ]
        )

        return last_ea_identifier_for_objects

    def get_last_ea_identifier_for_packages(
        self,
    ) -> int:
        packages_dataframe = self.owning_nf_ea_sql_universe.ea_tools_session_manager.ea_sql_stage_manager.ea_sql_universe_manager.get_ea_t_table_dataframe(
            ea_repository=self.owning_nf_ea_sql_universe.ea_repository,
            ea_collection_type=EaCollectionTypes.T_PACKAGE,
        )

        ea_package_identifiers_dataframe = packages_dataframe[
            [
                EaTPackageColumnTypes.T_PACKAGE_IDS.nf_column_name
            ]
        ]

        sorted_ea_package_identifiers_dataframe = ea_package_identifiers_dataframe.sort_values(
            by=EaTPackageColumnTypes.T_PACKAGE_IDS.nf_column_name,
            ascending=False,
        )

        if len(packages_dataframe) == 0:
            return 0

        last_ea_identifier_for_packages = int(
            sorted_ea_package_identifiers_dataframe[
                EaTPackageColumnTypes.T_PACKAGE_IDS.nf_column_name
            ].iloc[
                0
            ]
        )

        return last_ea_identifier_for_packages

    def get_last_ea_identifier_for_attributes(
        self,
    ) -> int:
        attributes_dataframe = (
            self.get_extended_t_attribute_dataframe()
        )

        ea_attribute_identifiers_dataframe = attributes_dataframe[
            [
                EaTAttributeColumnTypes.T_ATTRIBUTE_IDS.nf_column_name
            ]
        ]

        sorted_ea_attribute_identifiers_dataframe = ea_attribute_identifiers_dataframe.sort_values(
            by=EaTAttributeColumnTypes.T_ATTRIBUTE_IDS.nf_column_name,
            ascending=False,
        )

        if (
            len(attributes_dataframe)
            == 0
        ):
            return 0

        last_ea_identifier_for_attributes = int(
            sorted_ea_attribute_identifiers_dataframe[
                EaTAttributeColumnTypes.T_ATTRIBUTE_IDS.nf_column_name
            ].iloc[
                0
            ]
        )

        return last_ea_identifier_for_attributes
