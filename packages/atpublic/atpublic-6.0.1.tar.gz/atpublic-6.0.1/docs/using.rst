==================================
 Documenting the public interface
==================================

This library provides two decorators that document the public visibility of the names in your
module.  They keep your module's ``__all__`` in sync so you don't have to.

Also included is a function that you can put at the bottom of your module to simply infer all the public
names, and populate the ``__all__`` for you.


Background
==========

``__all__`` is great.  It has both functional and documentation purposes.

The functional purpose is that it `directly controls`_ which module names are
imported by the ``from <module> import *`` statement.  In the absence of an
``__all__``, when this statement is executed, every name in ``<module>`` that
does not start with an underscore will be imported.  This often leads to
importing too many names into the module.  That's a good enough reason not to
use ``from <module> import *`` with modules that don't have an ``__all__``.

In the presence of an ``__all__``, only the names specified in this list are
imported by the ``from <module> import *`` statement.  This in essence gives
the ``<module>`` author a way to explicitly state which names are for public
consumption.

And that's the second purpose of ``__all__``; it serves as module
documentation, explicitly naming the public objects it wants to export.  You
can print a module's ``__all__`` and get an explicit declaration of its public
API.


The problem with __all__
========================

``__all__`` has two problems.

First, it separates the declaration of a name's public export semantics from
the implementation of that name.  Usually the ``__all__`` is put at the top of
the module, although this isn't required, and in some cases it's `actively
prohibited`_.  So when you're looking at the definition of a function or class
in a module, you have to search for the ``__all__`` definition to know whether
the function or class is intended for public consumption.

This leads to the second problem, which is that it's too easy for the
``__all__`` to get `out of sync`_ with the module's contents.  Often a
function or class is renamed, removed, or added without the ``__all__`` being
updated.  Then it's difficult to know what the module author's intent was, and
it can lead to an exception when a string appearing in ``__all__`` doesn't
match an existing name in the module.  Some tools like Sphinx_ will complain
when names appear in ``__all__`` don't appear in the module.  All of this
points to the root problem; it should be easy to keep ``__all__`` in sync!


@public
=======

This package provides a way to declare a name's public visibility right at the point of its
declaration, and to infer the name to export from that definition.  In this way, a module's author
never explicitly sets the ``__all__`` so there's no way for it to get out of sync.

This package, and Python `issue 26632`_, propose just such a solution, in the form of a ``public()``
function that can be used as either a decorator, or a callable.

.. code-block:: pycon

    >>> from public import public

You'll usually use this as a decorator, for example:

.. code-block:: pycon

    >>> @public
    ... def foo():
    ...    pass

or:

.. code-block:: pycon

    >>> @public
    ... class Bar:
    ...     pass

The ``__all__`` after both of those code snippets has both names in it:

.. code-block:: pycon

    >>> print(__all__)
    ['foo', 'Bar']

Note that you do not need to initialize ``__all__`` in the module, since
``public()`` will do it for you.  Of course, if your module *already* has an
``__all__``, it will append any new names to the existing list.


Function call form
==================

The requirements to use the ``@public`` decorator are simple: the decorated thing must have a
``__name__`` attribute.  Since you'll overwhelmingly use it to decorate functions and classes, this
will almost always be the case.  If the object has a ``__module__`` attribute, that string is used
to look up the module object in ``sys.modules``, otherwise the module is extracted from the globals
where the decorator is called.

There's one other common use case that isn't covered by the ``@public``
decorator.  Sometimes you want to declare simple constants or instances as
publicly available.  You can't use the ``@public`` decorator for two reasons:
constants don't have a ``__name__`` and Python's syntax doesn't allow you to
decorate such constructs.

To solve this use case, ``public()`` is also a callable function accepting keyword arguments.  An
example makes this obvious.

.. invisible-code-block: pycon

    >>> reset()

.. code-block:: pycon

    >>> public(SEVEN=7)
    7
    >>> public(a_bar=Bar())
    <...Bar object ...>

The module's ``__all__`` now contains both of the keys:

.. code-block:: pycon

    >>> print(__all__)
    ['SEVEN', 'a_bar']

and as should be obvious, the module contains name bindings for these constants:

.. code-block:: pycon

    >>> print(SEVEN)
    7
    >>> print(a_bar)
    <....Bar object at ...>

Multiple keyword arguments are allowed:

.. code-block:: pycon

    >>> public(ONE=1, TWO=2)
    (1, 2)
    >>> print(__all__)
    ['SEVEN', 'a_bar', 'ONE', 'TWO']

    >>> print(ONE)
    1
    >>> print(TWO)
    2

You'll notice that the functional form of ``public()`` returns the values in its keyword arguments
in order.  This is to help with a use case where some linters complain because they can't see that
``public()`` binds the names in the global namespace.  In the above example they might report
erroneously that ``ONE`` and ``TWO`` aren't defined.  To work around this, when ``public()`` is used
in its functional form, it will return the values in the order they are seen [#]_ and you can simply
assign them to explicit local variable names.

.. code-block:: pycon

    >>> a, b, c = public(a=3, b=2, c=1)
    >>> print(__all__)
    ['SEVEN', 'a_bar', 'ONE', 'TWO', 'a', 'b', 'c']
    >>> print(a, b, c)
    3 2 1

It also works if you bind only a single value.

.. code-block:: pycon

    >>> d = public(d=9)
    >>> print(__all__)
    ['SEVEN', 'a_bar', 'ONE', 'TWO', 'a', 'b', 'c', 'd']
    >>> print(d)
    9


@private
========

You might also want to be explicit about your private, i.e. non-public, names.  This library
provides an ``@private`` decorator for this purpose.  While it mostly serves for documentation
purposes, this decorator also ensures that the decorated object's name does *not* appear in the
``__all__``.

.. invisible-code-block: pycon

    >>> reset()

.. code-block:: pycon

    >>> from public import private

    >>> @public
    ... def foo(): pass

    >>> print(__all__)
    ['foo']

    >>> @private
    ... def foo(): pass

    >>> print(__all__)
    []

You can see here that ``foo`` has been removed from the ``__all__``.  It's
okay if the name doesn't appear in ``__all__`` at all:

.. invisible-code-block: pycon

    >>> reset()

.. code-block:: pycon

    >>> @private
    ... class Baz:
    ...     pass

    >>> print(__all__)
    []

In this case, ``Baz`` never appears in ``__all__``.  Like with ``@public``,
the ``@private`` decorator will initialize ``__all__`` if needed, but if it
exists in the module, it must be a list.  There is no functional API for
``@private``.


Inferring __all__
=================

If you don't like using the decorators, you can instead infer and populate the contents of ``__all__`` by
calling the ``populate_all()`` function at the bottom of your module.  This uses heuristics to pick out some
names from the module, adding them to ``__all__`` if they meet the following criteria:

* The name does not start with an underscore.
* The name is not bound to a module object.  This prevents imported modules from being added.
* The object the name is bound to does not appear to be defined in some other module.  This prevents most
  from-imports from being added, but note that this can be fooled if you import simple types (such as an
  ``int`` or a ``str``) from another module (e.g. ``from sys import abiflags``), because simple types don't
  have a ``__module__`` attribute.

For example, if your Python module looks like this:

.. literalinclude:: popall_example.py
    :language: python
    :linenos:

when you import this module, the ``__all__`` will be populated with the names matching the above heuristics.

.. invisible-code-block: pycon

    >>> example = import_example('popall_example.py')

.. code-block:: pycon

    >>> example.__all__
    ['foo', 'Foo', 'fooint']

In this case, you can see that the module has an ``__all__`` set to ``['foo', 'Foo', 'fooint']`` but note that
neither ``_foobool`` nor ``populate_all`` are added.

If the inferencing misses some names you want to publicly export, you can always add them explicitly by using
``@public`` or appending to ``__all__``.

.. note::

    This function only adds new names to ``__all__``.


Caveats
=======

There are some important usage restrictions you should be aware of:

* Only use ``@public`` and ``@private`` on top-level object.  Specifically,
  don't try to use either decorator on a class method name.  While the
  declaration won't fail, you will get an exception when you attempt to ``from
  <module> import *`` because the name pulled from ``__all__`` won't be in the
  module's globals.
* If you explicitly set ``__all__`` in your module, be sure to set it to a
  list.  Some style guides require ``__all__`` to be a tuple, but since that's
  immutable, as soon as ``@public`` tries to append to it, you will get an
  exception.  Best practice is to not set ``__all__`` explicitly; let
  ``@public`` and ``@private`` do it!
* If you still want ``__all__`` to be immutable, put the following at the
  bottom of your module::

    __all__ = tuple(__all__)


.. [#] This is ordering is guaranteed by `PEP 468 <https://peps.python.org/pep-0468/>`_.


.. _`issue 26632`: http://bugs.python.org/issue26632
.. _builtins: https://docs.python.org/3/library/builtins.html
.. _`directly controls`: https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
.. _`actively prohibited`: http://pep8.readthedocs.io/en/latest/intro.html?highlight=e402#error-codes
.. _`out of sync`: http://bugs.python.org/issue23883
.. _implementations: http://bugs.python.org/issue22247#msg225637
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
