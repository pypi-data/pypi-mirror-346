from bclearer_interop_services.ea_interop_service.general.ea.com.ea_com_universes import (
    EaComUniverses,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_null_element import (
    INullElement,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def rename_nf_ea_element(
    ea_com_universe: EaComUniverses,
    element_ea_guid: str,
    new_ea_element_name: str,
):
    with ea_com_universe.i_dual_repository.get_element_by_guid(
        element_ea_guid=element_ea_guid
    ) as i_dual_element:
        if isinstance(
            i_dual_element, INullElement
        ):
            log_message(
                element_ea_guid
                + "Warning: Element not found"
            )

            return

        old_ea_element_name = (
            i_dual_element.name
        )

        if (
            old_ea_element_name
            == new_ea_element_name
        ):
            log_message(
                element_ea_guid
                + "Current name equals clean name for Element Name ("
                + old_ea_element_name
                + ")"
            )

        else:

            i_dual_element.name = (
                new_ea_element_name
            )

            i_dual_element.update()

            i_dual_element.refresh()

            log_message(
                element_ea_guid
                + " : Element Name changed ("
                + old_ea_element_name
                + ") to ("
                + new_ea_element_name
                + ")"
            )
