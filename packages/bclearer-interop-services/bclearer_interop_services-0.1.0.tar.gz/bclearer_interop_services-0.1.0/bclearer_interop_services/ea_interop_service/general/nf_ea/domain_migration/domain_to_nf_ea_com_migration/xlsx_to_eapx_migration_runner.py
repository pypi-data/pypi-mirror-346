from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.common.setup_and_close_out.set_up_and_close_out_helper import (
    end_domain_migration,
    set_up_logger_and_output_folder_for_domain_migration,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.gui.xlsx_to_eapx_parameters_getter import (
    get_xlsx_to_eapx_parameters,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.orchestrators.xlsx_to_eapx_migration_orchestator import (
    orchestrate_xlsx_to_eapx_migration,
)


def run_xlsx_to_eapx_migration():
    (
        input_file,
        output_folder,
        short_name,
        package_sheet_names,
        classifier_sheet_names,
        connector_sheet_names,
        stereotype_group_sheet_names,
        stereotype_sheet_names,
        stereotype_usage_sheet_names,
    ) = get_xlsx_to_eapx_parameters()

    set_up_logger_and_output_folder_for_domain_migration(
        output_folder=output_folder
    )

    orchestrate_xlsx_to_eapx_migration(
        input_file=input_file,
        output_folder=output_folder,
        short_name=short_name,
        package_sheet_names=package_sheet_names,
        classifier_sheet_names=classifier_sheet_names,
        connector_sheet_names=connector_sheet_names,
        stereotype_group_sheet_names=stereotype_group_sheet_names,
        stereotype_sheet_names=stereotype_sheet_names,
        stereotype_usage_sheet_names=stereotype_usage_sheet_names,
    )

    end_domain_migration()
