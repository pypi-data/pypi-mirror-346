from bclearer_core.nf.python_extensions.collections.nf_bimappings import (
    NfBimappings,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.nf_domains.standard_attribute_table_column_types import (
    StandardAttributeTableColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.nf_domains.standard_object_table_column_types import (
    StandardObjectTableColumnTypes,
)


def get_standard_attribute_to_nf_ea_com_column_name_dictionary() -> (
    dict
):
    standard_attribute_to_nf_ea_com_column_name_dictionary = (
        __standard_attribute_to_nf_ea_com_column_name_bimapping.get_range_keyed_on_domain()
    )

    return standard_attribute_to_nf_ea_com_column_name_dictionary


def get_nf_ea_com_column_name_to_standard_attribute_dictionary() -> (
    dict
):
    nf_ea_com_column_name_to_standard_attribute_dictionary = (
        __standard_attribute_to_nf_ea_com_column_name_bimapping.get_domain_keyed_on_range()
    )

    return nf_ea_com_column_name_to_standard_attribute_dictionary


__standard_attribute_to_nf_ea_com_column_name_bimapping = NfBimappings(
    map={
        StandardObjectTableColumnTypes.NF_UUIDS.column_name: NfColumnTypes.NF_UUIDS.column_name,
        StandardObjectTableColumnTypes.UML_OBJECT_NAMES.column_name: NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name,
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name: NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name,
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name: NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name,
        StandardAttributeTableColumnTypes.ATTRIBUTED_OBJECT_UUIDS.column_name: NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name,
        StandardAttributeTableColumnTypes.ATTRIBUTE_TYPE_UUIDS.column_name: NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name,
        StandardAttributeTableColumnTypes.UML_VISIBILITY_KIND.column_name: NfEaComColumnTypes.ELEMENT_COMPONENTS_UML_VISIBILITY_KIND.column_name,
        StandardAttributeTableColumnTypes.ATTRIBUTE_TYPE_NAMES.column_name: NfEaComColumnTypes.ELEMENT_COMPONENTS_TYPE.column_name,
        StandardAttributeTableColumnTypes.ATTRIBUTE_VALUES.column_name: NfEaComColumnTypes.ELEMENT_COMPONENTS_DEFAULT.column_name,
    }
)
