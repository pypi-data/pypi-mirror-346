from bclearer_core.nf.python_extensions.collections.nf_registries import (
    NfRegistries,
)


class NfEaComBnopRegistries(
    NfRegistries
):
    def __init__(self, owning_facade):
        NfRegistries.__init__(self)

        self.owning_facade = (
            owning_facade
        )

        self.dictionary_of_collections = (
            dict()
        )
