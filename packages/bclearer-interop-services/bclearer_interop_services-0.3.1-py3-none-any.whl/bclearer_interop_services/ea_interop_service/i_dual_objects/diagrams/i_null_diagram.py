from bclearer_interop_services.ea_interop_service.i_dual_objects.diagrams.i_diagram import (
    IDiagram,
)


class INullDiagram(IDiagram):

    def __init__(self):
        IDiagram.__init__(self)
        pass
