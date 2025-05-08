from enum import auto, unique

from bclearer_core.nf.types.column_types import (
    ColumnTypes,
)


@unique
class NfEaComColumnTypes(ColumnTypes):
    CLASSIFIERS_ALL_COMPONENT_EA_ATTRIBUTES = (
        auto()
    )
    CLASSIFIERS_ALL_COMPONENT_EA_OPERATIONS = (
        auto()
    )
    CLASSIFIERS_CONTAINING_EA_ELEMENT = (
        auto()
    )
    ELEMENTS_EA_OBJECT_TYPE = auto()
    ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS = (
        auto()
    )
    ELEMENTS_CLIENT_PLACE2_END_CONNECTORS = (
        auto()
    )
    ELEMENTS_CONTAINED_EA_DIAGRAMS = (
        auto()
    )
    ELEMENTS_CONTAINED_EA_CLASSIFIERS = (
        auto()
    )
    ELEMENTS_CLASSIFIER = auto()
    EXPLICIT_OBJECTS_EA_OBJECT_NAME = (
        auto()
    )
    EXPLICIT_OBJECTS_EA_OBJECT_NOTES = (
        auto()
    )
    EXPLICIT_OBJECTS_EA_GUID = auto()
    PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT = (
        auto()
    )
    PACKAGES_CONTAINED_EA_PACKAGES = (
        auto()
    )
    PACKAGES_VIEW_TYPE = auto()
    REPOSITORIED_OBJECTS_EA_REPOSITORY = (
        auto()
    )
    STEREOTYPE_EA_STEREOTYPE_GROUP = (
        auto()
    )
    STEREOTYPEABLE_OBJECTS_EA_OBJECT_STEREOTYPES = (
        auto()
    )
    CONNECTORS_DIRECTION_TYPE_NAME = (
        auto()
    )
    CONNECTORS_ELEMENT_TYPE_NAME = (
        auto()
    )
    CONNECTORS_SOURCE_CARDINALITY = (
        auto()
    )
    CONNECTORS_DEST_CARDINALITY = auto()
    ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER = (
        auto()
    )
    ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER = (
        auto()
    )
    ELEMENT_COMPONENTS_UML_VISIBILITY_KIND = (
        auto()
    )
    ELEMENT_COMPONENTS_DEFAULT = auto()
    ELEMENT_COMPONENTS_TYPE = auto()
    ATTRIBUTES_LOWER_BOUNDS = auto()
    ATTRIBUTES_UPPER_BOUNDS = auto()
    ANALYSIS_METRICS_METRICS = auto()
    ANALYSIS_METRICS_VALUES = auto()
    STEREOTYPE_CLIENT_NF_UUIDS = auto()
    STEREOTYPE_NAMES = auto()
    STEREOTYPE_APPLIES_TOS = auto()
    STEREOTYPE_STYLE = auto()
    STEREOTYPE_PROPERTY_TYPE = auto()

    def __column_name(self) -> str:
        column_name = (
            column_name_mapping[self]
        )

        return column_name

    column_name = property(
        fget=__column_name
    )


column_name_mapping = {
    NfEaComColumnTypes.CLASSIFIERS_ALL_COMPONENT_EA_ATTRIBUTES: "all_component_ea_attributes",
    NfEaComColumnTypes.CLASSIFIERS_ALL_COMPONENT_EA_OPERATIONS: "all_component_ea_operations",
    NfEaComColumnTypes.CLASSIFIERS_CONTAINING_EA_ELEMENT: "containing_ea_element",
    NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE: "ea_object_type",
    NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS: "supplier_place1_end_connectors",
    NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS: "client_place2_end_connectors",
    NfEaComColumnTypes.ELEMENTS_CONTAINED_EA_DIAGRAMS: "contained_ea_diagrams",
    NfEaComColumnTypes.ELEMENTS_CONTAINED_EA_CLASSIFIERS: "contained_ea_classifiers",
    NfEaComColumnTypes.ELEMENTS_CLASSIFIER: "classifier",
    NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME: "ea_object_name",
    NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES: "ea_object_notes",
    NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID: "ea_guid",
    NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT: "parent_ea_element",
    NfEaComColumnTypes.PACKAGES_CONTAINED_EA_PACKAGES: "contained_ea_packages",
    NfEaComColumnTypes.PACKAGES_VIEW_TYPE: "view_type",
    NfEaComColumnTypes.REPOSITORIED_OBJECTS_EA_REPOSITORY: "ea_repository",
    NfEaComColumnTypes.STEREOTYPE_EA_STEREOTYPE_GROUP: "ea_stereotype_group",
    NfEaComColumnTypes.STEREOTYPEABLE_OBJECTS_EA_OBJECT_STEREOTYPES: "ea_object_stereotypes",
    NfEaComColumnTypes.CONNECTORS_DIRECTION_TYPE_NAME: "ea_connector_direction_type_name",
    NfEaComColumnTypes.CONNECTORS_ELEMENT_TYPE_NAME: "ea_connector_element_type_name",
    NfEaComColumnTypes.CONNECTORS_SOURCE_CARDINALITY: "ea_connector_supplier_cardinality",
    NfEaComColumnTypes.CONNECTORS_DEST_CARDINALITY: "ea_connector_client_cardinality",
    NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER: "containing_ea_classifier",
    NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER: "classifying_ea_classifier",
    NfEaComColumnTypes.ELEMENT_COMPONENTS_UML_VISIBILITY_KIND: "uml_visibility_kind",
    NfEaComColumnTypes.ELEMENT_COMPONENTS_DEFAULT: "default",
    NfEaComColumnTypes.ELEMENT_COMPONENTS_TYPE: "type",
    NfEaComColumnTypes.ATTRIBUTES_LOWER_BOUNDS: "lower_bounds",
    NfEaComColumnTypes.ATTRIBUTES_UPPER_BOUNDS: "upper_bounds",
    NfEaComColumnTypes.ANALYSIS_METRICS_METRICS: "metrics",
    NfEaComColumnTypes.ANALYSIS_METRICS_VALUES: "values",
    NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS: "client_nf_uuids",
    NfEaComColumnTypes.STEREOTYPE_NAMES: "stereotype_names",
    NfEaComColumnTypes.STEREOTYPE_APPLIES_TOS: "stereotype_applies_tos",
    NfEaComColumnTypes.STEREOTYPE_STYLE: "stereotype_style",
    NfEaComColumnTypes.STEREOTYPE_PROPERTY_TYPE: "property_type",
}
