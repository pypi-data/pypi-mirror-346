from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_element import (
    IElement,
)


class INullElement(IElement):

    def __init__(self):
        IElement.__init__(self)
        pass
