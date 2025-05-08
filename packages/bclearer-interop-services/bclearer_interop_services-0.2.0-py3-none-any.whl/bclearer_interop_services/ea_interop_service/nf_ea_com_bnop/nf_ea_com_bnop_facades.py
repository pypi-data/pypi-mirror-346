from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.nf_ea_com_bnop.migrations.nf_ea_com_to_bnop.nf_ea_com_to_bnop_migration_orchestrator import (
    orchestrate_nf_ea_com_to_bnop_migration,
)
from bclearer_interop_services.ea_interop_service.nf_ea_com_bnop.nf_ea_com_bnop_registries import (
    NfEaComBnopRegistries,
)


class NfEaComBnopFacades:
    def __init__(self):
        self.nf_ea_com_bnop_registry = (
            NfEaComBnopRegistries(
                owning_facade=self
            )
        )

    def migrate_nf_ea_com_universe_to_bnop(
        self,
        nf_ea_com_universe: NfEaComUniverses,
    ):
        orchestrate_nf_ea_com_to_bnop_migration(
            nf_ea_com_universe=nf_ea_com_universe
        )

    def migrate_bnop_to_nf_ea_com_universe(
        self,
    ):
        pass
