sumo demo
=========

Here we demonstrate how sumo-scan is used to migrate existing EPICS supports
and an EPICS application.

This is a complete example. You need a Linux/Unix system and an internet
connection, git, all build tools for compiling 
`EPICS <http://www.aps.anl.gov/epics>`_ base and Python.

Build an EPICS example
----------------------

Prepare the directory
+++++++++++++++++++++

We create an example with EPICS base, two EPICS supports and an EPICS
application. Enter these commands::

  cd $HOME
  mkdir sumo-demo
  cd sumo-demo

Now you need to download these two scripts and put them in the
directory you just created:

- :download:`downloads/demo/build-demo.sh`
- :download:`downloads/demo/install-sumo.sh`

You have to make the downloaded scripts executable with this command::

  chmod u+x *.sh

Set up the support and application directories
++++++++++++++++++++++++++++++++++++++++++++++

First get and compile EPICS base, create and compile two EPICS supports and an
EPICS application with this command::

  ./build-demo.sh

You can start the soft-IOC of the application you just built with this
command::

  (cd apps/appA/iocBoot/iocA && ./st.cmd)

The IOC has two records, "low" and "high" that show some random numbers.

You can see values of these records with these commands::

  dbpr("low")
  dbpr("high")

After each `dbpr` the `VAL` field changes.

You can exit the soft-IOC with the key <control-d>.

Set up sumo
-----------

Run::

  ./install-sumo.sh

This creates a virtual python environment, downloads and installs sumo and
creates a sumo configuration file.

Make sumo accessible in your shell with these commands::

  source ./venv/bin/activate
  eval $(sumo help completion-line)

Further reading:

- :doc:`sumo-install`
- :doc:`configuration-files`
- :ref:`Command completion <reference-sumo-command-completion>`

Migrate the example for usage with sumo
---------------------------------------

Scan the support directory and create a dependency database
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Use sumo-scan to scan the supports::

  sumo-scan -d support > sumo/scan/SCAN

Create the dependency database::

  sumo db convert sumo/scan/SCAN

Further reading:

- :ref:`migration-examples-supports`
- :ref:`reference-sumo-db-The-dependency-database`
- :doc:`reference-sumo-scan`

Create a copy of the sources of the original application
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Since we dont't want to change the directory of the original application, we
create a copy and run "make distclean" to remove all files created by the
previous compilation::

  cp -a apps/appA apps/appA-sumo
  make -C apps/appA-sumo distclean -sj

Scan the application to create a MODULES file
+++++++++++++++++++++++++++++++++++++++++++++

Enter this command::

  sumo-scan -d apps/appA -g support | sumo db appconvert - -C > apps/appA-sumo/configure/MODULES

Further reading:

- :ref:`migration-examples-application`
- :ref:`Example MODULES file <app-usage-modules>`

Rebuild the application, now with sumo
++++++++++++++++++++++++++++++++++++++

Change the current working directory for the new application::

  cd apps/appA-sumo

Create a sumo build needed by the application::

  sumo build new --makeflags "-sj" --progress

Now use the build in the application::

  sumo build use

And build the application::

  make -sj

Start the application with::

  (cd iocBoot/iocA && ./st.cmd)

As before, the IOC has two records, "low" and "high" that show some random
numbers.

You can see values of these records with these commands::

  dbpr("low")
  dbpr("high")

After each `dbpr` the `VAL` field changes.

You can exit the soft-IOC with the key <control-d>.

Further reading:

- :ref:`sumo build new <reference-sumo-new>`
- :ref:`sumo build use <reference-sumo-use>`

What to do now
--------------

In this demo you have installed sumo, created a dependency database and a sumo
build. 

Here are more commands you can play with:

- :ref:`sumo db list <reference-sumo-db-list>`: Show modules in the database
- :ref:`sumo db list BASE <reference-sumo-db-list>`: Show versions of EPICS base in the database
- :ref:`sumo db show BASE:TAGLESS-7.0 <reference-sumo-db-show>`: Show details for EPICS base
- :ref:`sumo build list <reference-sumo-build-list>`: Show all builds
- :ref:`sumo build show AUTO-001 <reference-sumo-build-show>`: Show details for build "AUTO-001"
- ``cat configure/MODULES``: Show created MODULES file
- ``cat configure/RELEASE``: Show created RELEASE file
- :ref:`sumo config list <reference-sumo-config-list>`: Show which configuration files are loaded
- :ref:`sumo config show <reference-sumo-config-show>`: Show current configuration
- :ref:`sumo config show --disable-loading <reference-sumo-disable-loading>`: Show current configuration without executing #preload
- :ref:`sumo help <reference-sumo-help>`: Show main page of the program's help

