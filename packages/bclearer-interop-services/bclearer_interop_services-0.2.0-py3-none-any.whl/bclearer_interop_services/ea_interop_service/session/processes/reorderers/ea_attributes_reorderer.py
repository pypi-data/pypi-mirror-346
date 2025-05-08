from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.maps.nf_uuids_to_com_objects_mappings import (
    NfUuidsToIDualObjectsMappings,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.attributes.i_dual_attribute import (
    IDualAttribute,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_dual_element import (
    IDualElement,
)


def reorder_ea_attributes(
    classifier_id_order: dict,
):
    for (
        com_object
    ) in (
        NfUuidsToIDualObjectsMappings.get_i_dual_elements()
    ):
        __reorder_attributes_if_required(
            com_object=com_object,
            classifier_id_order=classifier_id_order,
        )


def __reorder_attributes_if_required(
    com_object,
    classifier_id_order: dict,
):
    if isinstance(
        com_object, IDualElement
    ):
        __reorder_attributes(
            i_dual_element=com_object,
            classifier_id_order=classifier_id_order,
        )


def __reorder_attributes(
    i_dual_element: IDualElement,
    classifier_id_order: dict,
):
    if (
        i_dual_element.attributes.count
        < 2
    ):
        return

    if len(classifier_id_order) == 0:
        return

    new_positions = dict()

    for index in range(
        i_dual_element.attributes.count
    ):
        new_positions = __add_new_position(
            i_dual_element=i_dual_element,
            index=index,
            classifier_id_order=classifier_id_order,
            new_positions=new_positions,
        )

    new_order = {
        k: v
        for k, v in sorted(
            new_positions.items(),
            key=lambda item: item[1],
        )
    }

    index = 0

    for (
        i_dual_attribute
    ) in new_order.keys():
        index = __reorder_attribute(
            i_dual_attribute=i_dual_attribute,
            index=index,
        )

    i_dual_element.attributes.refresh()

    i_dual_element.update()


def __add_new_position(
    i_dual_element: IDualElement,
    index: int,
    classifier_id_order: dict,
    new_positions: dict,
) -> dict:
    attribute_at_index = i_dual_element.attributes.get_at(
        index
    )

    classifier_id = (
        attribute_at_index.classifier_id
    )

    if (
        classifier_id
        in classifier_id_order
    ):
        position = classifier_id_order[
            classifier_id
        ]

    else:
        position = index + max(
            classifier_id_order.values()
        )

    new_positions[
        attribute_at_index
    ] = position

    return new_positions


def __reorder_attribute(
    i_dual_attribute: IDualAttribute,
    index: int,
) -> int:
    i_dual_attribute.pos = index

    index = index + 1

    i_dual_attribute.update()

    return index
