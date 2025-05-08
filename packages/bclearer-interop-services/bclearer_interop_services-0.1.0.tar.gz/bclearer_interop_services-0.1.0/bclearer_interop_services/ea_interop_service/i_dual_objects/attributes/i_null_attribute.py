from bclearer_interop_services.ea_interop_service.i_dual_objects.attributes.i_attribute import (
    IAttribute,
)


class INullAttribute(IAttribute):

    def __init__(self):
        IAttribute.__init__(self)
        pass
