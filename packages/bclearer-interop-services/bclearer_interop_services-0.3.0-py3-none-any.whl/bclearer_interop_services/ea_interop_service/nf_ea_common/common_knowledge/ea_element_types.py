from enum import auto, unique

from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_object_types import (
    EaObjectTypes,
)


@unique
class EaElementTypes(EaObjectTypes):
    ACTION = auto()
    ACTION_PIN = auto()
    ACTIVITY = auto()
    ACTIVITY_PARAMETER = auto()
    ACTIVITY_PARTITION = auto()
    ACTIVITY_REGION = auto()
    ACTOR = auto()
    ARTIFACT = auto()
    ASSOCIATION = auto()
    BOUNDARY = auto()
    CENTRAL_BUFFER_NODE = auto()
    CHANGE = auto()
    CLASS = auto()
    COLLABORATION = auto()
    COLLABORATION_OCCURRENCE = auto()
    COMMENT = auto()
    COMPONENT = auto()
    CONDITIONAL_NODE = auto()
    CONSTRAINT = auto()
    DATA_STORE = auto()
    DATA_TYPE = auto()
    DECISION = auto()
    DEFECT = auto()
    DEPLOYMENT_SPECIFICATION = auto()
    DEVICE = auto()
    DIAGRAM_FRAME = auto()
    ENTITY = auto()
    ENTRY_POINT = auto()
    ENUMERATION = auto()
    EVENT = auto()
    EXCEPTION_HANDLER = auto()
    EXECUTION_ENVIRONMENT = auto()
    EXIT_POINT = auto()
    EXPANSION_NODE = auto()
    EXPANSION_REGION = auto()
    FEATURE = auto()
    GUI_ELEMENT = auto()
    INFORMATION_ITEM = auto()
    INTERACTION = auto()
    INTERACTION_FRAGMENT = auto()
    INTERACTION_OCCURRENCE = auto()
    INTERACTION_STATE = auto()
    INTERFACE = auto()
    INTERRUPTIBLE_ACTIVITY_REGION = (
        auto()
    )
    ISSUE = auto()
    LABEL = auto()
    LOOP_NODE = auto()
    MERGE_NODE = auto()
    MESSAGE_ENDPOINT = auto()
    NODE = auto()
    NOTE = auto()
    OBJECT = auto()
    OBJECT_NODE = auto()
    PACKAGE = auto()
    PARAMETER = auto()
    PART = auto()
    PORT = auto()
    PRIMITIVE_TYPE = auto()
    PROTOCOL_STATE_MACHINE = auto()
    PROVIDED_INTERFACE = auto()
    REGION = auto()
    REPORT = auto()
    REQUIRED_INTERFACE = auto()
    REQUIREMENT = auto()
    RISK = auto()
    SCREEN = auto()
    SEQUENCE = auto()
    SIGNAL = auto()
    STATE = auto()
    STATE_MACHINE = auto()
    STATE_NODE = auto()
    SYNCHRONIZATION = auto()
    TASK = auto()
    TEST = auto()
    TEXT = auto()
    TIMELINE = auto()
    TRIGGER = auto()
    UML_DIAGRAM = auto()
    USE_CASE = auto()
    USER = auto()

    PROXY_CONNECTOR = auto()

    @staticmethod
    def get_type_from_name(name: str):
        for (
            ea_object_type,
            ea_object_type_name,
        ) in type_name_mapping.items():
            if (
                ea_object_type_name
                == name
            ):
                return ea_object_type

    def __type_name(self) -> str:
        type_name = type_name_mapping[
            self
        ]

        return type_name

    type_name = property(
        fget=__type_name
    )


type_name_mapping = {
    EaElementTypes.ACTION: "Action",
    EaElementTypes.ACTION_PIN: "ActionPin",
    EaElementTypes.ACTIVITY: "Activity",
    EaElementTypes.ACTIVITY_PARAMETER: "ActivityParameter",
    EaElementTypes.ACTIVITY_PARTITION: "ActivityPartition",
    EaElementTypes.ACTIVITY_REGION: "ActivityRegion",
    EaElementTypes.ACTOR: "Actor",
    EaElementTypes.ARTIFACT: "Artifact",
    EaElementTypes.ASSOCIATION: "Association",
    EaElementTypes.BOUNDARY: "Boundary",
    EaElementTypes.CENTRAL_BUFFER_NODE: "CentralBufferNode",
    EaElementTypes.CHANGE: "Change",
    EaElementTypes.CLASS: "Class",
    EaElementTypes.COLLABORATION: "Collaboration",
    EaElementTypes.COLLABORATION_OCCURRENCE: "CollaborationOccurrence",
    EaElementTypes.COMMENT: "Comment",
    EaElementTypes.COMPONENT: "Component",
    EaElementTypes.CONDITIONAL_NODE: "ConditionalNode",
    EaElementTypes.CONSTRAINT: "Constraint",
    EaElementTypes.DATA_STORE: "DataStore",
    EaElementTypes.DATA_TYPE: "DataType",
    EaElementTypes.DECISION: "Decision",
    EaElementTypes.DEFECT: "Defect",
    EaElementTypes.DEPLOYMENT_SPECIFICATION: "DeploymentSpecification",
    EaElementTypes.DEVICE: "Device",
    EaElementTypes.DIAGRAM_FRAME: "DiagramFrame",
    EaElementTypes.ENTITY: "Entity",
    EaElementTypes.ENTRY_POINT: "EntryPoint",
    EaElementTypes.ENUMERATION: "Enumeration",
    EaElementTypes.EVENT: "Event",
    EaElementTypes.EXCEPTION_HANDLER: "ExceptionHandler",
    EaElementTypes.EXECUTION_ENVIRONMENT: "ExecutionEnvironment",
    EaElementTypes.EXIT_POINT: "ExitPoint",
    EaElementTypes.EXPANSION_NODE: "ExpansionNode",
    EaElementTypes.EXPANSION_REGION: "ExpansionRegion",
    EaElementTypes.FEATURE: "Feature",
    EaElementTypes.GUI_ELEMENT: "GUIElement",
    EaElementTypes.INFORMATION_ITEM: "InformationItem",
    EaElementTypes.INTERACTION: "Interaction",
    EaElementTypes.INTERACTION_FRAGMENT: "InteractionFragment",
    EaElementTypes.INTERACTION_OCCURRENCE: "InteractionOccurrence",
    EaElementTypes.INTERACTION_STATE: "InteractionState",
    EaElementTypes.INTERFACE: "Interface",
    EaElementTypes.INTERRUPTIBLE_ACTIVITY_REGION: "InterruptibleActivityRegion",
    EaElementTypes.ISSUE: "Issue",
    EaElementTypes.LABEL: "Label",
    EaElementTypes.LOOP_NODE: "LoopNode",
    EaElementTypes.MERGE_NODE: "MergeNode",
    EaElementTypes.MESSAGE_ENDPOINT: "MessageEndpoint",
    EaElementTypes.NODE: "Node",
    EaElementTypes.NOTE: "Note",
    EaElementTypes.OBJECT: "Object",
    EaElementTypes.OBJECT_NODE: "ObjectNode",
    EaElementTypes.PACKAGE: "Package",
    EaElementTypes.PARAMETER: "Parameter",
    EaElementTypes.PART: "Part",
    EaElementTypes.PORT: "Port",
    EaElementTypes.PRIMITIVE_TYPE: "PrimitiveType",
    EaElementTypes.PROTOCOL_STATE_MACHINE: "ProtocolStateMachine",
    EaElementTypes.PROVIDED_INTERFACE: "ProvidedInterface",
    EaElementTypes.REGION: "Region",
    EaElementTypes.REPORT: "Report",
    EaElementTypes.REQUIRED_INTERFACE: "RequiredInterface",
    EaElementTypes.REQUIREMENT: "Requirement",
    EaElementTypes.RISK: "Risk",
    EaElementTypes.SCREEN: "Screen",
    EaElementTypes.SEQUENCE: "Sequence",
    EaElementTypes.SIGNAL: "Signal",
    EaElementTypes.STATE: "State",
    EaElementTypes.STATE_MACHINE: "StateMachine",
    EaElementTypes.STATE_NODE: "StateNode",
    EaElementTypes.SYNCHRONIZATION: "Synchronization",
    EaElementTypes.TASK: "Task",
    EaElementTypes.TEST: "Test",
    EaElementTypes.TEXT: "Text",
    EaElementTypes.TIMELINE: "TimeLine",
    EaElementTypes.TRIGGER: "Trigger",
    EaElementTypes.UML_DIAGRAM: "UMLDiagram",
    EaElementTypes.USE_CASE: "UseCase",
    EaElementTypes.USER: "User",
    EaElementTypes.PROXY_CONNECTOR: "ProxyConnector",
}
