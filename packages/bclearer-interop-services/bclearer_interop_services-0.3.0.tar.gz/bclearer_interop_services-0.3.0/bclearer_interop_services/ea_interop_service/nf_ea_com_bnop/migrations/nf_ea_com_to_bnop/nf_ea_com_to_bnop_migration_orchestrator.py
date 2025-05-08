from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.nf_ea_com_bnop.migrations.nf_ea_com_to_bnop.migrators.ea_named_by_connectors_migrator import (
    migrate_ea_connectors_in_scope_of_naming_pattern,
)
from bclearer_interop_services.ea_interop_service.nf_ea_com_bnop.migrations.nf_ea_com_to_bnop.migrators.ea_subtyping_connectors_migrator import (
    migrate_ea_connectors_in_scope_of_subtyping_pattern,
)
from bclearer_interop_services.ea_interop_service.nf_ea_com_bnop.migrations.nf_ea_com_to_bnop.migrators.ea_typing_connectors_migrator import (
    migrate_ea_connectors_in_scope_of_typing_pattern,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from bnop.core.object_model.bnop_repositories import (
    BnopRepositories,
)


def orchestrate_nf_ea_com_to_bnop_migration(
    nf_ea_com_universe: NfEaComUniverses,
):
    log_message(
        message="Started migrating nf ea com to bnop"
    )

    bnop_repository = BnopRepositories(
        uuid=create_new_uuid()
    )

    migrate_ea_connectors_in_scope_of_naming_pattern(
        nf_ea_com_universe=nf_ea_com_universe,
        bnop_repository=bnop_repository,
    )

    migrate_ea_connectors_in_scope_of_typing_pattern(
        nf_ea_com_universe=nf_ea_com_universe,
        bnop_repository=bnop_repository,
    )

    migrate_ea_connectors_in_scope_of_subtyping_pattern(
        nf_ea_com_universe=nf_ea_com_universe,
        bnop_repository=bnop_repository,
    )

    log_message(
        message="Finished migrating nf ea com to bnop"
    )
