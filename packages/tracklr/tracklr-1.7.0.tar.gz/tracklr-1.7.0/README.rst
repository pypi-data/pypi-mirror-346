README
======

``Tracklr`` is a command-line toolset for processing `iCalendar` feeds.

| |license| |downloads|
| |status| |format| |wheel|
| |version| |pyversions| |implementation|
| |coverage|

.. |version| image:: https://img.shields.io/pypi/v/tracklr
   :target: https://pypi.org/project/tracklr/
   :alt: PyPI - Version

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/tracklr
   :target: https://pypi.org/project/tracklr/
   :alt: PyPI - Python Versions

.. |implementation| image:: https://img.shields.io/pypi/implementation/tracklr
   :target: https://pypi.org/project/tracklr/
   :alt: PyPI - Implementation

.. |downloads| image:: https://img.shields.io/pypi/dm/tracklr
   :target: https://pypi.org/project/tracklr/
   :alt: PyPI - Downloads

.. |license| image:: https://img.shields.io/pypi/l/tracklr
   :target: https://pypi.org/project/tracklr/
   :alt: PyPI - License

.. |format| image:: https://img.shields.io/pypi/format/tracklr
   :target: https://pypi.org/project/tracklr/
   :alt: PyPI - Format

.. |status| image:: https://img.shields.io/pypi/status/tracklr
   :target: https://pypi.org/project/tracklr/
   :alt: PyPI - Status

.. |wheel| image:: https://img.shields.io/pypi/wheel/tracklr
   :target: https://pypi.org/project/tracklr/
   :alt: PyPI - Wheel

.. |coverage| image:: https://codecov.io/gl/markuz/tracklr/branch/master/graph/badge.svg
   :target: https://codecov.io/gl/markuz/tracklr
   :alt: coverage.io report

Installation
------------

Install ``tracklr`` via ``pip``::

    pip install tracklr


Additionally, you can install a collection of ``productivity`` packages to use in conjuction with Tracklr::

   pip install tracklr[productivity]


Those packages are  ``khal``, ``khard`` and ``vdirsyncer``.


Dependencies
------------

``Tracklr`` requires the following packages installed::

    appdirs
    cliff
    icalendar
    jinja2
    pyfiglet   # Optional
    pyyaml
    requests
    xhtml2pdf


Configuration
-------------

Out of the box ``tracklr`` uses its own configuration stored in ``Tracklr.__config__``.

For PDF reports ``tracklr`` uses by default its own HTML template in ``tracklr.pdf.Pdf.__template__``.

``tracklr`` provides ``init`` command to create ``tracklr.yml`` and ``pdf.html`` files either in
user config directory eg. ``~/.config/tracklr/`` or current working directory (default).

See ``tracklr init --help`` for more details.


Usage
-----

::

    # setup local config
    tracklr init config

    # setup global pdf.html uses for all tracklr instances
    tracklr init template --user-config-dir

    # display info about the current instance
    tracklr info

    # show only 2019-02 events
    tracklr ls -d 2019-02

    # show only 2019 @tracklr events
    tracklr ls -d 2019 -i @tracklr

    # generate 2019 @tracklr PDF report 
    tracklr pdf -d 2019 -i @tracklr

    # show all hours matching tag #tags
    tracklr group -i "#tags"


Documentation
-------------

Project documentation for the current version is available at https://tracklr.com/

Source of the documentaton is available in the `Tracklr` repository
https://gitlab.com/markuz/tracklr/tree/master/docs/source


Development
-----------

Pull requests welcomed.

``Tracklr`` git repository is available at https://gitlab.com/markuz/tracklr

For more information, see https://tracklr.com/development.html


License
-------

`BSD 3-clause Clear License <https://gitlab.com/markuz/tracklr/blob/master/LICENSE>`_
