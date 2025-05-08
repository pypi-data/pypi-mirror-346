from bclearer_interop_services.ea_interop_service.i_dual_objects.attributes.i_dual_attribute import (
    IDualAttribute,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.collections.i_dual_collection import (
    IDualCollection,
)


class IDualAttributeCollection(
    IDualCollection
):

    def __init__(self, ea_collection):
        IDualCollection.__init__(
            self,
            ea_collection=ea_collection,
        )

    def get_at(
        self, index: int
    ) -> IDualAttribute:
        collection_item = (
            self.ea_collection.GetAt(
                index
            )
        )

        attribute = IDualAttribute(
            attribute=collection_item
        )

        return attribute
