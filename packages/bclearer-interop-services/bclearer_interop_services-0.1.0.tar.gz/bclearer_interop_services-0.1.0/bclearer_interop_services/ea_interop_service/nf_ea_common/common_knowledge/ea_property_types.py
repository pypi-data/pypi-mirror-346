from enum import Enum, auto, unique


@unique
class EaPropertyTypes(Enum):
    CONNECTOR_PROPERTY = auto()
    ELEMENT_PROPERTY = auto()
    ATTRIBUTE_PROPERTY = auto()

    def __type_name(self) -> str:
        type_name = type_name_mapping[
            self
        ]

        return type_name

    type_name = property(
        fget=__type_name
    )


type_name_mapping = {
    EaPropertyTypes.CONNECTOR_PROPERTY: "connector property",
    EaPropertyTypes.ELEMENT_PROPERTY: "element property",
    EaPropertyTypes.ATTRIBUTE_PROPERTY: "attribute property",
}
