from bclearer_interop_services.ea_interop_service.i_dual_objects.collections.i_collection import (
    ICollection,
)


class INullCollection(ICollection):

    def __init__(self):
        ICollection.__init__(self)

        pass
