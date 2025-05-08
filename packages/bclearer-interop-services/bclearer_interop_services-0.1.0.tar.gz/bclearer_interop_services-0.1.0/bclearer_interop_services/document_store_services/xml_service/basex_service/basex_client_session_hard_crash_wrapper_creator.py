from typing import Optional

from BaseXClient import BaseXClient
from BaseXClient.BaseXClient import (
    Session,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def create_basex_session_hard_crash_wrapper(
    user_name: str,
    user_password: str,
) -> Session | None:
    try:
        session = BaseXClient.Session(
            "localhost",
            1984,
            user_name,
            user_password,
        )

        return session

    except Exception as error:
        log_message(
            message="An error occurred trying to create the BaseX session: "
            + str(error),
        )
