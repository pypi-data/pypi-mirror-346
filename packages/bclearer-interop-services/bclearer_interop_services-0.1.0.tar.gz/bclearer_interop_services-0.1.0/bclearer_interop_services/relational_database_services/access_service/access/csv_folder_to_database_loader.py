from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def load_database_with_table(
    db_connection,
    table_name: str,
    csv_folder: Folders,
):
    full_csv_path = (
        csv_folder.absolute_path_string
    )

    sql_query = (
        "SELECT * INTO "
        + table_name[:-4]
        + " FROM [text;HDR=Yes;FMT=Delimited(,);CharacterSet=65001;Database="
        + full_csv_path
        + "]."
        + table_name
        + ";"
    )

    log_message(message=sql_query)

    cursor = db_connection.cursor()

    cursor.execute(sql_query)

    db_connection.commit()
