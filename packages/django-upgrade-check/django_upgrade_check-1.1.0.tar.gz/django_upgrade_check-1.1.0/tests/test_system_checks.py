import logging

from django.core.checks import Error, Warning
from django.db import connection

import pytest

from upgrade_check.checks import check_upgrade_possible
from upgrade_check.constraints import UpgradeCheck, VersionRange
from upgrade_check.models import Version


@pytest.mark.django_db
def test_db_errors_are_non_fatal(caplog: pytest.LogCaptureFixture):
    """
    Check that DB errors don't block migrating initially.

    On fresh installs the database tables haven't been created yet, and system checks
    must pass for the initial migrate command to create the necessary tables.
    """
    # drop the table to force DB errors
    with connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE {Version._meta.db_table};")

    with caplog.at_level(logging.INFO, logger="upgrade_check.checks"):
        result = check_upgrade_possible(None)

    assert result == []
    assert "Skipping check because the DB looks uninitialized" in caplog.text


def test_upgrade_possible_no_errors_or_warnings(settings):
    settings.RELEASE = "2.0.1"
    settings.UPGRADE_CHECK_PATHS = {
        "2.0.0": UpgradeCheck(VersionRange(minimum="1.0.0")),
    }
    Version.objects.create(version="1.0.3")

    result = check_upgrade_possible(None)

    assert result == []


def test_upgrade_not_possible_reports_error(settings):
    settings.RELEASE = "2.0.1"
    settings.UPGRADE_CHECK_PATHS = {
        "2.0.0": UpgradeCheck(VersionRange(minimum="1.2.0")),
    }
    Version.objects.create(version="1.0.3")

    result = check_upgrade_possible(None)

    expected_error = Error(
        (
            "The upgrade checks detected a problem:\n\n"
            "Upgrading from 1.0.3 to 2.0.1 is not possible (strict checks: no)."
        ),
        hint=(
            "There may be upgrade instructions in the changelog/release notes. "
            "It should be safe to roll back the previous version."
        ),
        id="upgrade_check.E001",
    )
    assert result == [expected_error]


def test_invalid_version_warning_emitted_with_debug_false(settings):
    settings.DEBUG = False
    settings.UPGRADE_CHECK_STRICT = False
    settings.RELEASE = "dev"
    settings.UPGRADE_CHECK_PATHS = {
        "2.0.0": UpgradeCheck(VersionRange(minimum="1.2.0")),
    }
    Version.objects.create(version="1.2.0")

    result = check_upgrade_possible(None)

    expected_warning = Warning(
        "Could not reliably check the upgrade path - apply caution.",
        hint="Invalid version string: 'dev'",
        id="upgrade_check.W001",
    )
    assert result == [expected_warning]


def test_invalid_version_no_warning_emitted_with_debug_true(settings):
    settings.DEBUG = True
    settings.UPGRADE_CHECK_STRICT = False
    settings.RELEASE = "dev"
    settings.UPGRADE_CHECK_PATHS = {
        "2.0.0": UpgradeCheck(VersionRange(minimum="1.2.0")),
    }
    Version.objects.create(version="1.2.0")

    result = check_upgrade_possible(None)

    assert result == []
