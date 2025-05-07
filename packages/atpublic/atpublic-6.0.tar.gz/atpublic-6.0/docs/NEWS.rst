==================
@public change log
==================

6.0 (2025-05-06)
================
* Added ``populate_all()`` which can be called from the bottom of your module to infer and populate your
  module's ``__all__``.  Use this if you don't like the decorator syntax.  (:GL:`27`)
* Documentation improvements.

5.1 (2025-01-23)
================
* Drop official support for Python 3.8, add support for Python 3.13.

5.0 (2024-07-24)
================
* ``@public`` is now properly type annotated.
* Adopt ``hatch test`` and ``hatch fmt`` commands. (:GL:`25`)
* ``@public`` and ``@private`` now raise ``TypeError`` instead of
  ``ValueError`` if ``__all__`` is not a concrete ``list`` object. (:GL:`26`)
* Other minor coding improvements identified by ``ruff``.
* Switch to `Trusted Publishing
  <https://docs.pypi.org/trusted-publishers/adding-a-publisher/#gitlab-cicd>`_
  for publishing new versions to PyPI.  (:GL:`24`)

4.1 (2024-03-29)
================
* Add support for Python 3.12. (:GL:`22`)
* Switch to ``hatch``, replacing ``pdm`` and ``tox``. (:GL:`21`)

4.0 (2023-06-05)
================
* Drop Python 3.7 support. (:GL:`16`)
* Remove ``public.install()`` which was used to inject the ``public`` and
  ``private`` functions into the ``builtins`` namespace.  This isn't very
  helpful and could be actively harmful.  Explicit is better than
  implicit. (:GL:`14`)
* The functional form of ``public()`` now returns the argument *values* in the
  order they are given.  This allows you to explicitly bind those values to
  names in the global namespace.  While this is redundant, it does solve some
  linter problems.  (:GL:`12`)
* Switch from ``flake8`` and ``isort`` to ``ruff`` for code quality. (:GL:`32`)
* Bump dependencies.

3.1.2 (2023-05-31)
==================
* Switch to ``pdm-backend`` (:GL:`15`)
* Bump dependencies.
* More GitLab CI integration improvements.

3.1.1 (2022-09-02)
==================
* Improvements to the GitLab CI integration.

3.1 (2022-08-27)
================
* Fix a typo in pyproject.toml file.
* Exclude certain local cache files from the sdist/wheel.
* Add support for Python 3.11.
* Updates for pdm and dependencies.

3.0.1 (2022-01-10)
==================
* Fix a typo in the README.rst.

3.0 (2022-01-10)
================
* Use modern package management by adopting `pdm
  <https://pdm.fming.dev/>`_ and ``pyproject.toml``, and dropping ``setup.py``
  and ``setup.cfg``.
* Build the docs with Python 3.8.
* Update to version 3.0 of `Sybil <https://sybil.readthedocs.io/en/latest/>`_.
* Adopt the `Furo <https://pradyunsg.me/furo/quickstart/>`_ documentation theme.
* Use `importlib.metadata.version()
  <https://docs.python.org/3/library/importlib.metadata.html#distribution-versions>`_
  as a better way to get the package version number for the documentation.
* Drop Python 3.6 support.
* Update Windows GitLab runner to include Python 3.10.
* Update copyright years.
* The ``master`` branch is renamed to ``main``. (:GL:`11`)

2.3 (2021-04-13)
================
* Do type hinting the right way. (:GL:`10`)

2.2 (2021-04-13)
================
* ``public()`` and ``private()`` can't be correctly type annotated, so the
  type hints on these two functions have been removed.  The ``ModuleAware``
  was also removed.  (:GL:`10`)
* Added a ``py.typed`` file to satisfy type checkers.  (:GL:`9`)
* Fixed a documentation cross-reference bug.

2.1.3 (2021-02-15)
==================
* I `blue <https://blue.readthedocs.io/en/latest/>`_ it!

2.1.2 (2021-01-01)
==================
* Update copyright years.
* Include ``test/__init__.py`` and ``docs/__init__.py`` (:GL:`9`)

2.1.1 (2020-10-22)
==================
* Rename top-level tests/ directory to test/ (:GL:`8`)

2.1 (2020-10-21)
================
* Clean up some typing problems.
* Reorganized docs and tests out of the code directory (:GL:`7`).
* Fix the Windows CI tests.

2.0 (2020-07-27)
================
* Drop Python 3.4 and 3.5; add Python 3.8 and 3.9.
* The C implementation is removed. (:GL:`4`)
* Added an ``@private`` decorator (:GL:`3`)
* Build and test on Windows in addition to Linux.
* Fix the doctests so that they actually run and pass!
* Add type annotations and API reference documentation.
* Internal improvements and modernizations.

1.0 (2017-09-15)
================
* 1.0 release.
* Documentation improvements.

0.5 (2016-12-14)
================
* Fix MANIFEST.in inclusion of the src directory for the C extension.

0.4 (2016-11-28)
================
* Add Python 3.6 support.
* Make building the C extension optional, for environments without a C
  compiler.

0.3 (2016-05-25)
================
* Raise ``ValueError`` when ``__all__`` isn't a list (or subclass) instance.

0.2 (2016-05-22)
================
* Documentation updates based on initial feedback.
* Some minor test suite clean up.

0.1 (2016-05-09)
================
* Initial release.
