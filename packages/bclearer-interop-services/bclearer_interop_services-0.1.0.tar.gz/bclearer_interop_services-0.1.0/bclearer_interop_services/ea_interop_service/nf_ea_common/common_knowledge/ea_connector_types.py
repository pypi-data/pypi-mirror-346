from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_object_types import (
    EaObjectTypes,
)


@unique
class EaConnectorTypes(EaObjectTypes):
    ABSTRACTION = auto()
    AGGREGATION = auto()
    ASSEMBLY = auto()
    ASSOCIATION = auto()
    COLLABORATION = auto()
    COMMUNICATION_PATH = auto()
    CONNECTOR = auto()
    CONTROL_FLOW = auto()
    DELEGATE = auto()
    DEPENDENCY = auto()
    DEPLOYMENT = auto()
    ER_LINK = auto()
    EXTENSION = auto()
    GENERALIZATION = auto()
    INFORMATION_FLOW = auto()
    INSTANTIATION = auto()
    INTERRUPT_FLOW = auto()
    MANIFEST = auto()
    NESTING = auto()
    NOTE_LINK = auto()
    OBJECT_FLOW = auto()
    PACKAGE = auto()
    PROTOCOL_CONFORMANCE = auto()
    PROTOCOL_TRANSITION = auto()
    REALISATION = auto()
    SEQUENCE = auto()
    STATE_FLOW = auto()
    SUBSTITUTION = auto()
    USAGE = auto()
    USE_CASE = auto()

    @staticmethod
    def get_type_from_name(name: str):
        for (
            ea_connector_type,
            ea_connector_type_name,
        ) in type_name_mapping.items():
            if (
                ea_connector_type_name
                == name
            ):
                return ea_connector_type

    def __type_name(self) -> str:
        type_name = type_name_mapping[
            self
        ]

        return type_name

    type_name = property(
        fget=__type_name
    )


type_name_mapping = {
    EaConnectorTypes.ABSTRACTION: "Abstraction",
    EaConnectorTypes.AGGREGATION: "Aggregation",
    EaConnectorTypes.ASSEMBLY: "Assembly",
    EaConnectorTypes.ASSOCIATION: "Association",
    EaConnectorTypes.COLLABORATION: "Collaboration",
    EaConnectorTypes.COMMUNICATION_PATH: "CommunicationPath",
    EaConnectorTypes.CONNECTOR: "Connector",
    EaConnectorTypes.CONTROL_FLOW: "ControlFlow",
    EaConnectorTypes.DELEGATE: "Delegate",
    EaConnectorTypes.DEPENDENCY: "Dependency",
    EaConnectorTypes.DEPLOYMENT: "Deployment",
    EaConnectorTypes.ER_LINK: "ERLink",
    EaConnectorTypes.EXTENSION: "Extension",
    EaConnectorTypes.GENERALIZATION: "Generalization",
    EaConnectorTypes.INFORMATION_FLOW: "InformationFlow",
    EaConnectorTypes.INSTANTIATION: "Instantiation",
    EaConnectorTypes.INTERRUPT_FLOW: "InterruptFlow",
    EaConnectorTypes.MANIFEST: "Manifest",
    EaConnectorTypes.NESTING: "Nesting",
    EaConnectorTypes.NOTE_LINK: "NoteLink",
    EaConnectorTypes.OBJECT_FLOW: "ObjectFlow",
    EaConnectorTypes.PACKAGE: "Package",
    EaConnectorTypes.PROTOCOL_CONFORMANCE: "ProtocolConformance",
    EaConnectorTypes.PROTOCOL_TRANSITION: "ProtocolTransition",
    EaConnectorTypes.REALISATION: "Realisation",
    EaConnectorTypes.SEQUENCE: "Sequence",
    EaConnectorTypes.STATE_FLOW: "StateFlow",
    EaConnectorTypes.SUBSTITUTION: "Substitution",
    EaConnectorTypes.USAGE: "Usage",
    EaConnectorTypes.USE_CASE: "UseCase",
}
