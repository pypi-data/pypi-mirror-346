import os

from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.relational_database_services.access_service.access import (
    read_access_into_dictionary_of_dataframes,
)
from bclearer_interop_services.relational_database_services.sqlite_service.dictionary_of_dataframes_to_sqlite_exporter import (
    export_dictionary_of_dataframes_to_sqlite,
)
from nf_common.code.services.reporting_service.reporters.log_file import (
    LogFiles,
)


# TODO: Add runner for this method (run_bapp)
def orchestrate_convert_access_to_sqlite(
    input_access_database_file: Files,
) -> None:
    dictionary_of_dataframes = read_access_into_dictionary_of_dataframes(
        input_access_database_file=input_access_database_file,
    )

    access_database_base_name = os.path.basename(
        input_access_database_file.absolute_path_string,
    ).split(
        ".",
    )[
        0
    ]

    export_dictionary_of_dataframes_to_sqlite(
        dictionary_of_dataframes=dictionary_of_dataframes,
        sqlite_database_base_name=access_database_base_name,
        output_folder=Folders(
            absolute_path_string=LogFiles.folder_path,
        ),
        sqlite_database_file=None,
        database_exists=False,
    )
