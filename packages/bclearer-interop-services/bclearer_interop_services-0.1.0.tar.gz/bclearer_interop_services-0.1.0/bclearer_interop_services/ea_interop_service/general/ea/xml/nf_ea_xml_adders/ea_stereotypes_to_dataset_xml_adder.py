from xml.etree.ElementTree import (
    Element,
)

from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_adders.nf_ea_xml_add_helpers import (
    add_xml_row_element_to_xml_data_reference_table_element,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_additional_column_types import (
    NfEaComAdditionalColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.maps.nf_uuids_to_ea_guids_mappings import (
    NfUuidsToEaGuidsMappings,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_stereotypes_column_types import (
    EaTStereotypesColumnTypes,
)
from bclearer_interop_services.tuple_service.tuple_attribute_value_getter import (
    get_tuple_attribute_value_if_required,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)
from pandas import DataFrame


def add_ea_stereotypes_to_dataset_xml_root_element(
    ea_stereotypes: DataFrame,
    xml_element_for_stereotypes_dataset: Element,
) -> Element:
    for (
        ea_stereotype_tuple
    ) in ea_stereotypes.itertuples():
        __add_ea_stereotype_to_xml_tree(
            ea_stereotype_tuple=ea_stereotype_tuple,
            xml_element_for_stereotypes_dataset=xml_element_for_stereotypes_dataset,
        )

    return xml_element_for_stereotypes_dataset


def __add_ea_stereotype_to_xml_tree(
    ea_stereotype_tuple: tuple,
    xml_element_for_stereotypes_dataset: Element,
):
    ea_stereotype_nf_uuid = get_tuple_attribute_value_if_required(
        owning_tuple=ea_stereotype_tuple,
        attribute_name=NfColumnTypes.NF_UUIDS.column_name,
    )

    original_ea_guid = get_tuple_attribute_value_if_required(
        owning_tuple=ea_stereotype_tuple,
        attribute_name=NfEaComAdditionalColumnTypes.ORIGINAL_EA_GUIDS.column_name,
    )

    ea_stereotype_name = get_tuple_attribute_value_if_required(
        owning_tuple=ea_stereotype_tuple,
        attribute_name=NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name,
    )

    ea_stereotype_notes = get_tuple_attribute_value_if_required(
        owning_tuple=ea_stereotype_tuple,
        attribute_name=NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name,
    )

    ea_stereotype_applies_to = get_tuple_attribute_value_if_required(
        owning_tuple=ea_stereotype_tuple,
        attribute_name=NfEaComColumnTypes.STEREOTYPE_APPLIES_TOS.column_name,
    )

    ea_stereotype_style = get_tuple_attribute_value_if_required(
        owning_tuple=ea_stereotype_tuple,
        attribute_name=NfEaComColumnTypes.STEREOTYPE_STYLE.column_name,
    )

    if (
        original_ea_guid
        == DEFAULT_NULL_VALUE
    ):
        ea_stereotype_guid = (
            "{"
            + create_new_uuid()
            + "}"
        )

    else:
        ea_stereotype_guid = (
            original_ea_guid
        )

    if (
        ea_stereotype_name
        == DEFAULT_NULL_VALUE
    ):
        ea_stereotype_name = ""

    if (
        ea_stereotype_notes
        == DEFAULT_NULL_VALUE
    ):
        ea_stereotype_notes = ""

    names_to_values_map = {
        EaTStereotypesColumnTypes.T_STEREOTYPES_EA_GUIDS.column_name: ea_stereotype_guid,
        EaTStereotypesColumnTypes.T_STEREOTYPES_NAMES.column_name: ea_stereotype_name,
        EaTStereotypesColumnTypes.T_STEREOTYPES_DESCRIPTIONS.column_name: ea_stereotype_notes,
        EaTStereotypesColumnTypes.T_STEREOTYPES_APPLIES_TOS.column_name: ea_stereotype_applies_to,
        EaTStereotypesColumnTypes.T_STEREOTYPES_STYLES.column_name: ea_stereotype_style,
        EaTStereotypesColumnTypes.T_STEREOTYPES_MF_ENABLED.column_name: "FALSE",
    }

    add_xml_row_element_to_xml_data_reference_table_element(
        xml_element_for_table=xml_element_for_stereotypes_dataset,
        xml_column_names_to_values_map=names_to_values_map,
    )

    if (
        ea_stereotype_nf_uuid
        != DEFAULT_NULL_VALUE
    ):
        NfUuidsToEaGuidsMappings.add_single_map(
            nf_uuid=ea_stereotype_nf_uuid,
            ea_guid=ea_stereotype_guid,
        )
