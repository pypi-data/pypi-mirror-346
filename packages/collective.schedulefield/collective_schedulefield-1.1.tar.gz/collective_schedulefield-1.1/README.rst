collective.schedulefield
========================

Schedule behaviors for Plone content types.


Features
--------

- schedule or multi-schedule (with dates ranges) behaviors to define schedules
  (morning / afternoon / comment) by day of week
- exceptional closure behavior to define closing days


Installation
------------

Install ``collective.schedulefield`` by adding it to your buildout: ::

    [buildout]

    ...

    eggs =
        collective.schedulefield


and then running ``bin/buildout``


Compatibility
-------------

Versions 1.x are developed for Plone 6.

Versions 0.x are developed for Plone 4 & Plone 5.
Please note that they do not provide the full functionality (no multi-schedules,
no exceptional closures, no RESTAPI serializer).


Contribute
----------

Have an idea? Found a bug? Let us know by `opening a ticket`_.

- Issue Tracker: https://github.com/IMIO/collective.schedulefield/issues
- Source Code: https://github.com/IMIO/collective.schedulefield


License
-------

The project is licensed under the GPLv2.

.. _`opening a ticket`: https://github.com/IMIO/collective.schedulefield/issues
