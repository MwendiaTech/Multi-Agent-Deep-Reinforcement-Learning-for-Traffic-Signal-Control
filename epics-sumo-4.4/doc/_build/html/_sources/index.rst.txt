.. Support Module Tools documentation master file, created by
   sphinx-quickstart on Thu Dec 19 13:05:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: logo_hzb_big.png
   :align: right
   :target: http://www.helmholtz-berlin.de

====================================
Welcome to EPICS-sumo documentation!
====================================

.. toctree::
   :maxdepth: 5
   :hidden:

   sumo-install
   introduction
   modulespecs
   configuration-files
   reference-sumo-scan
   reference-sumo
   app-usage
   dev-usage
   example-sumo-build-try
   demo
   migration-examples
   contribute
   glossary
   license

A SUpport MOdule manager for EPICS
----------------------------------

The support module manager sumo is a program to build consistent sets of 
`EPICS <http://www.aps.anl.gov/epics>`_ support modules and use them in 
`EPICS <http://www.aps.anl.gov/epics>`_ applications.

Some of the features are:

- All module dependencies are held in a `JSON <http://www.json.org>`_
  dependency database.

- The dependency database can be managed automatically with a version control
  system in order to keep it in sync on a number of build hosts.

- In order to migrate your existing support module installation a scanner
  program creates a dependency database from existing support directories.

- The program builds consistent sets of 
  `EPICS <http://www.aps.anl.gov/epics>`_ support modules.

- The program fetches module source code from various sources, directories, tar
  files or version control systems (currently git, mercurial, darcs, subversion
  and cvs).
  
- If a set of support modules is to be used in an application a RELEASE is
  generated with all the relevant paths.

See :doc:`introduction` for more information.

See :doc:`demo` for a quickstart demo on your host (only for Linux/Unix
Systems).

:Author: Goetz Pfeiffer <Goetz.Pfeiffer@helmholtz-berlin.de>

Documentation
-------------

Reference documents
+++++++++++++++++++

- :doc:`reference-sumo`
- :doc:`reference-sumo-scan`
- :doc:`configuration-files`
- :doc:`modulespecs`

Use cases
+++++++++

- :doc:`app-usage`
- :doc:`example-sumo-build-try`
- :doc:`dev-usage`
- :doc:`migration-examples`
- :doc:`demo`

License and copyright
---------------------

Copyright (c) 2022 by `Helmholtz-Zentrum Berlin <https://www.helmholtz-berlin.de>`_.

This software of this project can be used under GPL v.3, see :doc:`license`.

Download
--------

Sumo is available as a debian or rpm package, as tar.gz or zip here:

* `sumo downloads at Sourceforge <https://sourceforge.net/projects/epics-sumo/files/?source=navbar>`_

Install
-------

You install sumo either as a debian or rpm package with your package manager,
from source or with pip.

For details on how to install sumo see :doc:`sumo-install`.

Sumo at sourceforge
-------------------

You find the sourceforge summary page for sumo at
`epics-sumo at Sourceforge <https://sourceforge.net/projects/epics-sumo>`_.

The source
----------

You can browse the mercurial repository here:

`repository at Sourceforge <http://hg.code.sf.net/p/epics-sumo/mercurial/epics-sumo>`_.

or clone it with this command:

Sourceforge::

  hg clone http://hg.code.sf.net/p/epics-sumo/mercurial epics-sumo

How to contribute
-----------------

If you have bug fixes or changes and extensions of sumo you are encouraged to
send my your changes. Here is a short description:

- :doc:`contribute`

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

