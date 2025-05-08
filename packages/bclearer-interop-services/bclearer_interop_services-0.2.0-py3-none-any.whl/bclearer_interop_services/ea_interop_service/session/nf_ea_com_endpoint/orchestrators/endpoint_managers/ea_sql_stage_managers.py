from bclearer_interop_services.ea_interop_service.session.nf_ea_com_endpoint.orchestrators.nf_managers import (
    NfManagers,
)
from bclearer_interop_services.ea_interop_service.session.nf_ea_com_endpoint.orchestrators.universe_managers.ea_sql_universe_managers import (
    EaSqlUniverseManagers,
)


class EaSqlStageManagers(NfManagers):
    def __init__(self):
        NfManagers.__init__(self)

        self.ea_sql_universe_manager = (
            EaSqlUniverseManagers()
        )

    def close(self):
        self.ea_sql_universe_manager.close()
