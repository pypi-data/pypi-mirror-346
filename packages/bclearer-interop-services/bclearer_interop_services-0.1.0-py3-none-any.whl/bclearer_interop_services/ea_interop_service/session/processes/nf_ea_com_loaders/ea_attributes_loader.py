from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.ea_interop_service.factories.i_dual_attribute_factory import (
    create_i_dual_attribute,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.maps.nf_uuids_to_com_objects_mappings import (
    NfUuidsToIDualObjectsMappings,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.attributes.i_dual_attribute import (
    IDualAttribute,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_dual_element import (
    IDualElement,
)
from pandas import DataFrame
from tqdm import tqdm


def load_ea_attributes(
    ea_attributes: DataFrame,
):
    ea_guid_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    name_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
    )

    classifying_ea_classifier_column_name = (
        NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name
    )

    containing_ea_classifier_column_name = (
        NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name
    )

    ea_attribute_type_name_column_name = (
        NfEaComColumnTypes.ELEMENT_COMPONENTS_TYPE.column_name
    )

    ea_attribute_initial_value_column_name = (
        NfEaComColumnTypes.ELEMENT_COMPONENTS_DEFAULT.column_name
    )

    for index, ea_attribute_row in tqdm(
        ea_attributes.iterrows(),
        total=ea_attributes.shape[0],
    ):
        ea_attribute = __load_ea_attribute(
            ea_attribute_name=ea_attribute_row[
                name_column_name
            ],
            ea_attribute_type_nf_uuid=ea_attribute_row[
                classifying_ea_classifier_column_name
            ],
            attributed_object_nf_uuid=ea_attribute_row[
                containing_ea_classifier_column_name
            ],
            ea_attribute_type_name=ea_attribute_row[
                ea_attribute_type_name_column_name
            ],
            ea_attribute_initial_value=ea_attribute_row[
                ea_attribute_initial_value_column_name
            ],
        )

        ea_attributes.at[
            index, ea_guid_column_name
        ] = ea_attribute.attribute_guid

    return ea_attributes


def __load_ea_attribute(
    ea_attribute_name: str,
    ea_attribute_type_nf_uuid: str,
    attributed_object_nf_uuid: str,
    ea_attribute_type_name: str,
    ea_attribute_initial_value: str,
) -> IDualAttribute:
    attributed_object = NfUuidsToIDualObjectsMappings.get_i_dual_element(
        nf_uuid=attributed_object_nf_uuid
    )

    if not isinstance(
        attributed_object, IDualElement
    ):
        raise TypeError

    registered_i_dual_element_nf_uuids = (
        NfUuidsToIDualObjectsMappings.get_nf_uuids_for_i_dual_elements()
    )

    if (
        ea_attribute_type_nf_uuid
        in registered_i_dual_element_nf_uuids
    ):
        attribute_type = NfUuidsToIDualObjectsMappings.get_i_dual_element(
            nf_uuid=ea_attribute_type_nf_uuid
        )

        if not isinstance(
            attribute_type, IDualElement
        ):
            raise TypeError

    else:
        attribute_type = None

    if (
        ea_attribute_initial_value
        == DEFAULT_NULL_VALUE
    ):
        ea_attribute_initial_value = (
            None
        )

    ea_attribute = create_i_dual_attribute(
        attributed_object=attributed_object,
        attribute_name=ea_attribute_name,
        attribute_type=attribute_type,
        attribute_visibility="Public",
        ea_attribute_type_name=ea_attribute_type_name,
        ea_attribute_initial_value=ea_attribute_initial_value,
    )

    return ea_attribute
