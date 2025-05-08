from xml.etree.ElementTree import (
    Element,
)

from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.common_knowledge.maps.ea_guids_to_ea_identifiers_for_connectors_mappings import (
    EaGuidsToEaIdentifiersForConnectorsMappings,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.common_knowledge.maps.ea_guids_to_ea_identifiers_for_objects_mappings import (
    EaGuidsToEaIdentifiersForObjectsMappings,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.common_knowledge.maps.ea_guids_to_ea_identifiers_for_packages_mappings import (
    EaGuidsToEaIdentifiersForPackagesMappings,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_adders.nf_ea_xml_add_helpers import (
    add_xml_row_element_to_xml_table_element,
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
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_object_column_types import (
    EaTObjectColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_element_types import (
    EaElementTypes,
)
from bclearer_interop_services.tuple_service.tuple_attribute_value_getter import (
    get_tuple_attribute_value_if_required,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def add_ea_classifiers_to_xml_root_element(
    ea_classifiers: DataFrame,
    xml_root: Element,
    xml_element_for_classifiers: Element,
    start_ea_identifier: int,
    proxy_load: bool,
    stereotype_usage_with_names: DataFrame,
) -> tuple:
    classifier_column_name = (
        NfEaComColumnTypes.ELEMENTS_CLASSIFIER.column_name
    )

    non_classified_ea_classifiers = (
        ea_classifiers.loc[
            ea_classifiers[
                classifier_column_name
            ]
            == DEFAULT_NULL_VALUE
        ]
    )

    next_ea_identifier = (
        start_ea_identifier + 1
    )

    for (
        ea_classifier_tuple
    ) in (
        non_classified_ea_classifiers.itertuples()
    ):
        __add_ea_classifier_to_xml_tree(
            ea_classifier_tuple=ea_classifier_tuple,
            ea_classifier_identifier=next_ea_identifier,
            xml_element_for_classifiers=xml_element_for_classifiers,
            proxy_load=proxy_load,
            stereotype_usage_with_names=stereotype_usage_with_names,
        )

        next_ea_identifier += 1

    classified_ea_classifiers = (
        ea_classifiers.loc[
            ea_classifiers[
                classifier_column_name
            ]
            != DEFAULT_NULL_VALUE
        ]
    )

    for (
        ea_classifier_tuple
    ) in (
        classified_ea_classifiers.itertuples()
    ):
        __add_ea_classifier_to_xml_tree(
            ea_classifier_tuple=ea_classifier_tuple,
            ea_classifier_identifier=next_ea_identifier,
            xml_element_for_classifiers=xml_element_for_classifiers,
            proxy_load=proxy_load,
            stereotype_usage_with_names=stereotype_usage_with_names,
        )

        next_ea_identifier += 1

    return (
        xml_root,
        xml_element_for_classifiers,
    )


def __add_ea_classifier_to_xml_tree(
    ea_classifier_tuple: tuple,
    ea_classifier_identifier: int,
    xml_element_for_classifiers: Element,
    proxy_load: bool,
    stereotype_usage_with_names: DataFrame,
):
    ea_classifier_type = get_tuple_attribute_value_if_required(
        owning_tuple=ea_classifier_tuple,
        attribute_name=NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name,
    )

    if proxy_load:
        if (
            ea_classifier_type
            != EaElementTypes.PROXY_CONNECTOR.type_name
        ):
            return

    if not proxy_load:
        if (
            ea_classifier_type
            == EaElementTypes.PROXY_CONNECTOR.type_name
        ):
            return

    containing_ea_package_nf_uuid = get_tuple_attribute_value_if_required(
        owning_tuple=ea_classifier_tuple,
        attribute_name=NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name,
    )

    containing_ea_package_ea_guid = NfUuidsToEaGuidsMappings.get_ea_guid(
        containing_ea_package_nf_uuid
    )

    ea_package_parent_ea_identifier = EaGuidsToEaIdentifiersForPackagesMappings.map.get_ea_identifier(
        containing_ea_package_ea_guid
    )

    ea_classifier_note = get_tuple_attribute_value_if_required(
        owning_tuple=ea_classifier_tuple,
        attribute_name=NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name,
    )

    if (
        ea_classifier_note
        == DEFAULT_NULL_VALUE
    ):
        ea_classifier_note = ""

    ea_classifier_classifier_nf_uuid = get_tuple_attribute_value_if_required(
        owning_tuple=ea_classifier_tuple,
        attribute_name=NfEaComColumnTypes.ELEMENTS_CLASSIFIER.column_name,
    )

    if (
        ea_classifier_classifier_nf_uuid
        == DEFAULT_NULL_VALUE
    ):
        ea_classifier_classifier_ea_guid = (
            ""
        )

        ea_classifier_classifier_id = 0

    else:
        ea_classifier_classifier_ea_guid = NfUuidsToEaGuidsMappings.get_ea_guid(
            ea_classifier_classifier_nf_uuid
        )

        if (
            ea_classifier_classifier_ea_guid
            in EaGuidsToEaIdentifiersForObjectsMappings.map.get_map()
        ):
            ea_classifier_classifier_id = EaGuidsToEaIdentifiersForObjectsMappings.map.get_ea_identifier(
                ea_classifier_classifier_ea_guid
            )

        elif (
            ea_classifier_classifier_ea_guid
            in EaGuidsToEaIdentifiersForConnectorsMappings.map.get_map()
        ):
            ea_classifier_classifier_id = EaGuidsToEaIdentifiersForConnectorsMappings.map.get_ea_identifier(
                ea_classifier_classifier_ea_guid
            )

        else:
            log_message(
                "Cannot find identifier for classifier's classifier with guid "
                + str(
                    ea_classifier_classifier_ea_guid
                )
            )

            return

    original_ea_guid = get_tuple_attribute_value_if_required(
        owning_tuple=ea_classifier_tuple,
        attribute_name=NfEaComAdditionalColumnTypes.ORIGINAL_EA_GUIDS.column_name,
    )

    if (
        original_ea_guid
        == DEFAULT_NULL_VALUE
    ):
        ea_classifier_guid = (
            "{"
            + create_new_uuid()
            + "}"
        )

    else:
        ea_classifier_guid = (
            original_ea_guid
        )

    ea_classifier_nf_uuid = get_tuple_attribute_value_if_required(
        owning_tuple=ea_classifier_tuple,
        attribute_name=NfColumnTypes.NF_UUIDS.column_name,
    )

    stereotype_names = stereotype_usage_with_names[
        stereotype_usage_with_names[
            NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name
        ]
        == ea_classifier_nf_uuid
    ][
        NfEaComColumnTypes.STEREOTYPE_NAMES.column_name
    ].values

    if len(stereotype_names) == 0:
        stereotype_name = ""

    else:
        stereotype_name = (
            stereotype_names[0]
        )

    ea_classifier_name = get_tuple_attribute_value_if_required(
        owning_tuple=ea_classifier_tuple,
        attribute_name=NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name,
    )

    names_to_values_map = {
        EaTObjectColumnTypes.T_OBJECT_IDS.column_name: ea_classifier_identifier,
        EaTObjectColumnTypes.T_OBJECT_TYPES.column_name: ea_classifier_type,
        EaTObjectColumnTypes.T_OBJECT_NAMES.column_name: ea_classifier_name,
        EaTObjectColumnTypes.T_OBJECT_NOTES.column_name: ea_classifier_note,
        EaTObjectColumnTypes.T_OBJECT_PACKAGE_IDS.column_name: ea_package_parent_ea_identifier,
        EaTObjectColumnTypes.T_OBJECT_EA_GUIDS.column_name: ea_classifier_guid,
        EaTObjectColumnTypes.T_OBJECT_CLASSIFIERS.column_name: ea_classifier_classifier_id,
        EaTObjectColumnTypes.T_OBJECT_CLASSIFIER_GUIDS.column_name: ea_classifier_classifier_ea_guid,
        EaTObjectColumnTypes.T_OBJECT_STEREOTYPES.column_name: stereotype_name,
    }

    # Since 'Package_ID' value is specific to XML import/export, it shouldn't be taken from enum.
    xml_extensions_map = {
        "Package_ID": containing_ea_package_ea_guid
    }

    add_xml_row_element_to_xml_table_element(
        xml_element_for_table=xml_element_for_classifiers,
        xml_column_names_to_values_map=names_to_values_map,
        xml_extensions_map=xml_extensions_map,
    )

    EaGuidsToEaIdentifiersForObjectsMappings.map.add_single_map(
        ea_guid=ea_classifier_guid,
        ea_identifier=ea_classifier_identifier,
    )

    NfUuidsToEaGuidsMappings.add_single_map(
        nf_uuid=ea_classifier_nf_uuid,
        ea_guid=ea_classifier_guid,
    )
