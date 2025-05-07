=========
Changelog
=========

1.1.0 (2025-05-07)
==================

Feature release to improve developer experience.

* In lax mode, the upgrade version comparison is now compared with ``>=`` rather
  than ``~=``, meaning that newer versions enforce the requirements of the most recent
  upgrade target. Thanks to @danielmursa-dev for the contribution!

1.0.0 (2025-04-10)
==================

Django-upgrade-check is now feature complete.

* Added ability to run code checks.
* Added management command checks as built-in code check.

0.2.0 (2025-04-10)
==================

Initial preview release.

The package is extracted from Open Formulieren and published as re-usable library now.

**Features**

* Record deployed version(s) on post-migrate.
* Check (new) version against latest deployed version and upgrade check configuration.
* Ability to define valid upgrade paths in settings.
* Automatic system checks that prevent database mutations on invalid upgrade paths.

Currently missing features:

* Running management commands in checks
* Running project-specific check scripts
