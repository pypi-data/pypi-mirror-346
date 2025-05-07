import logging
from io import StringIO

from django.core.management import call_command

import pytest

from upgrade_check.models import Version, get_machine_name
from upgrade_check.recorder import record_current_version


@pytest.mark.django_db
def test_record_new_version(settings):
    settings.RELEASE = "1.2.3"
    settings.GIT_SHA = "abcd1234"
    assert not Version.objects.exists()

    record_current_version()

    version = Version.objects.get()

    assert version.version == "1.2.3"
    assert version.git_sha == "abcd1234"
    assert version.timestamp is not None
    assert version.machine_name != ""
    assert "1.2.3@" in str(version)


@pytest.mark.django_db
def test_record_new_version_debounce(settings, caplog: pytest.LogCaptureFixture):
    settings.RELEASE = "1.2.3"
    settings.GIT_SHA = "abcd1234"
    assert record_current_version() is not None

    # recording again in quick succession should debounce
    with caplog.at_level(logging.INFO, logger="upgrade_check.recorder"):
        result = record_current_version()

    machine_name = get_machine_name()
    assert (
        f"Version 1.2.3 was already recorded on machine {machine_name} in the past "
        "3600 seconds."
    ) in caplog.text

    assert result is None
    assert Version.objects.count() == 1


@pytest.mark.django_db
def test_record_new_version_no_debounce_different_version(settings):
    settings.RELEASE = "1.2.3"
    settings.GIT_SHA = "abcd1234"
    assert record_current_version() is not None

    settings.RELEASE = "2.3.0"
    result = record_current_version()

    assert result is not None
    assert Version.objects.count() == 2


@pytest.mark.django_db
def test_migrate_records_version(settings):
    settings.RELEASE = "1.2.3"
    assert not Version.objects.exists()

    call_command("migrate", stdout=StringIO(), stderr=StringIO(), verbosity=0)

    version = Version.objects.get()
    assert version.version == "1.2.3"
