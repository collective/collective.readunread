.. image:: https://travis-ci.org/collective/collective.readunread.svg?branch=master
   :target: https://travis-ci.org/collective/collective.readunread

.. image:: https://coveralls.io/repos/collective/collective.readunread/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.readunread?branch=master

=====================
collective.readunread
=====================

This package provides read/unread status for dexterity Plone objects.

Features
--------

- Choose with a behavior which content type will be concerned (marking with IReadUnreadMarker)
- Propose a viewlet for objects providing IReadUnreadMarker


To do
--------

- Propose an optional zcml to automatically mark as read traversed objects
- Add a registry option with a portal types list to choose if modification event must be notified

Translations
------------

This product has been translated into

- french


Installation
------------

Install collective.readunread by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.readunread


and then running ``bin/buildout``


Development
-----------

- virtualenv2.7 .
- bin/pip install --upgrade pip
- bin/pip install -r requirements
- bin/buildout

Contribute
----------

- Issue Tracker: https://github.com/collective/collective.readunread/issues
- Source Code: https://github.com/collective/collective.readunread
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know on https://github.com/collective/collective.readunread/issues.


License
-------

The project is licensed under the GPLv2.
