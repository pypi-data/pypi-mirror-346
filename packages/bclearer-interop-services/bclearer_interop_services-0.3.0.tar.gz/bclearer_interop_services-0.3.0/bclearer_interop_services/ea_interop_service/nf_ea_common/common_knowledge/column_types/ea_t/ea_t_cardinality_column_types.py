from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_column_types import (
    EaTColumnTypes,
)


@unique
class EaTCardinalityColumnTypes(
    EaTColumnTypes
):
    T_CARDINALITY_CARDINALITY = auto()

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
    EaTCardinalityColumnTypes.T_CARDINALITY_CARDINALITY: "Cardinality"
}


nf_column_name_mapping = {
    EaTCardinalityColumnTypes.T_CARDINALITY_CARDINALITY: "t_cardinality_cardinality"
}
