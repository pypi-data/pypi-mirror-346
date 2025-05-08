from enum import auto, unique

from bclearer_core.nf.types.collection_types import (
    CollectionTypes,
)


@unique
class NfEaComCollectionTypes(
    CollectionTypes
):
    EA_PACKAGES = auto()
    EA_CLASSIFIERS = auto()
    EA_ATTRIBUTES = auto()
    EA_CONNECTORS = auto()
    EA_CONNECTORS_PC = auto()
    EA_STEREOTYPES = auto()
    STEREOTYPE_USAGE = auto()
    THIN_EA_EXPLICIT_OBJECTS = auto()
    THIN_EA_REPOSITORIED_OBJECTS = (
        auto()
    )
    THIN_EA_STEREOTYPEABLE_OBJECTS = (
        auto()
    )
    THIN_EA_PACKAGEABLE_OBJECTS = auto()
    THIN_EA_ELEMENTS = auto()
    THIN_EA_CLASSIFIERS = auto()
    THIN_EA_PACKAGES = auto()
    THIN_EA_DIAGRAMS = auto()
    THIN_EA_CONNECTORS = auto()
    THIN_EA_STEREOTYPES = auto()
    THIN_EA_ATTRIBUTES = auto()
    THIN_EA_ELEMENT_COMPONENTS = auto()
    THIN_EA_OPERATIONS = auto()
    EA_DIAGRAMS = auto()
    EA_STEREOTYPE_GROUPS = auto()
    EA_OPERATIONS = auto()
    EA_OBJECT_STEREOTYPES = auto()
    EA_CONNECTOR_TYPES = auto()
    EA_ELEMENT_TYPES = auto()
    EA_DIAGRAM_TYPES = auto()
    EA_CARDINALITIES = auto()
    EA_FULL_GENERALISATIONS = auto()
    EA_FULL_DEPENDENCIES = auto()
    EA_NEAREST_PACKAGES = auto()
    EA_FULL_PACKAGES = auto()
    EA_PACKAGE_CONTENTS_SUMMARY = auto()
    SUMMARY_TABLE_BY_TYPE = auto()
    DEPENDENCY_DEPTHS_TABLE = auto()
    ANALYSIS_METRICS = auto()
    # From model stats code
    MODEL_STATS_GENERAL_CONNECTORS_BY_TYPE = (
        auto()
    )
    MODEL_STATS_GENERAL_EDGES = auto()
    MODEL_STATS_GENERAL_LEAVES = auto()
    MODEL_STATS_GENERAL_NODES = auto()
    MODEL_STATS_GENERAL_OBJECTS_BY_TYPE = (
        auto()
    )
    MODEL_STATS_GENERAL_PATHS = auto()
    MODEL_STATS_GENERAL_ROOTS = auto()
    MODEL_STATS_GENERAL_SUMMARY_TABLE = (
        auto()
    )

    MODEL_STATS_PROXY_PROCESS_CONNECTORS_BY_TYPE = (
        auto()
    )
    MODEL_STATS_PROXY_PROCESS_EDGES = (
        auto()
    )
    MODEL_STATS_PROXY_PROCESS_LEAVES = (
        auto()
    )
    MODEL_STATS_PROXY_PROCESS_NODES = (
        auto()
    )
    MODEL_STATS_PROXY_PROCESS_OBJECTS_BY_TYPE = (
        auto()
    )
    MODEL_STATS_PROXY_PROCESS_PATHS = (
        auto()
    )
    MODEL_STATS_PROXY_PROCESS_ROOTS = (
        auto()
    )
    MODEL_STATS_PROXY_PROCESS_SUMMARY_TABLE = (
        auto()
    )

    MODEL_STATS_FULL_DEPENDENCIES_EDGES = (
        auto()
    )
    MODEL_STATS_FULL_DEPENDENCIES_LEAVES = (
        auto()
    )
    MODEL_STATS_FULL_DEPENDENCIES_NODES = (
        auto()
    )
    MODEL_STATS_FULL_DEPENDENCIES_PATHS = (
        auto()
    )
    MODEL_STATS_FULL_DEPENDENCIES_ROOTS = (
        auto()
    )
    MODEL_STATS_FULL_DEPENDENCIES_SUMMARY_TABLE = (
        auto()
    )

    MODEL_STATS_FIRST_CLASS_RELATION_EDGES = (
        auto()
    )
    MODEL_STATS_FIRST_CLASS_RELATION_LEAVES = (
        auto()
    )
    MODEL_STATS_FIRST_CLASS_RELATION_NODES = (
        auto()
    )
    MODEL_STATS_FIRST_CLASS_RELATION_ROOTS = (
        auto()
    )
    MODEL_STATS_FIRST_CLASS_RELATION_IMPLICIT_EDGES = (
        auto()
    )

    MODEL_STATS_HIGH_ORDER_TYPES_EDGES = (
        auto()
    )
    MODEL_STATS_HIGH_ORDER_TYPES_LEAVES = (
        auto()
    )
    MODEL_STATS_HIGH_ORDER_TYPES_NODES = (
        auto()
    )
    MODEL_STATS_HIGH_ORDER_TYPES_ROOTS = (
        auto()
    )
    MODEL_STATS_HIGH_ORDER_TYPES_IMPLICIT_EDGES = (
        auto()
    )

    @staticmethod
    def get_collection_type_from_name(
        name: str,
    ):
        for (
            collection_type,
            collection_name,
        ) in (
            collection_name_mapping.items()
        ):
            if collection_name == name:
                return collection_type

    def __collection_name(self) -> str:
        collection_name = (
            collection_name_mapping[
                self
            ]
        )

        return collection_name

    collection_name = property(
        fget=__collection_name
    )


collection_name_mapping = {
    NfEaComCollectionTypes.EA_PACKAGES: "ea_packages",
    NfEaComCollectionTypes.EA_CLASSIFIERS: "ea_classifiers",
    NfEaComCollectionTypes.EA_ATTRIBUTES: "ea_attributes",
    NfEaComCollectionTypes.EA_CONNECTORS: "ea_connectors",
    NfEaComCollectionTypes.EA_CONNECTORS_PC: "ea_connectors_pc",
    NfEaComCollectionTypes.EA_STEREOTYPES: "ea_stereotypes",
    NfEaComCollectionTypes.STEREOTYPE_USAGE: "stereotype_usage",
    NfEaComCollectionTypes.THIN_EA_EXPLICIT_OBJECTS: "thin_ea_explicit_objects",
    NfEaComCollectionTypes.THIN_EA_REPOSITORIED_OBJECTS: "thin_ea_repositoried_objects",
    NfEaComCollectionTypes.THIN_EA_STEREOTYPEABLE_OBJECTS: "thin_ea_stereotypeable_objects",
    NfEaComCollectionTypes.THIN_EA_PACKAGEABLE_OBJECTS: "thin_ea_packageable_objects",
    NfEaComCollectionTypes.THIN_EA_ELEMENTS: "thin_ea_elements",
    NfEaComCollectionTypes.THIN_EA_CLASSIFIERS: "thin_ea_classifiers",
    NfEaComCollectionTypes.THIN_EA_PACKAGES: "thin_ea_packages",
    NfEaComCollectionTypes.THIN_EA_DIAGRAMS: "thin_ea_diagrams",
    NfEaComCollectionTypes.THIN_EA_CONNECTORS: "thin_ea_connectors",
    NfEaComCollectionTypes.THIN_EA_STEREOTYPES: "thin_ea_stereotypes",
    NfEaComCollectionTypes.THIN_EA_ATTRIBUTES: "thin_ea_attributes",
    NfEaComCollectionTypes.THIN_EA_ELEMENT_COMPONENTS: "thin_ea_element_components",
    NfEaComCollectionTypes.THIN_EA_OPERATIONS: "thin_ea_operations",
    NfEaComCollectionTypes.EA_DIAGRAMS: "ea_diagrams",
    NfEaComCollectionTypes.EA_STEREOTYPE_GROUPS: "ea_stereotype_groups",
    NfEaComCollectionTypes.EA_OPERATIONS: "ea_operations",
    NfEaComCollectionTypes.EA_OBJECT_STEREOTYPES: "ea_object_stereotypes",
    NfEaComCollectionTypes.EA_CONNECTOR_TYPES: "ea_connector_types",
    NfEaComCollectionTypes.EA_ELEMENT_TYPES: "ea_element_types",
    NfEaComCollectionTypes.EA_DIAGRAM_TYPES: "ea_diagram_types",
    NfEaComCollectionTypes.EA_CARDINALITIES: "ea_cardinalities",
    NfEaComCollectionTypes.EA_FULL_GENERALISATIONS: "ea_full_generalisations",
    NfEaComCollectionTypes.EA_FULL_DEPENDENCIES: "ea_full_dependencies",
    NfEaComCollectionTypes.EA_NEAREST_PACKAGES: "ea_nearest_packages",
    NfEaComCollectionTypes.EA_FULL_PACKAGES: "ea_full_packages",
    NfEaComCollectionTypes.EA_PACKAGE_CONTENTS_SUMMARY: "ea_package_contents_summary",
    NfEaComCollectionTypes.SUMMARY_TABLE_BY_TYPE: "summary_table_by_type",
    NfEaComCollectionTypes.DEPENDENCY_DEPTHS_TABLE: "dependency_depths_table",
    NfEaComCollectionTypes.ANALYSIS_METRICS: "analysis_metrics",
    # From model stats code
    NfEaComCollectionTypes.MODEL_STATS_GENERAL_CONNECTORS_BY_TYPE: "general_connector_by_type",
    NfEaComCollectionTypes.MODEL_STATS_GENERAL_EDGES: "general_edges",
    NfEaComCollectionTypes.MODEL_STATS_GENERAL_LEAVES: "general_leaves",
    NfEaComCollectionTypes.MODEL_STATS_GENERAL_NODES: "general_nodes",
    NfEaComCollectionTypes.MODEL_STATS_GENERAL_OBJECTS_BY_TYPE: "general_objects_by_type",
    NfEaComCollectionTypes.MODEL_STATS_GENERAL_PATHS: "general_paths",
    NfEaComCollectionTypes.MODEL_STATS_GENERAL_ROOTS: "general_roots",
    NfEaComCollectionTypes.MODEL_STATS_GENERAL_SUMMARY_TABLE: "general_summary_table",
    NfEaComCollectionTypes.MODEL_STATS_PROXY_PROCESS_CONNECTORS_BY_TYPE: "proxies_connector_by_type",
    NfEaComCollectionTypes.MODEL_STATS_PROXY_PROCESS_EDGES: "proxies_edges",
    NfEaComCollectionTypes.MODEL_STATS_PROXY_PROCESS_LEAVES: "proxies_leaves",
    NfEaComCollectionTypes.MODEL_STATS_PROXY_PROCESS_NODES: "proxies_nodes",
    NfEaComCollectionTypes.MODEL_STATS_PROXY_PROCESS_OBJECTS_BY_TYPE: "proxies_objects_by_type",
    NfEaComCollectionTypes.MODEL_STATS_PROXY_PROCESS_PATHS: "proxies_paths",
    NfEaComCollectionTypes.MODEL_STATS_PROXY_PROCESS_ROOTS: "proxies_roots",
    NfEaComCollectionTypes.MODEL_STATS_PROXY_PROCESS_SUMMARY_TABLE: "proxies_summary_table",
    NfEaComCollectionTypes.MODEL_STATS_FULL_DEPENDENCIES_EDGES: "full_dependencies_edges",
    NfEaComCollectionTypes.MODEL_STATS_FULL_DEPENDENCIES_LEAVES: "full_dependencies_leaves",
    NfEaComCollectionTypes.MODEL_STATS_FULL_DEPENDENCIES_NODES: "full_dependencies_nodes",
    NfEaComCollectionTypes.MODEL_STATS_FULL_DEPENDENCIES_PATHS: "full_dependencies_paths",
    NfEaComCollectionTypes.MODEL_STATS_FULL_DEPENDENCIES_ROOTS: "full_dependencies_roots",
    NfEaComCollectionTypes.MODEL_STATS_FULL_DEPENDENCIES_SUMMARY_TABLE: "full_dependencies_summary_table",
    NfEaComCollectionTypes.MODEL_STATS_FIRST_CLASS_RELATION_EDGES: "FCR_edges",
    NfEaComCollectionTypes.MODEL_STATS_FIRST_CLASS_RELATION_LEAVES: "FCR_leaves",
    NfEaComCollectionTypes.MODEL_STATS_FIRST_CLASS_RELATION_NODES: "FCR_nodes",
    NfEaComCollectionTypes.MODEL_STATS_FIRST_CLASS_RELATION_ROOTS: "FCR_roots",
    NfEaComCollectionTypes.MODEL_STATS_FIRST_CLASS_RELATION_IMPLICIT_EDGES: "FCR_implicit_edges",
    NfEaComCollectionTypes.MODEL_STATS_HIGH_ORDER_TYPES_EDGES: "HOT_edges",
    NfEaComCollectionTypes.MODEL_STATS_HIGH_ORDER_TYPES_LEAVES: "HOT_leaves",
    NfEaComCollectionTypes.MODEL_STATS_HIGH_ORDER_TYPES_NODES: "HOT_nodes",
    NfEaComCollectionTypes.MODEL_STATS_HIGH_ORDER_TYPES_ROOTS: "HOT_roots",
    NfEaComCollectionTypes.MODEL_STATS_HIGH_ORDER_TYPES_IMPLICIT_EDGES: "HOT_implicit_edges",
}
