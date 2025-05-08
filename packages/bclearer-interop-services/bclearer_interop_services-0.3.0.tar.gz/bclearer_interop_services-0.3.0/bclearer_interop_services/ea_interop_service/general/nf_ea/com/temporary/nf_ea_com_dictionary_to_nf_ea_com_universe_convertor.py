from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_interop_services.ea_interop_service.session.processes.creators.empty_nf_ea_com_universe_creator import (
    create_empty_nf_ea_universe,
)
from pandas import DataFrame, concat


def convert_nf_ea_com_dictionary_to_nf_ea_com_universe(
    ea_tools_session_manager: EaToolsSessionManagers,
    nf_ea_com_dictionary: dict,
    short_name: str,
) -> NfEaComUniverses:
    nf_ea_com_universe = create_empty_nf_ea_universe(
        ea_tools_session_manager=ea_tools_session_manager,
        short_name=short_name,
    )

    for (
        collection_key,
        nf_com_ea_dictionary_item,
    ) in nf_ea_com_dictionary.items():
        __convert_nf_com_ea_dictionary_item_to_nf_ea_com_universe_collection(
            collection_key=collection_key,
            nf_com_ea_dictionary_item=nf_com_ea_dictionary_item,
            nf_ea_com_universe=nf_ea_com_universe,
        )

    return nf_ea_com_universe


def __convert_nf_com_ea_dictionary_item_to_nf_ea_com_universe_collection(
    collection_key: NfEaComCollectionTypes,
    nf_com_ea_dictionary_item: DataFrame,
    nf_ea_com_universe: NfEaComUniverses,
):
    if (
        collection_key
        == "ea_attributes_order"
    ):
        return

    if (
        collection_key
        == NfEaComCollectionTypes.EA_CONNECTORS_PC
    ):
        collection_key = (
            NfEaComCollectionTypes.EA_CONNECTORS
        )

    collection = nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
        collection_key
    ]

    new_collection = concat(
        [
            collection,
            nf_com_ea_dictionary_item,
        ]
    )

    new_collection = (
        new_collection.fillna(
            DEFAULT_NULL_VALUE
        )
    )

    nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
        collection_key
    ] = new_collection
