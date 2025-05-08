import os
import tkinter
from tkinter import filedialog

from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.common.gui_widgets.gui_widget_factory import (
    create_button,
    create_text_with_label,
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


def get_xlsx_to_eapx_parameters():
    def select_file():
        file_path = filedialog.askopenfile(
            parent=master,
            initialdir=os.getcwd(),
            title="Select xlsx file",
            filetypes=[
                (
                    "Excel files",
                    "*.xlsx",
                )
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
        string="Excel (xlsx) to EA Model (eapx)"
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

    package_sheets_listbox = create_text_with_label(
        master=master,
        row=3,
        label_text="Package sheets: ",
        initial_list=[
            NfEaComCollectionTypes.EA_PACKAGES.collection_name
        ],
    )

    classifier_sheets_listbox = create_text_with_label(
        master=master,
        row=4,
        label_text="Classifier sheets: ",
        initial_list=[
            NfEaComCollectionTypes.EA_CLASSIFIERS.collection_name
        ],
    )

    connector_sheets_listbox = create_text_with_label(
        master=master,
        row=5,
        label_text="Connector sheets: ",
        initial_list=[
            NfEaComCollectionTypes.EA_CONNECTORS.collection_name
        ],
    )

    stereotype_group_sheets_listbox = create_text_with_label(
        master=master,
        row=6,
        label_text="Stereotype Group sheets: ",
        initial_list=[
            NfEaComCollectionTypes.EA_STEREOTYPE_GROUPS.collection_name
        ],
    )

    stereotype_sheets_listbox = create_text_with_label(
        master=master,
        row=7,
        label_text="Stereotype sheets: ",
        initial_list=[
            NfEaComCollectionTypes.EA_STEREOTYPES.collection_name
        ],
    )

    stereotype_usage_sheets_listbox = create_text_with_label(
        master=master,
        row=8,
        label_text="Stereotype Usage sheets: ",
        initial_list=[
            NfEaComCollectionTypes.STEREOTYPE_USAGE.collection_name
        ],
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
        row=9,
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

    package_sheet_names = (
        package_sheets_listbox.get(
            "1.0", tkinter.END
        )
        .rstrip()
        .split("\n")
    )

    classifier_sheet_names = (
        classifier_sheets_listbox.get(
            "1.0", tkinter.END
        )
        .rstrip()
        .split("\n")
    )

    connector_sheet_names = (
        connector_sheets_listbox.get(
            "1.0", tkinter.END
        )
        .rstrip()
        .split("\n")
    )

    stereotype_group_sheet_names = (
        stereotype_group_sheets_listbox.get(
            "1.0", tkinter.END
        )
        .rstrip()
        .split("\n")
    )

    stereotype_sheet_names = (
        stereotype_sheets_listbox.get(
            "1.0", tkinter.END
        )
        .rstrip()
        .split("\n")
    )

    stereotype_usage_sheet_names = (
        stereotype_usage_sheets_listbox.get(
            "1.0", tkinter.END
        )
        .rstrip()
        .split("\n")
    )

    return (
        input_file,
        output_folder,
        short_name,
        package_sheet_names,
        classifier_sheet_names,
        connector_sheet_names,
        stereotype_group_sheet_names,
        stereotype_sheet_names,
        stereotype_usage_sheet_names,
    )
