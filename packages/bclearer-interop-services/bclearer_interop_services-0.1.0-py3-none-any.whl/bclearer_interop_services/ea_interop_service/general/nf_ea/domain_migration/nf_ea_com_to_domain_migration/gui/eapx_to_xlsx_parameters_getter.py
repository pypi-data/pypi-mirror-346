import os
import tkinter
from tkinter import filedialog

from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.common.gui_widgets.gui_widget_factory import (
    create_button,
    create_textbox_with_label,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from nf_common_source.code.services.datetime_service.time_helpers.time_getter import (
    now_time_as_string_for_files,
)


def get_eapx_to_xlsx_parameters():
    def select_file():
        file_path = filedialog.askopenfile(
            parent=master,
            initialdir=os.getcwd(),
            title="Select eapx file",
            filetypes=[
                ("EA Models", "*.eapx")
            ],
        )

        input_file_name_textbox.insert(
            0, file_path.name
        )

    def select_output_folder():
        output_folder_path = filedialog.askdirectory(
            parent=master,
            initialdir=os.getcwd(),
            title="Select output folder",
        )

        output_folder_name_textbox.insert(
            0,
            output_folder_path
            + "/"
            + now_time_as_string_for_files()
            + "/",
        )

    def close():
        master.quit()

    master = tkinter.Tk()

    master.wm_title(
        string="EA Model (eapx) to Excel (xlsx)"
    )

    input_file_name_textbox = (
        create_textbox_with_label(
            master=master,
            row=0,
            label_text="Input File: ",
            width=100,
        )
    )

    output_folder_name_textbox = create_textbox_with_label(
        master=master,
        row=1,
        label_text="Output Folder: ",
        width=100,
    )

    short_name_textbox = (
        create_textbox_with_label(
            master=master,
            row=2,
            label_text="Short Name: ",
            width=10,
        )
    )
    create_button(
        master=master,
        button_text="...",
        command=select_file,
        row=0,
    )

    create_button(
        master=master,
        button_text="...",
        command=select_output_folder,
        row=1,
    )

    create_button(
        master=master,
        button_text="OK",
        command=close,
        row=6,
    )

    master.mainloop()

    tkinter.mainloop()

    input_file = Files(
        absolute_path_string=input_file_name_textbox.get()
    )

    output_folder_name = (
        output_folder_name_textbox.get()
    )

    output_folder = Folders(
        absolute_path_string=output_folder_name
    )

    short_name = (
        short_name_textbox.get()
    )

    return (
        input_file,
        output_folder,
        short_name,
    )
