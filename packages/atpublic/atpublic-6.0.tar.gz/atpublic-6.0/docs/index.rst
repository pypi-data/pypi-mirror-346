=========================================
 Documenting the public interface
=========================================

.. currentmodule:: public

This library provides two decorators that document the public visibility of the names in your
module.  They keep your module's ``__all__`` in sync so you don't have to.

Also included is a function that you can put at the bottom of your module to simply infer all the public
names, and populate the ``__all__`` for you.

Please note that while the package is called :doc:`public <apiref>` and it provides a top-level module named
``public``, the PyPI package is called ``atpublic`` due to name conflicts.


Requirements
============

``public`` requires Python 3.9 or newer.


Documentation
=============

More information is available in the :doc:`user guide <using>` and the :doc:`API reference <apiref>`.


Project details
===============

 * Project home: https://gitlab.com/warsaw/public
 * Report bugs at: https://gitlab.com/warsaw/public/issues
 * Code hosting: https://gitlab.com/warsaw/public.git
 * Documentation: https://public.readthedocs.io
 * PyPI: https://pypi.python.org/pypi/atpublic

You can install it with `pip`::

    % pip install atpublic

**Do not install "public"; that is a different package!**

You can grab the latest development copy of the code using git.  The main
repository is hosted on GitLab.  If you have git installed, you can grab
your own branch of the code like this::

    $ git clone https://gitlab.com/warsaw/public.git

You can contact the author via barry@python.org.


Copyright
=========

Copyright (C) 2016-2025 Barry A. Warsaw

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Table of Contents and Index
===========================

* :ref:`genindex`

.. toctree::
    :glob:

    using
    apiref
    NEWS
