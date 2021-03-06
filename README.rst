lizard-fewsunblobbed
==========================================

Introduction

Usage, etc.

More details in src/lizard_fewsunblobbed/USAGE.txt .


Development installation
------------------------

The first time, you'll have to run the "bootstrap" script to set up setuptools
and buildout::

    $> python bootstrap.py

And then run buildout to set everything up::

    $> bin/buildout

(On windows it is called ``bin\buildout.exe``).

You'll have to re-run buildout when you or someone else made a change in
``setup.py`` or ``buildout.cfg``.

The current package is installed as a "development package", so
changes in .py files are automatically available (just like with ``python
setup.py develop``).

If you want to use trunk checkouts of other packages (instead of released
versions), add them as an "svn external" in the ``local_checkouts/`` directory
and add them to the ``develop =`` list in buildout.cfg.

Tests can always be run with ``bin/test`` or ``bin\test.exe``.


Settings
--------

In your settings.py, it is possible to define some filters to be
excluded from the filterlist.

FEWS_UNBLOBBED_EXCLUDE_FILTERS = ['ZZL_Meteo', 'ZZL_ZUIV_RUW', ]


Installation
------------

Run the Deltares postgis script to create the tables Filter, Location,
Parameter, Timeserie, Timeseriedata.

After creating the standard tables, install the IconStyle table by
running the command::

    $> bin/django syncdb --database=fews-unblobbed

