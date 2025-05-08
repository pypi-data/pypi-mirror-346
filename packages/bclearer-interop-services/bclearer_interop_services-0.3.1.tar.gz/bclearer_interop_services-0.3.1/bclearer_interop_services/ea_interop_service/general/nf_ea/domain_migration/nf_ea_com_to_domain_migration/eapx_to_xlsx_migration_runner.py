from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.common.setup_and_close_out.set_up_and_close_out_helper import (
    end_domain_migration,
    set_up_logger_and_output_folder_for_domain_migration,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.nf_ea_com_to_domain_migration.gui.eapx_to_xlsx_parameters_getter import (
    get_eapx_to_xlsx_parameters,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.nf_ea_com_to_domain_migration.orchestrators.eapx_to_xlsx_migration_orchestrator import (
    orchestrate_eapx_to_xlsx_migration,
)


def run_eapx_to_xlsx_migration():
    (
        input_file,
        output_folder,
        short_name,
    ) = get_eapx_to_xlsx_parameters()

    set_up_logger_and_output_folder_for_domain_migration(
        output_folder=output_folder
    )

    orchestrate_eapx_to_xlsx_migration(
        input_file=input_file,
        output_folder=output_folder,
        short_name=short_name,
    )

    end_domain_migration()
