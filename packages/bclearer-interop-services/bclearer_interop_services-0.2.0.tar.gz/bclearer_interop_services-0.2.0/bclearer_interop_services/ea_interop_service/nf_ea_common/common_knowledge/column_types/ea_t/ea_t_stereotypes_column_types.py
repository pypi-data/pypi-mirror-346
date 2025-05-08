from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_column_types import (
    EaTColumnTypes,
)


@unique
class EaTStereotypesColumnTypes(
    EaTColumnTypes
):
    T_STEREOTYPES_EA_GUIDS = auto()
    T_STEREOTYPES_NAMES = auto()
    T_STEREOTYPES_APPLIES_TOS = auto()
    T_STEREOTYPES_DESCRIPTIONS = auto()
    T_STEREOTYPES_STYLES = auto()
    T_STEREOTYPES_MF_ENABLED = auto()

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
    EaTStereotypesColumnTypes.T_STEREOTYPES_EA_GUIDS: "ea_guid",
    EaTStereotypesColumnTypes.T_STEREOTYPES_NAMES: "Stereotype",
    EaTStereotypesColumnTypes.T_STEREOTYPES_APPLIES_TOS: "AppliesTo",
    EaTStereotypesColumnTypes.T_STEREOTYPES_DESCRIPTIONS: "Description",
    EaTStereotypesColumnTypes.T_STEREOTYPES_STYLES: "Style",
    EaTStereotypesColumnTypes.T_STEREOTYPES_MF_ENABLED: "MFEnabled",
}


nf_column_name_mapping = {
    EaTStereotypesColumnTypes.T_STEREOTYPES_EA_GUIDS: "t_stereotypes_ea_guids",
    EaTStereotypesColumnTypes.T_STEREOTYPES_NAMES: "t_stereotypes_names",
    EaTStereotypesColumnTypes.T_STEREOTYPES_APPLIES_TOS: "t_stereotypes_applies_tos",
    EaTStereotypesColumnTypes.T_STEREOTYPES_DESCRIPTIONS: "t_stereotypes_descriptions",
    EaTStereotypesColumnTypes.T_STEREOTYPES_STYLES: "t_stereotypes_styles",
    EaTStereotypesColumnTypes.T_STEREOTYPES_MF_ENABLED: "t_stereotypes_mf_enabled",
}
