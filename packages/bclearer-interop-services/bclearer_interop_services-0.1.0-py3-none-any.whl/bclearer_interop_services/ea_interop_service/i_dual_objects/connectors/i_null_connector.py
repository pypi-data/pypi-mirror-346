from bclearer_interop_services.ea_interop_service.i_dual_objects.connectors.i_connector import (
    IConnector,
)


class INullConnector(IConnector):

    def __init__(self):
        IConnector.__init__(self)
        pass
