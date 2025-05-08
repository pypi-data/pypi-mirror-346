from bclearer_interop_services.ea_interop_service.i_dual_objects.stereotypes.i_stereotype import (
    IStereotype,
)


class INullStereotype(IStereotype):

    def __init__(self):
        IStereotype.__init__(self)
        pass
