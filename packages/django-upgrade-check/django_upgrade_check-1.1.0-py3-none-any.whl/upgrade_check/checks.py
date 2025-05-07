import logging
from collections.abc import Sequence

from django.apps.config import AppConfig
from django.core.checks import CheckMessage, Error, Warning, register
from django.db import OperationalError, ProgrammingError

from .upgrade_checks import UpgradeCheckResult, run_upgrade_check

logger = logging.getLogger(__name__)


@register()
def check_upgrade_possible(
    app_configs: Sequence[AppConfig] | None,
    **kwargs,
) -> list[CheckMessage]:
    """
    Check that upgrading from this version of the code is possible.

    System checks that raise errors prevent migrations from running, so an older
    version of the code can be deployed for a well defined, incremental upgrade path.

    These checks always run and the provided app configs are ignored.
    """
    try:
        result = run_upgrade_check()
    except (ProgrammingError, OperationalError) as exc:
        # the database table was not created yet or the connection parameters are wrong.
        # We can reasonably assume that this is the first time the version history is
        # being used.
        logger.info("Skipping check because the DB looks uninitialized", exc_info=exc)
        return []

    match result:
        case UpgradeCheckResult(ok=False, error=str() as err):
            return [
                Error(
                    f"The upgrade checks detected a problem:\n\n{err}",
                    hint=(
                        "There may be upgrade instructions in the changelog/release "
                        "notes. It should be safe to roll back the previous version."
                    ),
                    id="upgrade_check.E001",
                )
            ]
        case UpgradeCheckResult(ok=True, warning=""):
            return []
        case UpgradeCheckResult(ok=True, warning=str() as msg):
            return [
                Warning(
                    "Could not reliably check the upgrade path - apply caution.",
                    hint=msg,
                    id="upgrade_check.W001",
                )
            ]
        case _:  # pragma: no cover
            assert False, "unreachable"
