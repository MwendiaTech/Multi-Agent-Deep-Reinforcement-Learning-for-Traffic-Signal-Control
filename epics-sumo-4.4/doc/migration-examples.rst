Migrating supports and applications
===================================

Here are some examples on how to start using sumo when you already have a large
installation of support modules and applications.

The examples here are shown for our development environment here at the HZB but
could be applied at other sites with some changes.

.. _migration-examples-supports:

Migrating the support directory
-------------------------------

.. note::
   It is assumed that the supports in your support directory are located at
   paths with the schema "[BASEDIR]/[MODULEPATH]/[VERSION]". If you
   don't have this schema, the output ouf sumo-scan will require to be edited
   manually. See also 
   :ref:`sumo-scan Phase II, Grouping <reference-sumo-scan-Phase-II-Grouping>`.

This chapter shows how to *migrate* your existing installation of support
modules to sumo. sumo-scan can help you to create a first version of the
:ref:`dependency database <reference-sumo-db-The-dependency-database>`.
Alternatively you can create the dependency database from scratch.

Set up the sumo directory
+++++++++++++++++++++++++

We create a directory which will hold all sumo files and remember it in an
environment variable::

  mkdir sumo && cd sumo
  SUMODIR=`pwd`
  mkdir scan database build

Scan the support directory with sumo-scan
+++++++++++++++++++++++++++++++++++++++++

sumo-scan has many command line options that help you create a first version of
a :ref:`dependency database <reference-sumo-db-The-dependency-database>` that
is almost correct. You may however, have to edit the created text files in
order to remove wrong dependencies or give repository specifications a
canonical form.

For details see :ref:`sumo scan options <reference-sumo-scan-Options>`.

We assume that our collection of support modules is in directory <supportdir>
and that our various versions of `EPICS <http://www.aps.anl.gov/epics>`_ base
are in directory <epics-basedir>.  We invoke sumo-scan with this command::

  sumo-scan -d <supportdir> -d <epics-basedir> > $SUMODIR/scan/SCAN

We now have the results of the scan in a single file. This file is in 
`JSON <http://www.json.org>`_ format, you may load this file in your
text editor and check or modify it.

Apply changes to the scan file (optional)
+++++++++++++++++++++++++++++++++++++++++

At key "groups" in the scan file you see a structure that contains all
modules and versions that were found. For details see 
:ref:`sumo-scan Phase II, Grouping <reference-sumo-scan-Phase-II-Grouping>`.

Each module or version you remove here, will not be part of the dependency
database that is created later.

At key "repos" in the scan file you see the data structure that contains all
software repositories and source directories that were found. For details see
:ref:`sumo-scan Phase III, repository scan <reference-sumo-scan-Phase-III-repository-scan>`.

You may edit repository URLs here in order to have a canonical form.

Here at HZB we had to change repository paths like::

  /srv/csr/repositories/controls/darcs/epics/base/3-14-12-2

to a more generic form that works on other build hosts, too::

  rcsadm@repo.acc.bessy.de:/opt/repositories/controls/darcs/epics/base/3-14-12-2

Note that option "-U" of sumo-scan changes repository URLs on the fly. You
may want to re-run sumo-scan with this option instead of changing many
repository URLs in the scan file manually. For more information on this topic see
:ref:`sumo-scan options <reference-sumo-scan-Options>`.

Create the dependency database
++++++++++++++++++++++++++++++

Like sumo-scan, sumo also has command line options that may help you a more
correct version of the 
:ref:`dependency database <reference-sumo-db-The-dependency-database>`. 

For details see :ref:`sumo options <reference-sumo-Options>`.

We assume that ``$SUMODIR`` is defined and that the subdirectory ``database``
exists as described further above.  You convert the scan file to a dependency
database with this command::

  sumo --dbdir $SUMODIR/database --scandb $SUMODIR/database/SCAN.DB db convert $SUMODIR/scan/SCAN

Create the sumo configuration file
++++++++++++++++++++++++++++++++++

Finally you have to create a sumo configuration file that contains the paths of
the dependency database and the build directory.

We create the file with this command::

  sumo config make sumo.config --#opt-preload configure/MODULES.HOST --#opt-preload configure/MODULES --builddir $SUMODIR/build --dbdir $SUMODIR/database --scandb $SUMODIR/database/SCAN.DB 

For a system-wide configuration you may want to place this file in sumo's
library path. You get the name of this directory with this command::

  python -c 'import sumolib;from os.path import *; print(dirname(sumolib.__file__))'

You find more information on configuration files at 
:doc:`configuration-files`.

Migrating a single support
--------------------------

We first have to scan the existing RELEASE file with sumo-scan. We have to know
the paths of the used `EPICS <http://www.aps.anl.gov/epics>`_ base and the
directory with used support modules. These are given as option "-g" to the
program. The output of sumo-scan is directed to sumo which prints 
`JSON <http://www.json.org>`_ data compatible with the 
:ref:`dependency database <reference-sumo-db-The-dependency-database>` to the
console::

  sumo-scan -d . -g <supportdir> -g <epics-basedir> --ignore-changes 'configure/RELEASE' | sumo db modconvert - -C <supportname>

Option ``--ignore-changes 'configure/RELEASE'`` is needed if file
configure/RELEASE has uncomitted changes. If sumo-scan finds any uncomitted
changes it sets the :ref:`source data <reference-sumo-source-data>` to type
'path' which usually is not what you want.

Note that you may omit <supportname> but in this case the `JSON
<http://www.json.org>`_ data contains not just your support module but also all
dependent modules. 

You may direct the output to a file and use 
:ref:`sumo edit <reference-sumo-db-edit>` to add this to the 
:ref:`dependency database <reference-sumo-db-The-dependency-database>`.

.. _migration-examples-application:

Migrating an application
------------------------

Create configuration file and module list
+++++++++++++++++++++++++++++++++++++++++

We first have to scan the existing RELEASE file with sumo-scan. We have to know
the paths of our old `EPICS <http://www.aps.anl.gov/epics>`_ base and the old
support directory, these are given as option "-g" to the program. The output of
sumo-scan is directed to sumo which creates a `JSON <http://www.json.org>`_
file "configure/MODULES" with :term:`modulespecs` and :term:`aliases`::

  sumo-scan -d . -g <supportdir> -g <epics-basedir> | sumo db appconvert - -C > configure/MODULES

Our global sumo configuration file (see further above) defines everything sumo
needs. You may want to define option "buildtag-stem" that is used to name
builds created for this application in an extra configuration file with this
command::

  sumo -C --buildtag-stem <APPNAME> config make sumo.config

Build all support modules the application requires
++++++++++++++++++++++++++++++++++++++++++++++++++

Now we try to use modules from our support directory::

  sumo build try

If the program replies::

  Not all dependencies were included in module specifications

you first have to add missing modules to file ``configure/MODULES``. The
command::

  sumo build try --detail 1 

may help you with that.

When our module list is complete we can now use a matching build with::

  sumo build new

If program prints this message::

  no build found that matches modulespecs

then there is no matching build and we first have to create one. This is done
with command::

  sumo build new

The list of :term:`modules` is taken from file ``configure/MODULES``. The
program creates a collection of all :term:`modules` needed, checks out the
sources of all :term:`modules`, creates a new entry in the :term:`BUILDS.DB`
database, creates a makefile and calls make.

Use the support modules in the application
++++++++++++++++++++++++++++++++++++++++++

After all needed support modules were built (see above) we use the build with::

  sumo build use

The sumo command "build use" looks in the :term:`support directory` for 
a :term:`build` matching our :term:`module` requirements and creates
a RELEASE that uses that :term:`build`. The program responds for example::

  using build AUTO-001
  
Now that the RELEASE file is created we can go ahead and build our application
by calling "make"::

  make

