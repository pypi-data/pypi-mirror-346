from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)


def get_node_value(node) -> str:
    if node is None:
        return DEFAULT_NULL_VALUE

    if node.text is None:
        return DEFAULT_NULL_VALUE

    return node.text
