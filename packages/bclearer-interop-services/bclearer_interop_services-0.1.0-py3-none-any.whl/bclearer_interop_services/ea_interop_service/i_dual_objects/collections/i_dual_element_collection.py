from bclearer_interop_services.ea_interop_service.i_dual_objects.collections.i_dual_collection import (
    IDualCollection,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_dual_element import (
    IDualElement,
)


class IDualElementCollection(
    IDualCollection
):

    def __init__(self, ea_collection):
        IDualCollection.__init__(
            self,
            ea_collection=ea_collection,
        )

    def get_at(
        self, index: int
    ) -> IDualElement:
        collection_item = (
            self.ea_collection.GetAt(
                index
            )
        )

        element = IDualElement(
            element=collection_item
        )

        return element
