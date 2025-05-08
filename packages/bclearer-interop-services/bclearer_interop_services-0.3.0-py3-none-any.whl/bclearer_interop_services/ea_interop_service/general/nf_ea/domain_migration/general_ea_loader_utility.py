import tkinter

from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.common.gui_widgets.gui_widget_factory import (
    create_button,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.xlsx_to_eapx_migration_runner import (
    run_xlsx_to_eapx_migration,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.nf_ea_com_to_domain_migration.eapx_to_xlsx_migration_runner import (
    run_eapx_to_xlsx_migration,
)


def main():
    def eapx_to_xlsx_clicked():
        run_eapx_to_xlsx_migration()

    def xlsx_to_eapx_clicked():
        run_xlsx_to_eapx_migration()

    master = tkinter.Tk()

    create_button(
        master=master,
        button_text="eapx to xlsx",
        command=eapx_to_xlsx_clicked,
        row=0,
    )

    create_button(
        master=master,
        button_text="xlsx to eapx",
        command=xlsx_to_eapx_clicked,
        row=1,
    )

    master.mainloop()

    tkinter.mainloop()


main()
