from enum import auto, unique

from bclearer_core.nf.types.column_types import (
    ColumnTypes,
)


@unique
class ExtendedTDiagramobjectsColumnTypes(
    ColumnTypes
):
    T_DIAGRAMOBJECTS_COMPOSITE_EA_GUIDS = (
        auto()
    )
    T_DIAGRAMOBJECTS_EA_HUMAN_READABLE_NAMES = (
        auto()
    )

    def __column_name(self) -> str:
        column_name = (
            column_name_mapping[self]
        )

        return column_name

    column_name = property(
        fget=__column_name
    )


column_name_mapping = {
    ExtendedTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_COMPOSITE_EA_GUIDS: "t_diagramobjects_composite_ea_guids",
    ExtendedTDiagramobjectsColumnTypes.T_DIAGRAMOBJECTS_EA_HUMAN_READABLE_NAMES: "t_diagramobjects_ea_human_readable_names",
}
