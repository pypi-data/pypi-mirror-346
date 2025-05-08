from bclearer_interop_services.ea_interop_service.i_dual_objects.connectors.i_dual_connector import (
    IDualConnector,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_dual_element import (
    IDualElement,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_null_element import (
    INullElement,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.packages.i_dual_package import (
    IDualPackage,
)


class NfUuidsToIDualObjectsMappings:
    __i_dual_packages_map = dict()

    __i_dual_elements_map = dict()

    __i_dual_connectors_map = dict()

    def __init__(self):
        pass

    @staticmethod
    def map_nf_uuid_to_i_dual_package(
        nf_uuid: str,
        i_dual_package: IDualPackage,
    ):
        NfUuidsToIDualObjectsMappings.__i_dual_packages_map.update(
            {nf_uuid: i_dual_package}
        )

    @staticmethod
    def map_nf_uuid_to_i_dual_element(
        nf_uuid: str,
        i_dual_element: IDualElement,
    ):
        NfUuidsToIDualObjectsMappings.__i_dual_elements_map.update(
            {nf_uuid: i_dual_element}
        )

    @staticmethod
    def map_nf_uuid_to_i_dual_connector(
        nf_uuid: str,
        i_dual_connector: IDualConnector,
    ):
        NfUuidsToIDualObjectsMappings.__i_dual_connectors_map.update(
            {nf_uuid: i_dual_connector}
        )

    @staticmethod
    def get_i_dual_package(
        nf_uuid: str,
    ):
        i_dual_package = NfUuidsToIDualObjectsMappings.__i_dual_packages_map[
            nf_uuid
        ]

        return i_dual_package

    @staticmethod
    def get_i_dual_element(
        nf_uuid: str,
    ):
        if (
            not nf_uuid
            in NfUuidsToIDualObjectsMappings.__i_dual_elements_map
        ):
            return INullElement()

        i_dual_element = NfUuidsToIDualObjectsMappings.__i_dual_elements_map[
            nf_uuid
        ]

        return i_dual_element

    @staticmethod
    def get_i_dual_connector(
        nf_uuid: str,
    ):
        i_dual_connector = NfUuidsToIDualObjectsMappings.__i_dual_connectors_map[
            nf_uuid
        ]

        return i_dual_connector

    @staticmethod
    def get_i_dual_elements():
        return (
            NfUuidsToIDualObjectsMappings.__i_dual_elements_map.values()
        )

    @staticmethod
    def get_nf_uuids_for_i_dual_elements():
        return set(
            NfUuidsToIDualObjectsMappings.__i_dual_elements_map.keys()
        )
