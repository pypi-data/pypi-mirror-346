from enum import Enum


class EaObjectTypes(Enum):
    pass

    @staticmethod
    def get_type_from_name(name: str):
        raise NotImplementedError
