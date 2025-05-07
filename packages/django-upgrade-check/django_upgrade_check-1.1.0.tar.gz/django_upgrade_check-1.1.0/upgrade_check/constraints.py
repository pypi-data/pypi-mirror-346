"""
Provide interfaces to express upgrade constraints.

Upgrades can be constrained by simple (prior) version requirements, management commands
that need to pass or arbitrary callbacks to allow for varying degrees of flexibility
and project-specific checks.

We currently only support SemVer for the version comparisons.
"""

from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Protocol

from django.core.management import CommandError, call_command

from semantic_version import SimpleSpec, Version

__all__ = [
    "VersionRange",
    "UpgradeCheck",
    "UpgradePaths",
    "InvalidVersionError",
    "TargetVersionMatchError",
    "check_upgrade_possible",
]

OP_GREATER_OR_EQUAL = ">="
OP_COMPATIBLE = "~="


@dataclass(slots=True, unsafe_hash=True)
class VersionRange:
    """
    Describe a minimum required version and optional upper bound.

    The version range bounds are inclusive. E.g. a range of ``1.0.3 - 1.0.5`` covers
    the versions ``1.0.3``, ``1.0.4`` and ``1.0.5``.

    ``VersionRange`` instances are intended to be immutable.
    """

    minimum: str
    """
    The minimum version, typically expressed as major.minor.patch.

    You can specify partial versions like ``1.1`` if the exact patch version is not
    relevant.
    """
    maximum: str = ""
    """
    The upper bound, optional. If unspecified, there is no upper bound.

    If you specify a partial range like ``2.0``, anything newer than ``2.0.0`` will
    be considered out of range.
    """
    _min_version: Version = field(init=False)
    _max_version: Version | None = field(init=False)

    def __post_init__(self):
        self._min_version = Version.coerce(self.minimum)
        self._max_version = Version.coerce(self.maximum) if self.maximum else None

    def contains(self, in_version: Version):
        if in_version < self._min_version:
            return False
        if self._max_version and in_version > self._max_version:
            return False
        return True


class CodeCheck(Protocol):
    """
    Run a code-based check.

    The ``execute`` method must return a boolean indicating a pass (``True``) or fail
    (``False``). Code checks are responsible for their own error reporting to
    stdout/stderr.
    """

    def execute(self) -> bool: ...


class CommandCheck:
    """
    A management command and its options to call as part of the upgrade check.

    :arg command: Name of the management command to call.
    :arg options: Any additional keyword arguments are forwarded to the
        ``call_command`` call.
    """

    def __init__(self, command: str, *, options: dict[str, object] | None = None):
        self.command = command
        self.options = options

    def execute(self) -> bool:
        """
        Execute the management command.

        If it doesn't return, treat the check as success. If it raises ``CommandError``,
        fail the check. Management commands are responsible for their own output.

        :return: ``True`` indicating success, ``False`` if the check failed.
        """
        options = self.options or {}
        try:
            call_command(self.command, **options)
        except CommandError:
            return False
        else:
            return True


class UpgradeCheck:
    """
    Define the conditions for a valid upgrade check.

    Provide either a :class:`VersionRange` or a collection of version ranges to test if
    this check passes. The version number check passes as soon as one range satisfies
    the provided version.

    .. todo:: support management command checks
    .. todo:: support arbitrary callables/callbacks for additional (script) checks
    """

    valid_ranges: Collection[VersionRange]
    code_checks: Sequence[CodeCheck]

    def __init__(
        self,
        valid_range: VersionRange | Collection[VersionRange],
        code_checks: Sequence[CodeCheck] = (),
    ):
        # normalize to a collection
        self.valid_ranges = (
            (valid_range,) if isinstance(valid_range, VersionRange) else valid_range
        )
        self.code_checks = code_checks

    def check_version(self, current_version: Version) -> bool:
        """
        Check if the provided version is contained in any of the valid ranges.

        :arg current_version: The version the application is currently at.
        """
        for version_range in self.valid_ranges:
            if version_range.contains(current_version):
                return True
        return False


type UpgradePaths = Mapping[str, UpgradeCheck]
"""
A mapping of target version strings to their checks that must pass.

Defining a version with an upgrade check dictates that those checks must pass before
the application can be upgraded to the specified version.
"""


class InvalidVersionError(ValueError):
    def __init__(self, message: str, *args):
        self.message = message
        super().__init__(message, *args)


class TargetVersionMatchError(ValueError):
    def __init__(self, message: str, *args):
        self.message = message
        super().__init__(message, *args)


def check_upgrade_possible(
    upgrade_paths: UpgradePaths,
    *,
    from_version: str,
    to_version: str,
    raise_if_no_match: bool = False,
) -> bool:
    """
    Test if upgrading from ``from_version`` to ``to_version`` is possible.

    :arg upgrade_paths: The upgrade path configuration, specifying which checks apply
      for which target/upgrade version.
    :arg from_version: The starting version - must be a version string in SemVer format.
    :arg to_version: The target version - must be a version string in SemVer format.
    """
    if from_version == to_version:
        return True

    try:
        _from_version = Version(from_version)
        _to_version = Version(to_version)
    except ValueError as exc:
        raise InvalidVersionError(str(exc)) from exc

    # find the most appropriate constraint - check for exact matches first
    operator = OP_GREATER_OR_EQUAL if not raise_if_no_match else OP_COMPATIBLE
    target_version: str
    if to_version in upgrade_paths:
        target_version = to_version
        compare_spec = SimpleSpec(f"{operator}{target_version}")
    else:
        for target_version in upgrade_paths:
            # 2. Check the ~=X.Y.x version range, which allows the major.minor range.
            # E.g. 2.0.1 matches ~= 2.0.0, but 2.1.0 does not. Similarly, 1.5 matches
            # ~= 1.4 (!).
            compare_spec = SimpleSpec(f"{operator}{target_version}")
            if _to_version in compare_spec:
                break
        else:
            # no match found - could be deliberate, could be a mistake -> users can
            # opt into strict mode
            if raise_if_no_match:
                raise TargetVersionMatchError(
                    f"No match found for target version '{to_version}'."
                )
            return True

    assert target_version
    # if we have a loose spec (e.g. 2.0) and you're already on 2.0.x, ensure we skip
    # the upgrade checks.
    if _from_version in compare_spec:
        return True

    upgrade_check = upgrade_paths[target_version]
    version_check_ok = upgrade_check.check_version(_from_version)
    if not version_check_ok:
        return False

    for code_check in upgrade_check.code_checks:
        success = code_check.execute()
        if not success:
            return False

    return True
