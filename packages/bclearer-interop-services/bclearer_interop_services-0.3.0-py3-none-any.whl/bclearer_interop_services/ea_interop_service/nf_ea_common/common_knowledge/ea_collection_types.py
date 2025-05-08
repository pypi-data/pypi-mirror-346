from enum import auto, unique

from bclearer_core.nf.types.collection_types import (
    CollectionTypes,
)


@unique
class EaCollectionTypes(
    CollectionTypes
):
    NOT_SET = auto()
    T_OBJECT = auto()
    T_CONNECTOR = auto()
    T_PACKAGE = auto()
    T_ATTRIBUTE = auto()
    T_XREF = auto()
    T_STEREOTYPES = auto()
    T_DIAGRAM = auto()
    T_DIAGRAMLINKS = auto()
    T_DIAGRAMOBJECTS = auto()
    T_OPERATION = auto()
    T_CONNECTORTYPES = auto()
    T_OBJECTTYPES = auto()
    T_DIAGRAMTYPES = auto()
    T_CARDINALITY = auto()
    EXTENDED_T_OBJECT = auto()
    EXTENDED_T_CONNECTOR = auto()
    EXTENDED_T_PACKAGE = auto()
    EXTENDED_T_ATTRIBUTE = auto()
    EXTENDED_T_OPERATION = auto()
    EXTENDED_T_XREF = auto()
    EXTENDED_T_STEREOTYPES = auto()
    EXTENDED_T_DIAGRAM = auto()
    EXTENDED_T_DIAGRAMLINKS = auto()
    EXTENDED_T_DIAGRAMOBJECTS = auto()
    EXTENDED_T_CONNECTORTYPES = auto()
    EXTENDED_T_OBJECTTYPES = auto()
    EXTENDED_T_DIAGRAMTYPES = auto()
    EXTENDED_T_CARDINALITY = auto()
    OBJECT_STEREOTYPES = auto()
    PACKAGE_HIERARCHY = auto()

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
    EaCollectionTypes.T_OBJECT: "t_object",
    EaCollectionTypes.T_CONNECTOR: "t_connector",
    EaCollectionTypes.T_PACKAGE: "t_package",
    EaCollectionTypes.T_ATTRIBUTE: "t_attribute",
    EaCollectionTypes.T_OPERATION: "t_operation",
    EaCollectionTypes.T_XREF: "t_xref",
    EaCollectionTypes.T_STEREOTYPES: "t_stereotypes",
    EaCollectionTypes.T_DIAGRAM: "t_diagram",
    EaCollectionTypes.T_DIAGRAMLINKS: "t_diagramlinks",
    EaCollectionTypes.T_DIAGRAMOBJECTS: "t_diagramobjects",
    EaCollectionTypes.T_CONNECTORTYPES: "t_connectortypes",
    EaCollectionTypes.T_OBJECTTYPES: "t_objecttypes",
    EaCollectionTypes.T_DIAGRAMTYPES: "t_diagramtypes",
    EaCollectionTypes.T_CARDINALITY: "t_cardinality",
    EaCollectionTypes.EXTENDED_T_OBJECT: "extended_t_object",
    EaCollectionTypes.EXTENDED_T_CONNECTOR: "extended_t_connector",
    EaCollectionTypes.EXTENDED_T_PACKAGE: "extended_t_package",
    EaCollectionTypes.EXTENDED_T_ATTRIBUTE: "extended_t_attribute",
    EaCollectionTypes.EXTENDED_T_OPERATION: "extended_t_operation",
    EaCollectionTypes.EXTENDED_T_XREF: "extended_t_xref",
    EaCollectionTypes.EXTENDED_T_STEREOTYPES: "extended_t_stereotypes",
    EaCollectionTypes.EXTENDED_T_DIAGRAM: "extended_t_diagram",
    EaCollectionTypes.EXTENDED_T_DIAGRAMLINKS: "extended_t_diagramlinks",
    EaCollectionTypes.EXTENDED_T_DIAGRAMOBJECTS: "extended_t_diagramobjects",
    EaCollectionTypes.EXTENDED_T_CONNECTORTYPES: "extended_t_connectortypes",
    EaCollectionTypes.EXTENDED_T_OBJECTTYPES: "extended_t_objecttypes",
    EaCollectionTypes.EXTENDED_T_DIAGRAMTYPES: "extended_t_diagramtypes",
    EaCollectionTypes.EXTENDED_T_CARDINALITY: "extended_t_cardinality",
    EaCollectionTypes.OBJECT_STEREOTYPES: "object_stereotypes",
    EaCollectionTypes.PACKAGE_HIERARCHY: "package_hierarchy",
}
