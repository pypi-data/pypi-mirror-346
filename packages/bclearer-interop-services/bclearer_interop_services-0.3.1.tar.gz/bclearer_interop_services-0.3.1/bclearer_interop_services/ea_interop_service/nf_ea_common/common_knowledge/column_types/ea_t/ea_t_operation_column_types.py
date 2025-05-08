from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_column_types import (
    EaTColumnTypes,
)


@unique
class EaTOperationColumnTypes(
    EaTColumnTypes
):
    T_OPERATION_IDS = auto()
    T_OPERATION_OBJECT_IDS = auto()
    T_OPERATION_NAMES = auto()
    T_OPERATION_TYPES = auto()
    T_OPERATION_STEREOTYPES = auto()
    T_OPERATION_NOTES = auto()
    T_OPERATION_CLASSIFIERS = auto()
    T_OPERATION_EA_GUIDS = auto()

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
    EaTOperationColumnTypes.T_OPERATION_IDS: "OperationID",
    EaTOperationColumnTypes.T_OPERATION_OBJECT_IDS: "Object_ID",
    EaTOperationColumnTypes.T_OPERATION_NAMES: "Name",
    EaTOperationColumnTypes.T_OPERATION_TYPES: "Type",
    EaTOperationColumnTypes.T_OPERATION_STEREOTYPES: "Stereotype",
    EaTOperationColumnTypes.T_OPERATION_NOTES: "Notes",
    EaTOperationColumnTypes.T_OPERATION_CLASSIFIERS: "Classifier",
    EaTOperationColumnTypes.T_OPERATION_EA_GUIDS: "ea_guid",
}


nf_column_name_mapping = {
    EaTOperationColumnTypes.T_OPERATION_IDS: "t_operation_ids",
    EaTOperationColumnTypes.T_OPERATION_OBJECT_IDS: "t_operation_object_ids",
    EaTOperationColumnTypes.T_OPERATION_NAMES: "t_operation_names",
    EaTOperationColumnTypes.T_OPERATION_TYPES: "t_operation_types",
    EaTOperationColumnTypes.T_OPERATION_STEREOTYPES: "t_operation_stereotypes",
    EaTOperationColumnTypes.T_OPERATION_NOTES: "t_operation_notes",
    EaTOperationColumnTypes.T_OPERATION_CLASSIFIERS: "t_operation_classifiers",
    EaTOperationColumnTypes.T_OPERATION_EA_GUIDS: "t_operation_ea_guids",
}
