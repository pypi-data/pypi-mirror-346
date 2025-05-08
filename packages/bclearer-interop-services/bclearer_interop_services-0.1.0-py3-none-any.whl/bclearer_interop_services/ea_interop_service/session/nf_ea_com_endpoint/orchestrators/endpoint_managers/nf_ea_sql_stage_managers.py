from bclearer_interop_services.ea_interop_service.session.nf_ea_com_endpoint.orchestrators.nf_managers import (
    NfManagers,
)
from bclearer_interop_services.ea_interop_service.session.nf_ea_com_endpoint.orchestrators.universe_managers.nf_ea_sql_universe_managers import (
    NfEaSqlUniverseManagers,
)


class NfEaSqlStageManagers(NfManagers):
    def __init__(
        self, ea_tools_session_manager
    ):
        NfManagers.__init__(self)

        self.nf_ea_sql_universe_manager = NfEaSqlUniverseManagers(
            ea_tools_session_manager=ea_tools_session_manager
        )

    def close(self):
        self.nf_ea_sql_universe_manager.close()
