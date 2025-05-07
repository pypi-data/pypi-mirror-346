import logging
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from .models import Version, get_machine_name

logger = logging.getLogger(__name__)

IGNORE_DEPLOYMENTS_SINCE = 3600  # in seconds

type _Version = str
type _GitSha = str


def get_version_info() -> tuple[_Version, _GitSha]:
    """
    Read the version details from the settings/configured project.

    .. todo:: make this configurable via a callable. To be able to compare versions,
       they must adhere to semver though. For now, we use hardcoded setting names.
    """
    version: _Version = settings.RELEASE or "UNKNOWN"
    git_sha: _GitSha = settings.GIT_SHA or version
    return version, git_sha


def record_current_version() -> Version | None:
    """
    Extract the current version and record it in the database.

    We grab the current version from the project and the machine name that we're running
    on and attempt to record this deployment, applying some debouncing logic to avoid
    flooding the database.

    Returns the created version instance or ``None`` if nothing was created.
    """
    cutoff = timezone.now() - timedelta(seconds=IGNORE_DEPLOYMENTS_SINCE)
    machine_name = get_machine_name()
    version, git_sha = get_version_info()

    # check if we have a recorded version already for the same machine name to avoid
    # flooding the database (e.g. when there's a crashloop in kubernetes...)
    has_version = Version.objects.filter(
        machine_name=machine_name, version=version, timestamp__gte=cutoff
    ).exists()
    if has_version:
        extra = {
            "version": version,
            "machine": machine_name,
            "interval": IGNORE_DEPLOYMENTS_SINCE,
        }
        logger.info(
            "Version %(version)s was already recorded on machine %(machine)s in the "
            "past %(interval)d seconds.",
            extra,
            extra=extra,
        )
        return None

    return Version.objects.create(
        version=version,
        git_sha=git_sha,
        machine_name=machine_name,
    )
