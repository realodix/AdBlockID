python-abp AdBlockID
==========

Adjusted for AdBlockID.

This repository contains a library for working with Adblock Plus filter lists,
a script for rendering diffs between filter lists, and the script that is used
for building Adblock Plus filter lists from the form in which they are authored
into the format suitable for consumption by the adblocking software (aka
rendering).

.. contents::


Installation
------------

Prerequisites:

* Linux, Mac OS X or Windows (any modern Unix should work too)
* Python (2.7 or 3.5+)
* pip
* GIT

To install::

    $ pip install -e python-abp_AdBlockID


Rendering of filter lists
-------------------------

The filter lists are originally authored in relatively smaller parts focused
on particular types of filters, related to a specific topic or relevant for a
particular geographical area.
We call these parts *filter list fragments* (or just *fragments*) to
distinguish them from full filter lists that are consumed by the adblocking
software such as Adblock Plus.

Rendering is a process that combines filter list fragments into a filter list.
It starts with one fragment that can include other ones and so forth.
The produced filter list is marked with a `version and a timestamp <https://adblockplus.org/filters#special-comments>`_.

Python-abp contains a script that can do this called ``flrender``::

    $ flrender fragment.txt filterlist.txt


This will take the top level fragment in ``fragment.txt``, render it and save it
into ``filterlist.txt``.

The ``flrender`` script can also be used by only specifying ``fragment.txt``::

    $ flrender fragment.txt


in which case the rendering result will be sent to ``stdout``. Moreover, when
it's run with no positional arguments::

    $ flrender


it will read from ``stdin`` and send the results to ``stdout``.

Fragments might reference other fragments that should be included into them.
The references come in two forms: http(s) includes and local includes::

    %include http://www.server.org/dir/list.txt%
    %include easylist:easylist/easylist_general_block.txt%


The http include contains a URL that will be fetched and inserted at the point
of reference.
The local include contains a path inside the easylist repository.
``flrender`` needs to be able to find a copy of the repository on the local
filesystem. We use ``-i`` option to point it to to the right directory::

    $ flrender -i easylist=/home/abc/easylist input.txt output.txt


Now the local include referenced above will be resolved to:
``/home/abc/easylist/easylist/easylist_general_block.txt``
and the fragment will be loaded from this file.

Directories that contain filter list fragments that are used during rendering
are called sources.
They are normally working copies of the repositories that contain filter list
fragments.
Each source is identified by a name: that's the part that comes before ":" in
the include instruction and it should be the same as what comes before "=" in
the ``-i`` option.

Commonly used sources have generally accepted names. For example the main
EasyList repository is referred to as ``easylist``.
If you don't know all the source names that are needed to render some list,
just run ``flrender`` and it will report what it's missing::

    $ flrender easylist.txt output/easylist.txt
    Unknown source: 'easylist' when including 'easylist:easylist/easylist_gener
    al_block.txt' from 'easylist.txt'


You can clone the necessary repositories to a local directory and add ``-i``
options accordingly.


Generating diffs
----------------

See `python-abp: Generating diffs <https://github.com/adblockplus/python-abp#generating-diffs>`_.


Library API
-----------

See `python-abp: Library API <https://github.com/realodix/AdBlockFilterTools/tree/main/python-abp#id5>`_.


Development
-----------

When adding new functionality, add tests for it (preferably first). If some
code will never be reached on a certain version of Python, it may be exempted
from coverage tests by adding a comment, e.g. ``# pragma: no py2 cover``.

All public functions, classes and methods should have docstrings compliant with
`NumPy/SciPy documentation guide <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`_.
One exception is the constructors of classes that the user is not expected to
instantiate (such as exceptions).


Using the library with R
------------------------

See `python-abp: Using the library with R <https://github.com/adblockplus/python-abp#using-the-library-with-r>`_.


Reference
---------
- https://github.com/adblockplus/python-abp


License
---------
This file is part of `Adblock Plus <https://adblockplus.org/>`_.

Copyright (C) 2006-present eyeo GmbH. Licensed under the [GNU General Public License](http://www.gnu.org/licenses/).
