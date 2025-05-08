from bclearer_interop_services.ea_interop_service.i_dual_objects.i_repository import (
    IRepository,
)


class INullRepository(IRepository):

    def __init__(self):
        IRepository.__init__(self)
        pass
