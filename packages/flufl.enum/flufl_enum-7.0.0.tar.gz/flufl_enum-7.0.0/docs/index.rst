=========================================
flufl.enum - A Python enumeration package
=========================================

This package is called ``flufl.enum``, a Python enumeration package.

The goals of ``flufl.enum`` are to produce simple, specific, concise semantics
in an easy to read and write syntax.  ``flufl.enum`` has just enough of the
features needed to make enumerations useful, but without a lot of extra
baggage to weigh them down.  This work grew out of the `Mailman 3.0
<https://docs.mailman3.org/en/latest/>`_ project.  This package was previously
called ``munepy``.

Since enums were added to Python in 3.4, why use this package instead of the
Python standard library `enum <https://docs.python.org/3/library/enum.html>`_
package?  ``flufl.enum`` is intentionally simpler, and thus potentially faster
and easier to maintain.


Requirements
============

``flufl.enum`` requires Python 3.9 or newer.


Documentation
=============

A `simple guide`_ to using the library is available within this package, along
with a detailed `API reference`_.


Project details
===============

 * Project home: https://gitlab.com/warsaw/flufl.enum
 * Report bugs at: https://gitlab.com/warsaw/flufl.enum/issues
 * Code hosting: https://gitlab.com/warsaw/flufl.enum.git
 * Documentation: http://fluflenum.readthedocs.org/

You can install it with ``pip``::

    % pip install flufl.enum

You can grab the latest development copy of the code using git.  The
repository is hosted on GitLab.  If you have git installed, you can grab your
own branch of the code like this::

    $ git clone https://gitlab.com/warsaw/flufl.enum.git

You may contact the author via barry@python.org.


Copyright
=========

Copyright (C) 2004-2025 Barry A. Warsaw

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Table of Contents
=================

* :ref:`genindex`

.. toctree::
    :glob:

    using
    apiref
    NEWS

.. _`simple guide`: using.html
.. _`API reference`: apiref.html
