from enum import auto, unique

from bclearer_core.nf.types.column_types import (
    ColumnTypes,
)


@unique
class ExtendedTDiagramlinksColumnTypes(
    ColumnTypes
):
    T_DIAGRAMLINKS_COMPOSITE_EA_GUIDS = (
        auto()
    )
    T_DIAGRAMLINKS_EA_HUMAN_READABLE_NAMES = (
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
    ExtendedTDiagramlinksColumnTypes.T_DIAGRAMLINKS_COMPOSITE_EA_GUIDS: "t_diagramlinks_composite_ea_guids",
    ExtendedTDiagramlinksColumnTypes.T_DIAGRAMLINKS_EA_HUMAN_READABLE_NAMES: "t_diagramlinks_ea_human_readable_names",
}
