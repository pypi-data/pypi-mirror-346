from xml.etree.ElementTree import (
    Element,
)

from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_adders.native_xml_preparer import (
    prepare_native_xml,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_io_agents.xml_serialiser import (
    serialise_xml,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_loaders.ea_attributes_xml_loader import (
    map_and_xml_load_ea_attributes,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_loaders.ea_classifiers_xml_loader import (
    map_and_xml_load_ea_non_proxy_classifiers,
    map_and_xml_load_ea_proxy_classifiers,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_loaders.ea_connectors_xml_loader import (
    map_and_xml_load_ea_connectors,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_loaders.ea_packages_xml_loader import (
    map_and_xml_load_ea_packages,
)
from bclearer_interop_services.ea_interop_service.general.ea.xml.nf_ea_xml_loaders.ea_stereotype_usages_xml_loader import (
    map_and_xml_load_ea_stereotype_usages,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.dataframes.ea_connectors_splitter import (
    split_ea_connectors,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.stereotypes.ea_model_load_helper import (
    get_stereotype_usage_with_names_dataframe,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def orchestrate_creation_xml_native_file_for_import(
    output_xml_file_full_path: str,
    nf_ea_com_dataframes_dictionary: dict,
    start_ea_identifier_for_new_objects: int,
    start_ea_identifier_for_new_packages: int,
    start_ea_identifier_for_new_attributes: int,
    default_model_package_ea_guid: str,
    start_ea_identifier_for_new_connector=0,
):
    log_message(
        "Exporting the data to native xml."
    )

    (
        xml_root_element,
        xml_root_element_guid,
        xml_element_for_packages,
    ) = prepare_native_xml(
        object_ea_identifier_for_import_package=start_ea_identifier_for_new_objects,
        package_ea_identifier_for_import_package=start_ea_identifier_for_new_packages,
        default_model_package_ea_guid=default_model_package_ea_guid,
    )

    start_ea_identifier_for_new_objects += (
        1
    )

    start_ea_identifier_for_new_packages += (
        1
    )

    xml_root_element = __map_and_load(
        xml_root_element=xml_root_element,
        xml_root_element_guid=xml_root_element_guid,
        xml_element_for_packages=xml_element_for_packages,
        nf_ea_com_dataframes_dictionary=nf_ea_com_dataframes_dictionary,
        start_ea_identifier_for_new_objects=start_ea_identifier_for_new_objects,
        start_ea_identifier_for_new_packages=start_ea_identifier_for_new_packages,
        start_ea_identifier_for_new_attributes=start_ea_identifier_for_new_attributes,
        start_ea_identifier_for_new_connectors=start_ea_identifier_for_new_connector,
    )

    serialise_xml(
        xml_root_element=xml_root_element,
        xml_file_full_path=output_xml_file_full_path,
    )


def __map_and_load(
    xml_root_element: Element,
    xml_root_element_guid: str,
    xml_element_for_packages: Element,
    nf_ea_com_dataframes_dictionary: dict,
    start_ea_identifier_for_new_objects: int,
    start_ea_identifier_for_new_packages: int,
    start_ea_identifier_for_new_attributes: int,
    start_ea_identifier_for_new_connectors: int,
) -> Element:
    stereotype_usage_with_names = get_stereotype_usage_with_names_dataframe(
        nf_ea_com_dataframes_dictionary=nf_ea_com_dataframes_dictionary
    )

    (
        xml_root_element,
        xml_element_for_packages_as_objects,
        start_ea_identifier_for_new_objects,
    ) = map_and_xml_load_ea_packages(
        ea_packages=nf_ea_com_dataframes_dictionary[
            NfEaComCollectionTypes.EA_PACKAGES
        ],
        start_ea_identifier_for_new_packages=start_ea_identifier_for_new_packages,
        start_ea_identifier_for_new_objects=start_ea_identifier_for_new_objects,
        xml_root_element=xml_root_element,
        xml_element_for_packages=xml_element_for_packages,
        containing_ea_package_guid=xml_root_element_guid,
    )

    (
        xml_root_element,
        xml_element_for_classifiers,
    ) = map_and_xml_load_ea_non_proxy_classifiers(
        ea_classifiers=nf_ea_com_dataframes_dictionary[
            NfEaComCollectionTypes.EA_CLASSIFIERS
        ],
        start_ea_identifier=start_ea_identifier_for_new_objects,
        xml_root_element=xml_root_element,
        xml_element_for_classifiers=xml_element_for_packages_as_objects,
        stereotype_usage_with_names=stereotype_usage_with_names,
    )

    (
        ea_connectors_not_connecting_proxy_connector,
        ea_connectors_connecting_proxy_connector,
    ) = split_ea_connectors(
        ea_connectors=nf_ea_com_dataframes_dictionary[
            NfEaComCollectionTypes.EA_CONNECTORS
        ],
        ea_classifiers=nf_ea_com_dataframes_dictionary[
            NfEaComCollectionTypes.EA_CLASSIFIERS
        ],
    )

    (
        xml_root_element,
        xml_element_for_connectors,
        start_ea_identifier_for_new_connectors,
    ) = map_and_xml_load_ea_connectors(
        ea_connectors=ea_connectors_not_connecting_proxy_connector,
        start_ea_identifier=start_ea_identifier_for_new_connectors,
        xml_root_element=xml_root_element,
        stereotype_usage_with_names=stereotype_usage_with_names,
    )

    (
        xml_root_element,
        xml_element_for_classifiers,
    ) = map_and_xml_load_ea_proxy_classifiers(
        ea_classifiers=nf_ea_com_dataframes_dictionary[
            NfEaComCollectionTypes.EA_CLASSIFIERS
        ],
        start_ea_identifier=start_ea_identifier_for_new_objects,
        xml_root_element=xml_root_element,
        xml_element_for_classifiers=xml_element_for_packages_as_objects,
        stereotype_usage_with_names=stereotype_usage_with_names,
    )

    if (
        not ea_connectors_connecting_proxy_connector.empty
    ):
        (
            xml_root_element,
            xml_element_for_connectors,
            start_ea_identifier_for_new_connectors,
        ) = map_and_xml_load_ea_connectors(
            ea_connectors=ea_connectors_connecting_proxy_connector,
            start_ea_identifier=start_ea_identifier_for_new_connectors,
            xml_root_element=xml_root_element,
            xml_element_for_connectors=xml_element_for_connectors,
            stereotype_usage_with_names=stereotype_usage_with_names,
        )

    xml_root_element = map_and_xml_load_ea_attributes(
        ea_attributes=nf_ea_com_dataframes_dictionary[
            NfEaComCollectionTypes.EA_ATTRIBUTES
        ],
        ea_classifiers=nf_ea_com_dataframes_dictionary[
            NfEaComCollectionTypes.EA_CLASSIFIERS
        ],
        start_ea_identifier=start_ea_identifier_for_new_attributes,
        xml_root_element=xml_root_element,
    )

    xml_root_element = map_and_xml_load_ea_stereotype_usages(
        stereotype_usage_with_names=stereotype_usage_with_names,
        xml_root_element=xml_root_element,
    )

    return xml_root_element
