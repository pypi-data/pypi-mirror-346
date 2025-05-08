from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_column_types import (
    EaTColumnTypes,
)


@unique
class EaTObjectTypesColumnTypes(
    EaTColumnTypes
):
    T_OBJECTTYPES_OBJECT_TYPES = auto()
    T_OBJECTTYPES_DESCRIPTIONS = auto()
    T_OBJECTTYPES_DESIGN_OBJECTS = (
        auto()
    )
    T_OBJECTTYPES_IMAGE_IDS = auto()

    def __column_name(self) -> str:
        column_name = (
            column_name_mapping[self]
        )

        return column_name

    def __nf_column_name(self) -> str:
        nf_column_name = (
            nf_column_name_mapping[self]
        )

        return nf_column_name

    column_name = property(
        fget=__column_name
    )

    nf_column_name = property(
        fget=__nf_column_name
    )


column_name_mapping = {
    EaTObjectTypesColumnTypes.T_OBJECTTYPES_OBJECT_TYPES: "Object_Type",
    EaTObjectTypesColumnTypes.T_OBJECTTYPES_DESCRIPTIONS: "Description",
    EaTObjectTypesColumnTypes.T_OBJECTTYPES_DESIGN_OBJECTS: "DesignObject",
    EaTObjectTypesColumnTypes.T_OBJECTTYPES_IMAGE_IDS: "ImageID",
}


nf_column_name_mapping = {
    EaTObjectTypesColumnTypes.T_OBJECTTYPES_OBJECT_TYPES: "t_objecttypes_object_types",
    EaTObjectTypesColumnTypes.T_OBJECTTYPES_DESCRIPTIONS: "t_objecttypes_descriptions",
    EaTObjectTypesColumnTypes.T_OBJECTTYPES_DESIGN_OBJECTS: "t_objecttypes_design_objects",
    EaTObjectTypesColumnTypes.T_OBJECTTYPES_IMAGE_IDS: "t_objecttypes_image_ids",
}
