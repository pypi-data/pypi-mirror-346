from dataclasses import dataclass

from django.conf import settings

from .constraints import (
    InvalidVersionError,
    TargetVersionMatchError,
    UpgradePaths,
    check_upgrade_possible,
)
from .models import Version
from .recorder import get_version_info


def _get_valid_upgrade_paths() -> UpgradePaths:
    paths = getattr(settings, "UPGRADE_CHECK_PATHS", {})
    return paths


@dataclass
class UpgradeCheckResult:
    ok: bool
    from_version: str
    to_version: str
    warning: str = ""
    error: str = ""


def run_upgrade_check() -> UpgradeCheckResult:
    """
    Gather the current and last recorded project versions and check any upgrades.

    The current version is taken from the code and interpreted as the "target version"
    to upgrade to. That *may* be the currently active version. The last recorded
    project version is taken from the database - we simply take the last recorded entry
    and deliberately don't do any additional timestamp checks or filtering to account
    for possible (small) clock drifts.
    """
    most_recent_recorded_version = (
        Version.objects.order_by("-timestamp").only("version").first()
    )
    # if we have no version history, any version can be deployed -> check passes
    if most_recent_recorded_version is None:
        return UpgradeCheckResult(ok=True, from_version="", to_version="")

    current: str = most_recent_recorded_version.version
    target = get_version_info()[0]
    strict: bool = getattr(settings, "UPGRADE_CHECK_STRICT", False)

    try:
        upgrade_possible = check_upgrade_possible(
            _get_valid_upgrade_paths(),
            from_version=current,
            to_version=target,
            raise_if_no_match=strict,
        )
    except InvalidVersionError as exc:
        return UpgradeCheckResult(
            ok=not strict,
            from_version=current,
            to_version=target,
            warning=exc.message if (not strict and not settings.DEBUG) else "",
            error=f"Invalid semver version provided. {exc.message}" if strict else "",
        )

    except TargetVersionMatchError as exc:
        return UpgradeCheckResult(
            ok=False,
            from_version=current,
            to_version=target,
            error=exc.message,
        )

    err_msg = (
        f"Upgrading from {current} to {target} is not possible (strict "
        f"checks: {'yes' if strict else 'no'})."
    )
    return UpgradeCheckResult(
        ok=upgrade_possible,
        from_version=current,
        to_version=target,
        error=err_msg if not upgrade_possible else "",
    )
