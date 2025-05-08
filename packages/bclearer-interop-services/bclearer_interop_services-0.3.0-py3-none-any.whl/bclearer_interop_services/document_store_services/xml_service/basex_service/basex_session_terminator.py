import os.path
import subprocess

from BaseXClient.BaseXClient import (
    Session,
)
from bclearer_interop_services.file_system_service import (
    get_file_absolute_path,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def terminate_basex_session(
    drive_relative_path: str,
    basex_session: Session,
    file_name: str = "basexserverstop.bat",
) -> None:
    basex_session.close()

    subprocess_file_path = get_file_absolute_path(
        drive_relative_path=drive_relative_path,
        file_name=file_name,
    )

    if os.path.exists(
        subprocess_file_path,
    ):
        subprocess.Popen(
            [subprocess_file_path],
            stdout=subprocess.PIPE,
        )

    else:
        log_message(
            message="Subprocess file does not exist",
        )
