from dataclasses import dataclass

import pytest
from semantic_version import Version

from upgrade_check.constraints import (
    CommandCheck,
    InvalidVersionError,
    TargetVersionMatchError,
    UpgradeCheck,
    VersionRange,
    check_upgrade_possible,
)


@pytest.mark.parametrize(
    "minimum,maximum,test,expected_result",
    [
        # no maximum version
        ("1.0.0", "", "1.0.0", True),
        ("1.0.0", "", "1.1.0", True),
        ("1.0.0", "", "1.0.1", True),
        ("1.0.0", "", "2.0.0", True),
        ("1.0", "", "2.0.0", True),
        ("1", "", "2.0.0", True),
        ("1.0.0", "", "0.99", False),
        ("1.1", "", "0.99", False),
        ("1", "", "0.99", False),
        ("2.0.3", "", "2.0.2", False),
        # with maximum version
        ("1.0.0", "1.1.0", "1.0.0", True),
        ("1.0.0", "1.1.0", "1.1.0", True),
        ("1.0.0", "1.1.0", "1.1.1", False),
        ("1.0.0", "1.1.0", "2.0.0", False),
        ("1.0.0", "2", "1.5.10", True),
        ("1.0.0", "2", "2.0.0", True),
        ("1.0.0", "2", "2.0.1", False),
        ("1.0.0", "2", "2.1.0", False),
        ("1.0.0", "2", "3.0.0", False),
        # unspecified patch
        ("2.1", "", "2.1.0", True),
        ("2.1", "", "2.1.3", True),
        ("2.1", "", "2.0.999", False),
        # unspecified minor
        ("2", "", "2.0.0", True),
        ("2", "", "1.0.0", False),
        ("2", "", "2.1.0", True),
    ],
)
def test_containment(minimum: str, maximum: str, test: str, expected_result: bool):
    version_range = VersionRange(minimum=minimum, maximum=maximum)

    result = version_range.contains(Version.coerce(test))

    assert result == expected_result


@pytest.mark.parametrize(
    "test_version,expected",
    [
        ("1.0.0", False),
        ("1.1.2", False),
        ("1.1.3", True),
        ("1.2.0", True),
        ("2.0.0", True),
        ("2.0.1", False),
        ("2.1.0", False),
    ],
)
def test_ugprade_check_single_range(test_version: str, expected: bool):
    check = UpgradeCheck(valid_range=VersionRange(minimum="1.1.3", maximum="2.0.0"))
    current_version = Version(test_version)

    result = check.check_version(current_version)

    assert result == expected


def test_upgrade_check_collection_set_hashing():
    check = UpgradeCheck(
        valid_range={
            VersionRange(minimum="1.1.3", maximum="1.1.5"),
            VersionRange(minimum="1.2.0", maximum="2.0.0"),
        }
    )

    num_ranges = len(check.valid_ranges)

    assert num_ranges == 2


@pytest.mark.parametrize(
    "test_version,expected",
    [
        ("1.0.0", False),
        ("1.1.2", False),
        ("1.1.3", True),
        ("1.1.5", True),
        ("1.1.6", False),
        ("1.2.0", True),
        ("2.0.0", True),
        ("2.0.1", False),
        ("2.1.0", False),
    ],
)
def test_ugprade_check_multiple_ranges(test_version: str, expected: bool):
    check = UpgradeCheck(
        valid_range={
            VersionRange(minimum="1.1.3", maximum="1.1.5"),
            VersionRange(minimum="1.2.0", maximum="2.0.0"),
        }
    )
    current_version = Version(test_version)

    result = check.check_version(current_version)

    assert result == expected


UPGRADE_CONFIG = {
    "1.4": UpgradeCheck(
        {
            VersionRange(minimum="1.2.2", maximum="1.2.9"),
            VersionRange(minimum="1.3.4"),
        }
    ),
    "1.4.9": UpgradeCheck(VersionRange(minimum="1.4.3")),
}


@pytest.mark.parametrize(
    "from_version,to_version,expected_result",
    [
        ("1.0.0", "1.4.0", False),
        ("1.2.1", "1.4.0", False),
        ("1.2.1", "1.5.0", False),
        ("1.2.2", "1.5.0", True),
        ("1.2.2", "1.4.0", True),
        ("1.2.3", "1.4.0", True),
        ("1.2.3", "1.4.1", True),
        ("1.2.3", "1.4.2", True),
        ("1.2.9", "1.4.2", True),
        ("1.2.10", "1.4.2", False),
        ("1.3.3", "1.4.0", False),
        ("1.3.3", "1.5.0", False),
        ("1.3.4", "1.4.0", True),
        ("1.3.4", "1.5.0", True),
        ("1.3.999", "1.4.999", True),
        ("1.4.0", "1.4.0", True),
        ("1.3.5", "1.4.9", False),
        ("1.3.5", "1.5.0", True),
        ("1.4.4", "1.4.9", True),
        ("1.4.4", "1.5.0", True),
    ],
)
def test_upgrade_possible(from_version: str, to_version: str, expected_result: bool):
    result = check_upgrade_possible(
        UPGRADE_CONFIG,
        from_version=from_version,
        to_version=to_version,
        raise_if_no_match=False,
    )

    assert result == expected_result


def test_upgrade_possible_no_match_strict_mode():
    with pytest.raises(TargetVersionMatchError):
        check_upgrade_possible(
            UPGRADE_CONFIG,
            from_version="1.4.10",
            to_version="2.1.0",
            raise_if_no_match=True,
        )


def test_upgrade_possible_no_match_lax_mode():
    result = check_upgrade_possible(
        UPGRADE_CONFIG,
        from_version="1.4.10",
        to_version="2.1.0",
        raise_if_no_match=False,
    )

    assert result is True


def test_dont_block_if_already_in_target_range():
    result = check_upgrade_possible(
        {"2.0": UpgradeCheck(VersionRange(minimum="1.1.0", maximum="1.1.9"))},
        from_version="2.0.1",
        to_version="2.0.2",
    )

    assert result is True


@pytest.mark.parametrize(
    "from_version,to_version",
    [
        ("1.0", "1.4.0"),
        ("1.0.0", "1.4"),
        ("2025.4", "1.4.9"),
    ],
)
def test_invalid_input_versions(from_version: str, to_version: str):
    with pytest.raises(InvalidVersionError):
        check_upgrade_possible(
            UPGRADE_CONFIG, from_version=from_version, to_version=to_version
        )


def test_management_command_fails_check():
    upgrade_config = {
        "1.1.0": UpgradeCheck(
            valid_range=VersionRange(minimum="1.0.0"),
            code_checks=[
                CommandCheck("fail_upgrade_check", options={"fail": True}),
            ],
        )
    }

    result = check_upgrade_possible(
        upgrade_config, from_version="1.0.0", to_version="1.1.0"
    )

    assert result is False


def test_management_command_passes_check():
    upgrade_config = {
        "1.1.0": UpgradeCheck(
            valid_range=VersionRange(minimum="1.0.0"),
            code_checks=[CommandCheck("fail_upgrade_check")],
        )
    }

    result = check_upgrade_possible(
        upgrade_config, from_version="1.0.0", to_version="1.1.0"
    )

    assert result is True


@dataclass
class Check:
    outcome: bool

    def execute(self) -> bool:
        return self.outcome


def test_custom_code_check_pass():
    upgrade_config = {
        "1.1.0": UpgradeCheck(
            valid_range=VersionRange(minimum="1.0.0"),
            code_checks=[Check(outcome=True)],
        )
    }

    result = check_upgrade_possible(
        upgrade_config, from_version="1.0.0", to_version="1.1.0"
    )

    assert result is True


def test_custom_code_check_fail():
    upgrade_config = {
        "1.1.0": UpgradeCheck(
            valid_range=VersionRange(minimum="1.0.0"),
            code_checks=[Check(outcome=False)],
        )
    }

    result = check_upgrade_possible(
        upgrade_config, from_version="1.0.0", to_version="1.1.0"
    )

    assert result is False
