from bclearer_interop_services.ea_interop_service.i_dual_objects.attributes.i_dual_attribute import (
    IDualAttribute,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.collections.i_dual_attribute_collection import (
    IDualAttributeCollection,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_dual_element import (
    IDualElement,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_element import (
    IElement,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.i_dual_repository import (
    IDualRepository,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def remove_nf_ea_attribute(
    i_dual_repository: IDualRepository,
    ea_attribute_guid: str,
):
    with i_dual_repository.get_attribute_by_guid(
        attribute_guid=ea_attribute_guid
    ) as i_dual_attribute:
        __report_attribute(
            i_dual_attribute=i_dual_attribute
        )

        __remove_nf_ea_attribute(
            i_dual_repository=i_dual_repository,
            i_dual_attribute=i_dual_attribute,
            ea_attribute_guid=ea_attribute_guid,
        )


def __remove_nf_ea_attribute(
    i_dual_repository: IDualRepository,
    i_dual_attribute: IDualAttribute,
    ea_attribute_guid: str,
):
    if not isinstance(
        i_dual_attribute, IDualAttribute
    ):
        log_message(
            ea_attribute_guid
            + " Warning: Attribute not found"
        )

        return

    parent_i_dual_element = __get_parent_i_dual_element(
        i_dual_repository=i_dual_repository,
        i_dual_attribute=i_dual_attribute,
    )

    if not isinstance(
        parent_i_dual_element,
        IDualElement,
    ):
        log_message(
            ea_attribute_guid
            + " Warning: Parent Element not found"
        )

        return

    index_to_delete = __get_index_to_delete(
        i_dual_attribute_collection=parent_i_dual_element.attributes,
        ea_attribute_guid=ea_attribute_guid,
    )

    if index_to_delete == -1:
        __report_deletion_failure(
            ea_attribute_guid=ea_attribute_guid
        )

        return

    __delete_index(
        parent_i_dual_element=parent_i_dual_element,
        index_to_delete=index_to_delete,
    )

    __report_deletion_success(
        ea_attribute_guid=ea_attribute_guid
    )


def __get_parent_i_dual_element(
    i_dual_repository: IDualRepository,
    i_dual_attribute: IDualAttribute,
) -> IElement:
    parent_id = (
        i_dual_attribute.parent_id
    )

    parent_i_dual_element = i_dual_repository.get_element_by_id(
        element_id=parent_id
    )

    return parent_i_dual_element


def __get_index_to_delete(
    i_dual_attribute_collection: IDualAttributeCollection,
    ea_attribute_guid: str,
) -> int:
    for index in range(
        i_dual_attribute_collection.count
    ):
        attribute_at_index = i_dual_attribute_collection.get_at(
            index
        )

        if (
            attribute_at_index.attribute_guid
            == ea_attribute_guid
        ):
            return index

    return -1


def __delete_index(
    parent_i_dual_element: IDualElement,
    index_to_delete: int,
):
    parent_i_dual_element.attributes.delete(
        index=index_to_delete
    )

    parent_i_dual_element.attributes.refresh()

    parent_i_dual_element.update()

    parent_i_dual_element.refresh()


def __report_attribute(
    i_dual_attribute: IDualAttribute,
):
    attribute_guid = (
        i_dual_attribute.attribute_guid
    )

    attribute_name = (
        i_dual_attribute.name
    )

    log_message(
        attribute_guid
        + " : Attribute '"
        + attribute_name
        + "' to be removed"
    )


def __report_deletion_success(
    ea_attribute_guid: str,
):
    log_message(
        ea_attribute_guid
        + " : Attribute removed"
    )


def __report_deletion_failure(
    ea_attribute_guid: str,
):
    log_message(
        ea_attribute_guid
        + " : Attribute removal failed.  Failed to find attribute in parent collection"
    )
