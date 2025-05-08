=====================
flufl.enum change log
=====================

7.0 (2025-05-07)
================
* Iteration over enum items now preserves the order of their definition. (:GL:`9`)
* Documentation improvements.
* Add support for Python 3.13 and 3.14; remove support for Python 3.8.
* Fix test suite for running on older Pythons.

6.1 (2024-03-30)
================
* Add support for Python 3.12. (:GL:`6`)
* Switch to ``hatch``, replacing ``pdm`` and ``tox``. (:GL:`7`)
* Switch to ``ruff`` from ``blue`` and ``isort``.  (:GL:`8`)

6.0.2 (2023-07-16)
==================
* Update dependencies.
* Minor documentation updates.

6.0.1 (2023-06-26)
==================
* Update dependencies.
* This release also utilizes a newer ``pdm-backend`` which fixes the project
  metadata.

6.0 (2023-06-05)
================
* Drop Python 3.7 support. (:GL:`4`)
* Switch from ``flake8`` and ``isort`` to ``ruff`` for code quality. (:GL:`5`)
* More GitLab CI integration improvements.
* Bump dependencies.

5.0.1 (2022-09-03)
==================
* Update ``pyproject.toml`` to latest pdm.
* Update dependencies eagerly.
* Improvements to the GitLab CI integration.

5.0 (2022-08-25)
================
Backward incompatibilities:

* Removed all Python 2 support, and Python 2-isms.
* Removed all remaining previously deprecated functionality.
* Dropped support for Python < 3.7; add support for Python up to 3.11.
* Switched to the Apache License Version 2.0.
* Changed the way ``Enum[]`` and ``Enum()`` syntax are used to access enum
  items, to be more aligned with Python 3's standard ``enum`` library.  Now
  you use ``Enum[]`` to look up an enum value by attribute name, and you use
  ``Enum()`` to look up an enum value by value.  The one difference remaining
  is that with ``flufl.enum`` you can use ``Enum[]`` to look up an enum value
  by providing an enum value (standard library ``enum`` does not support this
  mode).

Code and Documentation:

* Added ``@public`` where appropriate.
* Fixed some typos in the README.
* Added an API reference document.
* Updated dependencies.

Housekeeping:

* Source tree reorganization.
* The ``master`` branch is renamed to ``main``.
* Updated copyright years.
* 100% coverage; mypy clean; i-blue-it
* Use ``pdm`` as the package manager, and switch to ``pyproject.toml``.
* Switched to the ``pytest`` runner.

4.1.1 (2017-01-24)
==================
* Support Python 3.6.  (Closes #1)

4.1 (2015-10-09)
================
* Fix the regexp that matches identifiers in the functional API.
  (LP: #1167052)
* Deprecate using getitem syntax for accessing enum values by attribute
  name.  Use ``getattr(Enum, name)`` instead.  (LP: #1167091)
* Duplicate enum values error now provides information on the attribute names
  that produced the conflict.  Given by Eli Bendersky.
* The documentation now makes it clear that iteration sort order is not
  guaranteed for ``Enum`` but *is* guaranteed for ``IntEnum``.
* Comparison operators now return ``NotImplemented`` which cause their use to
  raise ``TypeError`` instead of ``NotImplementedError``.  This is for
  consistency with Python 3.  In Python 2, we raise the ``TypeError``
  explicitly.
* ``repr(Enum)`` now sorts in attribute name order, as does iteration over
  ``Enum``.  Iteration over ``IntEnum`` is sorted by the enumeration item
  values (which must be integers).
* ``Enum.__getattr__()`` and special treatment for ``__members__`` is
  removed.  A ``__dir__()`` is provided to limit ``dir(Enum)`` to just the
  enumeration item names.
* As per BDFL request, document the ``__value_factory__`` API.
* Add support for Python 3.5 and drop support for Python 2.6.

4.0.1 (2014-06-11)
==================
* Include MANIFEST.in and tox.ini in the sdist tarball, otherwise the Debian
  package won't built correctly.
* Drop use of distribute.
* Narrow tox supported environments.
* Bump copyright years.

4.0 (2013-04-05)
================
* Fix documentation bugs.  (LP: #1026403, LP: #1132830)
* Deprecate ``EnumValue.__int__()``; use ``IntEnumValue`` (via ``IntEnum``)
  instead.
* Add ``IntEnum`` class which returns int-subclass enum values. (LP: #1132976)
  - Add ``__index__()`` method to support slicing.  (LP: #1132972)
  - Add non-deprecated ``__int__()`` method.
* Deprecate ``make()``; use ``Enum()`` instead.
  - Call ``IntEnum()`` to create integer valued enums.  (LP: #1162375)
  - Accept a space-separate string of enum values which are auto-split.
  - Accept a dictionary of enumeration name/value pairs.
* Add ``.value`` attribute to enum values.  (LP: #1132859)
* For ``__getitem__()`` and ``__call__()``, fall back to using the ``.value``
  attribute if the argument has one. (LP: #1124596)
* Previously deprecated APIs ``EnumValue.enumclass``, ``EnumValue.enumname``,
  and ``enum.make_enum()`` are removed.  (LP: #1132951)
* Small change to the ``repr`` of enum values; they now say "value=" instead
  of "int=".
* Multiple enum values now raise a `ValueError` instead of a `TypeError`.

3.3.2 (2012-04-19)
==================
* Add classifiers to setup.py and make the long description more compatible
  with the Cheeseshop.
* Other changes to make the Cheeseshop page look nicer.  (LP: #680136)
* setup_helper.py version 2.1.

3.3.1 (2012-01-19)
==================
* Fix Python 3 compatibility with Sphinx's conf.py ($python setup.py install).

3.3 (2012-01-19)
================
* Remove the dependency on 2to3 for Python 3 support; support Python 3
  directly with a single code base.
* flufl.enum.make_enum() is deprecated in favor of flufl.enum.make() which
  provides a better API.  (LP: #839529)
* Updated to distribute 0.6.19.
* Moved all documentation to .rst suffix.
* Make test_deprecations() compatible with Python 3 and Python 2.
* Removed markup for pylint.
* Improve documentation to illustrate that enum values with similar names and
  integer representations still do not hash equally.  (Found by Jeroen
  Vermeulen).

3.2 (2011-08-19)
================
* make_enum() accepts an optional `iterable` argument to provide the values
  for the enums.
* The .enumclass and .enumname attributes are deprecated.  Use .enum and
  .name instead, respectively.
* Improve the documentation regarding ordered comparisons and equality
  tests.  (LP: #794853)
* make_enum() now enforces the use of valid Python identifiers. (LP: #803570)

3.1 (2011-03-01)
================
* New convenience function `make_enum()`. (Contributed by Michael Foord)
* Fix `from flufl.enum import *`.
* Enums created with the class syntax can be pickled and unpickled.
  (Suggestion and basic implementation idea by Phillip Eby).

3.0.1 (2010-06-07)
==================
* Fixed typo which caused the package to break.

3.0 (2010-04-24)
================
* Package renamed to flufl.enum.

2.0.2 (2010-01-29)
==================
* Fixed some test failures when running under 2to3.

2.0.1 (2010-01-08)
==================
* Fix the manifest and clarify license.

2.0 (2010-01-07)
================
* Use Sphinx to build the documentation.
* Updates to better package Debian/Ubuntu.
* Use distribute_setup instead of ez_setup.
* Rename pep-xxxx.txt; this won't be submitted as a PEP.
* Remove dependencies on nose and setuptools_bzr
* Support Python 3 via 2to3.
