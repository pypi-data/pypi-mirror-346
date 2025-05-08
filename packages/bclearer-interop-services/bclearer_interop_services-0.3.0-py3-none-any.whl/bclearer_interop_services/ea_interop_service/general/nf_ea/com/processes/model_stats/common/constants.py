from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.nf_domains.standard_object_table_column_types import (
    StandardObjectTableColumnTypes,
)

ROOT_OUTPUT_FOLDER_TITLE_MESSAGE = (
    "Please select root output folder"
)

NF_UUIDS_COLUMN_NAME = "nf_uuids"
NF_UUIDS2_COLUMN_NAME = "nf_uuids2"


UUID_COLUMN_NAME = (
    StandardObjectTableColumnTypes.NF_UUIDS.column_name
)
CONTAINED_EA_PACKAGES_COLUMN_NAME = (
    "contained_ea_packages"
)
EA_OBJECT_TYPE_COLUMN_NAME = (
    "ea_object_type"
)

EA_CONNECTOR_ELEMENT_TYPE_NAME_COLUMN_NAME = (
    "ea_connector_element_type_name"
)

SUPPLIER_PLACE1_END_CONNECTORS_COLUMN_NAME = (
    "supplier_place1_end_connectors"
)
CLIENT_PLACE2_END_CONNECTORS_COLUMN_NAME = (
    "client_place2_end_connectors"
)
CONTAINED_EA_DIAGRAMS_COLUMN_NAME = (
    "contained_ea_diagrams"
)
CONTAINED_EA_CLASSIFIERS_COLUMN_NAME = (
    "contained_ea_classifiers"
)
CLASSIFIER_COLUMN_NAME = "classifier"
PARENT_EA_ELEMENT_COLUMN_NAME = (
    "parent_ea_element"
)
PARENT_EA_ELEMENT1_COLUMN_NAME = (
    "parent_ea_element1"
)
PARENT_EA_ELEMENT_NAME_COLUMN_NAME = (
    "parent_ea_element_name"
)
EA_OBJECT_STEREOTYPES_COLUMN_NAME = (
    "ea_object_stereotypes"
)
EA_REPOSITORY_COLUMN_NAME = (
    "ea_repository"
)
EA_OBJECT_NAME_COLUMN_NAME = (
    "ea_object_name"
)
EA_OBJECT_NOTES_COLUMN_NAME = (
    "ea_object_notes"
)
EA_GUID_COLUMN_NAME = "ea_guid"

# EA MODEL TABLE NAMES

EA_CLASSIFIERS_TABLE_NAME = (
    "ea_classifiers"
)
EA_FULL_DEPENDENCIES_TABLE_NAME = (
    "ea_full_dependencies"
)

# EA MODEL TABLES COLUMN NAMES

PROVIDER_COLUMN_NAME = "provider"
DEPENDENT_COLUMN_NAME = "dependent"
SOURCE_COLUMN_NAME = "source"
TARGET_COLUMN_NAME = "target"
SOURCE_NAME_COLUMN_NAME = "source_name"
TARGET_NAME_COLUMN_NAME = "target_name"
STEREOTYPE_NAMES_COLUMN_NAME = (
    "stereotype_names"
)
PACKAGE_NAMES_COLUMN_NAME = (
    "package_names"
)


HIGHER_RELATIONS_TABLE_NAME = (
    "higher_relations_table"
)

FIRST_CLASS_RELATIONS_TABLE_NAME = (
    "first_class_relations_table"
)

DATA_VISUALIZATION_HIGHER_RELATIONS_NAME = "data_visualization_higher_relations"

DATA_VISUALIZATION_FIRST_CLASS_RELATIONS_NAME = "data_visualization_first_class_relations"

DATA_VISUALIZATION_NAME = (
    "data_visualisation"
)

EA_TABLES_NAME = "ea_tables"

EA_MODEL_TABLES_INPUT_FOLDER_TITLE = "Please select ea model tables folder"

EA_CONNECTORS_TABLE_NAME = (
    "ea_connectors"
)

PROXYCONNECTOR_TYPE_NAME = (
    "ProxyConnector"
)

ASSOCIATION_TYPE_NAME = "Association"

CLASS_TYPE_NAME = "Class"

PATHS_COLUMN_NAME = "paths"

PATH_LEVEL_DEPTH_COLUMN_NAME = (
    "path_level_depth"
)

LEAVES_COLUMN_NAME = "leaves"

FULL_DEPENDENCIES_SUMMARY_TABLE_NAME = (
    "full_dependencies_summary_table"
)

LEAVES_MAX_DEPTH_COLUMN_NAME = (
    "leaves_max_depth"
)

LEAVES_NAME_COLUMN_NAME = "leaves_name"

LEAVES_TYPE_COLUMN_NAME = "leaves_type"

RELATION_TYPE_COLUMN_NAME = (
    "relation_type"
)

HIGH_ORDER_TYPE_RELATION_NAME = "HOT"

FIRST_CLASS_RELATION_NAME = "FCR"

OBJECT_TYPE_NAME = "Object"

FULL_DEPENDENCIES_NODES_TABLE_NAME = (
    "full_dependencies_nodes"
)
FULL_DEPENDENCIES_EDGES_TABLE_NAME = (
    "full_dependencies_edges"
)
FULL_DEPENDENCIES_LEAVES_TABLE_NAME = (
    "full_dependencies_leaves"
)
FULL_DEPENDENCIES_ROOTS_TABLE_NAME = (
    "full_dependencies_roots"
)
FULL_DEPENDENCIES_PATHS_TABLE_NAME = (
    "full_dependencies_paths"
)
FULL_DEPENDENCIES_OBJECTS_BY_TYPE_TABLE_NAME = (
    "full_dependencies_objects_by_type"
)

EDGES_SOURCE_COLUMN_NAME = (
    "edges_source"
)
EDGES_TARGET_COLUMN_NAME = (
    "edges_target"
)

HIGH_ORDER_TYPE_NODES_TABLE_NAME = (
    "high_order_type_nodes"
)

HIGH_ORDER_TYPE_EDGES_TABLE_NAME = (
    "high_order_type_edges"
)

HIGH_ORDER_TYPE_IMPLICIT_EDGES_TABLE_NAME = (
    "high_order_type_implicit_edges"
)

HIGH_ORDER_TYPE_lEAVES_TABLE_NAME = (
    "high_order_type_leaves"
)

HIGH_ORDER_TYPE_ROOTS_TABLE_NAME = (
    "high_order_type_roots"
)

HIGH_ORDER_TYPE_TOTALS_COLUMN_NAME = (
    "high_order_type_totals"
)
HIGH_ORDER_TYPE_STATS_COLUMN_NAME = (
    "high_order_type_stats"
)

SUMMARY_TABLE_TABLE_NAME = (
    "summary_table"
)

NUMBER_OF_HOT_NODES_NAME = (
    "number_of_HOT_nodes"
)
NUMBER_OF_HOT_EDGES = (
    "number_of_HOT_edges"
)
NUMBER_OF_HOT_IMPLICIT_EDGES = (
    "number_of_HOT_implicit_edges"
)
NUMBER_OF_HOT_LEAVES = (
    "number_of_HOT_leaves"
)
NUMBER_OF_HOT_ROOTS = (
    "number_of_HOT_roots"
)
HOT_PATH_LEVEL_MAX_DEPTH = (
    "HOT_path_level_max_depth"
)
HOT_LEAVES_MAX_DEPTH = (
    "HOT_leaves_max_depth"
)

EDGE_SOURCE_COLUMN_NAME = "edge_source"
EDGE_TARGET_COLUMN_NAME = "edge_target"

FULL_DEPENDENCIES_NAME = (
    "full_dependencies"
)

FULL_DEPENDENCIES_NUMBER_OF_NODES = (
    "full_dependencies_number_of_nodes"
)
FULL_DEPENDENCIES_NUMBER_OF_EDGES = (
    "full_dependencies_number_of_edges"
)
FULL_DEPENDENCIES_NUMBER_OF_LEAVES = (
    "full_dependencies_number_of_leaves"
)
FULL_DEPENDENCIES_NUMBER_OF_ROOTS = (
    "full_dependencies_number_of_roots"
)
FULL_DEPENDENCIES_NUMBER_OF_PATHS = (
    "full_dependencies_number_of_paths"
)
STATS_COLUMN_NAME = "Stats"
TOTALS_COLUMN_NAME = "Totals"

FIRST_CLASS_RELATION_NODES_TABLE_NAME = (
    "first_class_relation_nodes"
)

FIRST_CLASS_RELATION_EDGES_TABLE_NAME = (
    "first_class_relation_edges"
)

IMPLICIT_EDGES_TABLE_NAME = (
    "implicit_edges"
)

FIRST_CLASS_RELATION_lEAVES_TABLE_NAME = (
    "first_class_relation_leaves"
)

FIRST_CLASS_RELATION_ROOTS_TABLE_NAME = (
    "first_class_relation_roots"
)

FIRST_CLASS_RELATION_TOTALS_COLUMN_NAME = (
    "first_class_relation_totals"
)

FIRST_CLASS_RELATION_STATS_COLUMN_NAME = (
    "first_class_relation_stats"
)

PATH_LEVEL_MAX_DEPTH = (
    "path_level_max_depth"
)

LEAVES_MAX_DEPTH = "leaves_max_depth"

FIRST_CLASS_RELATION_EDGES_SOURCE_COLUMN_NAME = (
    "first_class_relation_edges_source"
)

FIRST_CLASS_RELATION_EDGES_TARGET_COLUMN_NAME = (
    "first_class_relation_edges_target"
)

NUMBER_OF_NODES = "number_of_nodes"

NUMBER_OF_EDGES = "number_of_edges"

NUMBER_OF_CONNECTED_PROXIES_EDGES = (
    "number_of_connected_proxies_edges"
)

NUMBER_OF_IMPLICIT_EDGES = (
    "number_of_implicit_edges"
)

NUMBER_OF_LEAVES = "number_of_leaves"

NUMBER_OF_ROOTS = "number_of_roots"

NUMBER_OF_PATHS = "number_of_paths"

LEVEL_COLUMN_NAME = "level"

EDGES_TABLE_NAME = "edges"

NODES_COLUMN_NAME = "nodes"

ROOTS_COLUMN_NAME = "roots"

DEPENDENCY_NAME = "Dependency"

IMPLICIT_DEPENDENCY_NAME = (
    "implicit_dependency"
)

GENERAL_NAME = "general"

CONNECTED_PROXIES_NAME = "proxies"

OBJECTS_BY_TYPE_TABLE_NAME = (
    "objects_by_type"
)

CONNECTOR_BY_TYPE_TABLE_NAME = (
    "connector_by_type"
)

GENERAL_DATA_VISUALIZATION_NAME = (
    "general_data_visualization"
)

GENERAL_SUMMARY_TABLE_NAME = (
    NfEaComCollectionTypes.MODEL_STATS_GENERAL_SUMMARY_TABLE.collection_name
)

NODES_TABLE_NAME_SUFFIX = "_nodes"

EDGES_TABLE_NAME_SUFFIX = "_edges"

ROOTS_TABLE_NAME_SUFFIX = "_roots"

LEAVES_TABLE_NAME_SUFFIX = "_leaves"
