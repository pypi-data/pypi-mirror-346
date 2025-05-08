from bclearer_interop_services.ea_interop_service.i_dual_objects.collections.i_dual_collection import (
    IDualCollection,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.connectors.i_dual_connector import (
    IDualConnector,
)


class IDualConnectorCollection(
    IDualCollection
):

    def __init__(self, ea_collection):
        IDualCollection.__init__(
            self,
            ea_collection=ea_collection,
        )

    def get_at(
        self, index: int
    ) -> IDualConnector:
        collection_item = (
            self.ea_collection.GetAt(
                index
            )
        )

        connector = IDualConnector(
            connector=collection_item
        )

        return connector
