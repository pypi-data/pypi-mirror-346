from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)


def get_tuple_attribute_value_if_required(
    owning_tuple: tuple,
    attribute_name: str,
) -> str:
    if (
        attribute_name
        == DEFAULT_NULL_VALUE
    ):
        return DEFAULT_NULL_VALUE

    if not hasattr(
        owning_tuple,
        attribute_name,
    ):
        return DEFAULT_NULL_VALUE

    tuple_attribute_value = getattr(
        owning_tuple,
        attribute_name,
    )

    return tuple_attribute_value
