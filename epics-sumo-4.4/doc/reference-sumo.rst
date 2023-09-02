====
sumo
====

What the script does
--------------------

The script has two major purposes:

- Manage the :term:`dependency database` :term:`DEPS.DB`. 
  It is used to create this file from the output of 
  :doc:`sumo-scan <reference-sumo-scan>` and to query and 
  change that file.
- Create and manage :term:`builds`. It also keeps note of 
  all builds in the build database :term:`BUILDS.DB`.

The script takes one or mode commands and has a number of options. Single
character options always start with a single dash "-", long options start with
a double dash "--", commands are simple words on the command line.

How it works
------------

Information on all known :term:`modules` and module :term:`versions` is kept in
the :term:`dependency database`. This file also contains a :term:`source`
specification for each module that may be a directory, tar file or url or a
repository specification.

A complete and consistent set of modules that is compiled is called a
:term:`build`.  All :term:`builds` are kept in a single directory, the
:term:`support directory`. Information on :term:`builds` is kept in a 
`JSON <http://www.json.org>`_ file, the build database :term:`BUILDS.DB`.

.. _reference-sumo-db-The-dependency-database:

The dependency database
+++++++++++++++++++++++

The dependency database :term:`DEPS.DB` file is a `JSON <http://www.json.org>`_ file
that contains information on versions of support modules and their
dependencies. Here is an example how this file looks like::

  {
    "BSPDEP_TIMER": {
        "R6-2": {
            "aliases": {
                "BASE": "EPICS_BASE"
            },
            "dependencies": [
                "BASE"
            ],
            "extra": [
                "# BSPDEP_TIMER: board support specific timer support",
                "# This is version R6-2"
            ],
            "make-recipes": {
                "all": [
                    "cd $DIR && ./configure --prefix=.",
                    "$(MAKE) -C $DIR"
                ],
                "clean": [
                    "$(MAKE) -C $DIR realclean"
                ]
            },
            "source": {
                "darcs": {
                    "tag": "R6-2",
                    "url": "rcsadm@aragon.acc.bessy.de:/opt/repositories/controls/darcs/epics/support/bspDep/timer"
                }
            }
        }
    },
    "MCAN": {
        "R2-4-0": {
            "aliases": {
                "BASE": "EPICS_BASE",
                "MISC_DBC": "DBC",
                "MISC_DEBUGMSG": "DEBUGMSG",
                "SOFT_DEVHWCLIENT": "DEVHWCLIENT"
            },
            "dependencies": [
                "ALARM",
                "BASE",
                "MISC_DBC",
                "MISC_DEBUGMSG",
                "SOFT_DEVHWCLIENT"
            ],
            "source": {
                "darcs": {
                    "tag": "R2-4-0",
                    "url": "rcsadm@aragon.acc.bessy.de:/opt/Epics/R3.14.12/support/mcan/2-4-0"
                }
            }
        },
        "R2-4-1": {
            "aliases": {
                "BASE": "EPICS_BASE",
                "MISC_DBC": "DBC",
                "MISC_DEBUGMSG": "DEBUGMSG",
                "SOFT_DEVHWCLIENT": "DEVHWCLIENT"
            },
            "dependencies": [
                "ALARM",
                "BASE",
                "MISC_DBC",
                "MISC_DEBUGMSG",
                "SOFT_DEVHWCLIENT"
            ],
            "source": {
                "darcs": {
                    "tag": "R2-4-1",
                    "url": "rcsadm@aragon.acc.bessy.de:/opt/Epics/R3.14.12/support/mcan/2-4-0"
                }
            }
        },
    },
  }

The basic datastructure is this::

  {
      MODULENAME : {
          VERSIONNAME : {
              <versiondata>
          },
          VERSIONNAME : {
              <versiondata>
          },
          ...
      }
  }

The *versiondata* map has this form::

  {
      "aliases": {
          <aliasdata>
      },
      "dependencies": {
          <dependency data>
      },
      "extra": {
          <extra data>
      },
      "make-recipes": {
          <make-recipes data>
      },
      "releasefile": <releasefilename>,
      "source": {
          <source data>
      },
      "weight": <weight>
  }

aliases
:::::::

When the support module is to be compiled "sumo build" creates a RELEASE file
from the known dependencies of the module. The RELEASE file contains variable
definitions, one for each dependency whose name is the module name and whose
value is the path of the compiled module. If a module needs a variable name
that is different from the module name, an alias must be defined. For each
dependency that is part of the alias map, the *ALIASNAME* of the alias map is
taken. The *aliasdata* map has this form::

  {
      MODULENAME: MODULEALIAS,
      MODULENAME: MODULEALIAS,
      ...
  }

dependencies
::::::::::::

This is a list of :term:`modules` this :term:`module` depends on. Note that we
do not store the :term:`versions` of the :term:`modules` here. Information on
which :term:`version` is compatible with another :term:`version` can be found
in the build database :term:`BUILDS.DB`.  This is the form of the
*dependencies* list::

  [
      MODULENAME,
      MODULENAME,
      ...
  ]

.. _reference-sumo-extra:

extra
:::::

This *optional* field is used to specify extra lines that are added to the
generated RELEASE file of the module. 

This is a list of strings, one for each line to add.

.. _reference-sumo-make-recipes:

make-recipes
::::::::::::

This *optional* field is used to specify alternative make recipes for the
makefile that is generated for all modules of a build. 

For each of the make targets "all", "clean", "config" and "distclean" a list of
lines can be defined that is put in the generated makefile. In the make-recipes
map, each of the map keys "all", "clean", "config" and "distclean" is optional.
For convenience, the string "$DIR" is replaced with the special make variable
``$(@D)`` in every line. This is the directory of the checked out module (see
also documentation of the "make" command). Note that *you do not have to
prepend each line with a <TAB> character*, sumo already does this.

Note that for the "all" target your last recipe line is usually 
``$(MAKE) -C $DIR``.

If you have an empty object (or dictionary in python speak) here, this means
that the module has no makefile at all. It is just checked out and possibly
configured (see also :ref:`"commands"<reference-sumo-db-commands>`).

You have an example of a `make-recipes` structure at the top of the chapter
:ref:`The dependency database <reference-sumo-db-The-dependency-database>` .

You can define make-recipes on the command line with 
:ref:`sumo db make-recipes<reference-sumo-db-make-recipes>` or directly in the 
dependency database with :ref:`sumo db edit<reference-sumo-db-edit>`.

Special variables and characters:

- ``$DIR``: (sumo) The directory of the MODULE.
- ``\"``: (bash) A literal double quote character.
- ``$(VAR)``: (make) Insert value of make or shell variable ``VAR``.
- ``$$``: (make) A dollar character passed to the shell.
- ``\\$$``: (make, bash) A literal dollar character passed to the shell.
- ``\\``: (json, bash) At the end of the json string this means line continuation for bash.

This is the form of the *make-recipes* map::
 
  "all": [
      STRING,
      STRING,
      ...
  ],
  "clean": [
      STRING,
      STRING,
      ...
  ],
  "config": [
      STRING,
      STRING,
      ...
  ],
  "distclean": [
      STRING,
      STRING,
      ...
  ]

releasefile
:::::::::::

This *optional* field is used to specify an alternative name for the generated
RELEASE file. The default name, if releasefile is not given, is
`configure/RELEASE`.

.. _reference-sumo-source-data:

source
::::::

*source data* describes where the :term:`sources` of a :term:`module` can be
found. It is a map with a single key. The key has one of the following values:

- path: This specifies a *directory* with the sources. The sources are copied
  from that location.
- tar: This specifies a *tar file* with the sources. The tar file is fetched
  and extracted.
- darcs: This specifies a *darcs repository*. 
- hg: This specifies a *mercurial repository*. 
- git: This specifies a *git repository*. 
- svn This specifies a *subversion repository*. 
- cvs This specifies a *cvs repository*. 

In the following description of source data, *FILEURL* means a string that is
either the path of a file on the local filesystem *or* an url of a file with
this form:

- ``http://``
- ``ftp://``
- ``ssh://``
- ``file://``

.. _reference-sumo-db-commands:

In the following description, *COMMANDS* means a list of strings that are
command lines which are executed in the given order inside the module directory
*after* the module was checked out. Possible patches (see below) are applied
after the commands. You may find the feature useful for git sub repositories
which must be initialized by an extra git command.

In the following description of source data, *PATCHFILES* means a list of
strings that are names of *patchfiles*. These are applied to the source with
the patch utility after the source is fetched. The strings specifying
patchfiles are FILEURLs.
  
path
^^^^

This is used to specify a directory that contains all the sources. 

For a directory in the local host, the *source data* has this form::

  {
      "path": "PATH"
  }

For a directory on a remote host that can be accessed with ssh, the *source
data* has this form::

  {
      "path": "USER@HOST:REMOTEPATH"
  }

tar
^^^

This is used to specify a tar, gzip tar or bzip tar file that contains the
sources. The filename must have one of these extensions:

- .tar : a simple tar file
- .tar.gz : a tar file compressed with gzip
- .tgz : a tar file compressed with gzip
- .tar.bz2 : a tar file compressed with bzip2

The *source data* has this form:: 

  {
      "tar": {
          "commands": COMMANDS,
          "patches": PATCHFILES,
          "url": "FILEURL"
      }
  }

The keys "commands" and "patches" are *optional*. 

"TARFILE" may be a filename or an URL with one of these forms:

- ``http://``
- ``ftp://``
- ``ssh://``
- ``file://``

darcs
^^^^^

This is used to specify a source from a darcs repository.  

The *source data* has this form:: 

  {
      "darcs": {
          "commands": COMMANDS,
          "patches": PATCHFILES,
          "tag": "TAG",
          "url": "REPOSITORY"
      }
  }

The keys "commands" and "patches" are *optional*. 

The key "tag" is also *optional*, if it is given it specifies the darcs tag that
is used to fetch the source. 

The key "url" is a darcs repository specification (see manual of darcs for
further information).

hg
^^

This is used to specify a source from a mercurial repository.  

The *source data* has this form:: 

  {
      "hg": {
          "commands": COMMANDS,
          "patches": PATCHFILES,
          "rev": "REVISION",
          "tag": "TAG",
          "url": "REPOSITORY"
      }
  }

The keys "commands" and "patches" are *optional*. 

The key "rev" is *optional*, if it is given it specifies the mercurial revision
that is used to fetch the source. Note that "rev" and "tag" MUST NOT be given
both.

The key "tag" is also *optional*, if it is given it specifies the mercurial tag
that is used to fetch the source. Note that "rev" and "tag" MUST NOT be given
both.

The key "url" is a mercurial repository specification (see manual of mercurial
for further information).

git
^^^

This is used to specify a source from a git repository.  

The *source data* has this form:: 

  {
      "git": {
          "commands": COMMANDS,
          "patches": PATCHFILES,
          "rev": "REVISION",
          "tag": "TAG",
          "url": "REPOSITORY"
      }
  }

The keys "commands" and "patches", "rev" and "tag" are *optional*. 

Note that "rev" and "tag" **must not** be given both.

If key "rev" is given it specifies the revision key of a *git commit*. After
the initial ``git clone`` sumo performs ``git checkout REVISION``.

If the key "tag" is given, it specifies a *tag* or a *branch* that is used to
fetch the source with ``git clone -b TAG``.

The key "url" is a git repository specification (see manual of git for
further information).

svn
^^^

This is used to specify a source from a subversion repository.  

The *source data* has this form:: 

  {
      "svn": {
          "commands": COMMANDS,
          "patches": PATCHFILES,
          "rev": "REVISION",
          "tag": "TAG",
          "url": "REPOSITORY"
      }
  }

The keys "commands" and "patches" are *optional*. 

The key "rev" is *optional*, if it is given it specifies the subversion revision
that is used to fetch the source. Note that "rev" and "tag" MUST NOT be given
both.

The key "tag" is also *optional*, if it is given it specifies the subversion tag
that is used to fetch the source. Note that "rev" and "tag" MUST NOT be given
both. If "tag" is given the string "tags" and the tag name are appended to the
repository url.

The key "url" is a subversion repository specification (see manual of
subversion for further information).

cvs
^^^

This is used to specify a source from a cvs repository.  

The *source data* has this form:: 

  {
      "cvs": {
          "commands": COMMANDS,
          "patches": PATCHFILES,
          "tag": "TAG",
          "url": "REPOSITORY"
      }
  }

The keys "commands" and "patches" are *optional*. 

The key "tag" is also *optional*, if it is given it specifies the cvs tag
that is used to fetch the source. 

The key "url" is the cvs repository specification. In the following "<cvsroot>"
means the path of your cvs repository and <module> is the directory within
"<cvsroot>" where the module is kept. "<user>" and "<host>" are the username
and hostname when you contact your cvs repository via ssh. There are three
formats you can use here:

Simple path 
  This has the form ``<cvsroot>/<module>`` 

Path with "file" prefix 
  This has the form ``file://<cvsroot>/<module>`` 

SSH path 
  This has the form ``ssh://<user>@<host>:<cvsroot>/<module>`` 

weight
::::::

This *optional* field is used to define the weight factor for a module. You
usually don't have to use this, see `db weight WEIGHT MODULES`_ for details.

The scan database
+++++++++++++++++

When :doc:`"sumo-scan all"<reference-sumo-scan>` is used to scan an existing
support directory it also gathers information on what version of a module
depends on what version of another module. In order to keep this information
although the dependency database doesn't contain versions of dependencies, this
information is held in a separate file, the scan database or :term:`SCANDB`.

Here is an example on how this file looks like::

  {
      "AGILENT": {
          "R2-3": {
              "BASE": {
                  "R3-14-12-2-1": "scanned"
              }
          }
      },
      "AGILENT-SUPPORT": {
          "R0-10": {
              "BASE": {
                  "R3-14-12-2-1": "scanned"
              }
          },
          "R0-11": {
              "BASE": {
                  "R3-14-12-2-1": "scanned"
              }
          },
          "R0-12": {
              "BASE": {
                  "R3-14-12-2-1": "scanned"
              }
          },
          "R0-9-5": {
              "BASE": {
                  "R3-14-12-2-1": "scanned"
              }
          }
      },
      "ALARM": {
          "R3-7": {
              "BASE": {
                  "R3-14-12-2-1": "scanned"
              },
              "BSPDEP_TIMER": {
                  "R6-2": "scanned"
              },
              "MISC_DBC": {
                  "R3-0": "scanned"
              }
          },
          "R3-8": {
              "BASE": {
                  "R3-14-12-2-1": "scanned"
              },
              "BSPDEP_TIMER": {
                  "R6-2": "scanned"
              },
              "MISC_DBC": {
                  "R3-0": "scanned"
              }
          }
      }
  }

The basic datastructure is this::

  {
      MODULENAME: {
          DEPENDENCY_MODULENAME: {
              DEPENDENCY_VERSION: STATE
              DEPENDENCY_VERSION: STATE
              ...
          }
      }
  }

For each dependency of a module this structure contains the version of the
dependency and a state. The state can be "stable" or "testing" or "scanned" but
is always "scanned" if the file was generated with sumo db.

.. _reference-sumo-The-build-database:

The build database
++++++++++++++++++

The build database :term:`BUILDS.DB` file is a `JSON <http://www.json.org>`_
file that contains information of all :term:`builds` in the 
:term:`support directory`.

Here is an example how this file looks like::

  {
      "001": {
          "modules": {
              "ALARM": "R3-5",
              "ASYN": "R4-15-bessy2",
              "BASE": "R3-14-8-2-0",
              "BSPDEP_CPUBOARDINIT": "R4-0",
              "BSPDEP_TIMER": "R5-1",
              "CSM": "R3-8",
              "EK": "R2-1",
              "GENSUB": "PATH-1-6-1",
              "MCAN": "R2-3-18",
              "MISC": "R2-4",
              "SEQ": "R2-0-12-1",
              "SOFT": "R2-5",
              "VXSTATS": "R2-0"
          },
          "state": "stable"
      },
      "002": {
          "linked": {
              "ASYN": "001",
              "BASE": "001",
              "BSPDEP_CPUBOARDINIT": "001",
              "BSPDEP_TIMER": "001",
              "CSM": "001",
              "EK": "001",
              "GENSUB": "001",
              "MISC": "001",
              "SEQ": "001",
              "SOFT": "001",
              "VXSTATS": "001"
          },
          "modules": {
              "ALARM": "R3-4",
              "ASYN": "R4-15-bessy2",
              "BASE": "R3-14-8-2-0",
              "BSPDEP_CPUBOARDINIT": "R4-0",
              "BSPDEP_TIMER": "R5-1",
              "CSM": "R3-8",
              "EK": "R2-1",
              "GENSUB": "PATH-1-6-1",
              "MCAN": "R2-3-18",
              "MISC": "R2-4",
              "SEQ": "R2-0-12-1",
              "SOFT": "R2-5",
              "VXSTATS": "R2-0"
          },
          "state": "unstable"
      }
  }

The basic datastructure is this::

  {
      BUILDTAG : {
          <builddata> 
          },
      BUILDTAG : {
          <builddata> 
          },
      ...
  }

The *builddata* has this form::

  {
      "linked": {
          <linkdata>
          },
      "modules": {
          <moduledata>
          },
      "state": <state>
  }

moduledata
::::::::::

moduledata is a map that maps :term:`modulenames` to :term:`versionnames`.
This specifies all the :term:`modules` that are part of the :term:`build`.
Since a :term:`build` may reuse :term:`modules` from another :term:`build` not
all modules from this map may actually exist as separate directories of the
:term:`build`. The *moduledata* has this form::

  {
      MODULENAME: VERSIONNAME,
      MODULENAME: VERSIONNAME,
      ...
  }

linkdata
::::::::

linkdata is a map that maps :term:`modulenames` to buildtags. This map contains
all :term:`modules` of the :term:`build` that are reused from other
:term:`builds`. If a :term:`build` has no linkdata, the key "linked" in
*builddata* is omitted. The *linkdata* has this form::

  {
      MODULENAME: BUILDTAG,
      MODULENAME: BUILDTAG,
      ...
  }

state
:::::

This is a :term:`state` string that describes the state of the :term:`build`.
Here are the meanings of the :term:`state` string:

* unstable: the :term:`build` has been created but not yet compiled
* testing: the :term:`build` has been compiled successfully
* stable: the :term:`build` has been tested in production successfully
* disabled the :term:`build` should no longer be used
* incomplete the :term:`build` is defined but not all module directories are
  created
* broken the :term:`build` is broken and should be deleted

Configuration Files
+++++++++++++++++++

Many options that can be given on the command line can be taken from
configuration files. For more details see
:doc:`"configuration files "<configuration-files>`.

Commands
--------

You always have to provide sumo with a *maincommand*. Some *maincommands* need
to be followed by a *subcommand*. 

maincommands
++++++++++++

.. _reference-sumo-help:

help COMMAND
::::::::::::

This command prints help for the given command. It can be invoked as::

  help
  help MAINCOMMAND
  help SUBCOMMAND
  help MAINCOMMAND SUBCOMMAND

You get a list of all known MAINCOMMANDS with::

  help maincommand

config SUBCOMMAND
:::::::::::::::::

Show the configuration or create or modify a configuration file. These are
known subcommands here:

- list       - list loaded configuration files
- local      - create configuration for "local" builds
- make       - create configuration file
- new        - create a new configuration file from one of the provided templates 
- show       - show configuration data
- standalone - create configuration for "standalone" builds

You get help on each subcommand with::

  help SUBCOMMAND

lock FILE
:::::::::

Lock a FILE, then exit sumo. This is useful if you want to read or write a
database file without sumo interfering. Don't forget to remove the lock later
with the "unlock" command.

This command must be followed by a *filename*.

unlock FILE
:::::::::::

Unlock a FILE, then exit sumo. If you locked a database with "lock" before you
should always unlock it later, otherwise sumo can't access the file.

This command must be followed by a *filename*.

db SUBCOMMAND
:::::::::::::

This is the maincommand for all operations that work with the 
dependency database or :term:`DEPS.DB` file.

For all of the db subcommands you have to specify the dependency database
directory with option ``--dbdir`` or a configuration file.

These are the known subcommands here:

alias-add
  add an alias for a dependency in a module

appconvert
  convert a scanfile to a MODULES file for an application

check
  consistency check of the DB file

clonemodule
  add a module under a new name in the DB file

cloneversion
  create a new DB entry by copying an old one

commands
  define commands to be executed after module checkout

convert
  convert a scanfile created by sumo-scan to a DB file

dependency-add
  add a dependency to a module

dependency-delete
  delete a dependency of a module

edit
  edit the dependency file with an editor

extra
  define extra lines to add to RELEASE file

find
  search for modules with a regexp

format
  reformat the dependency file

list
  list modules or versions of modules

make-recipes
  define special make-recipes for a module

merge
  merge two DB files

modconvert
  print new DB file entries for the given MODULES from a scanfile

releasefilename
  define an alternative filename for the RELEASE file

replaceversion
  replace a DB entry with a new one

show
  show details of moduleversions

weight
  set the weight factor for modules

You get help on each subcommand with::

  help SUBCOMMAND

build SUBCOMMAND
::::::::::::::::

This is the maincommand for all operations that work with builds and the build
database (:term:`BUILDS.DB`).

For all of the build subcommands you have to specify the dependency database
directory and the build directory with ``--dbdir`` and ``--builddir`` or a
configuration file.

These are the known subcommands:

delete
  delete a build

find
  look for builds that match a module specification

getmodules
  From a missing or incomplete module specification create a valid module
  specification from an existing build.

list
  list names of all builds

new
  create a new build

remake
  do "make clean" and "make all" with a build

show
  show details of a build

showmodules
  show modules of a build

showdependencies
  show dependences of a build or all builds

showdependents
  show dependents of a build or all builds

state
  show or change the state of a build

try
  check the module specification for completeness and consistency

use
  use all modules or your module specification in your application

You get help on each subcommand with::

  help SUBCOMMAND

subcommands for maincommand "config"
++++++++++++++++++++++++++++++++++++

.. _reference-sumo-config-list:

config list
:::::::::::

List all configuration files that were loaded.

config local DIRECTORY
::::::::::::::::::::::

This command is used to create a new sumo directory with a new build directory
but using existing builds from your current build directory. It also creates an
independent copy of the dependency database. 

DIRECTORY is created if it does not yet exist. This command takes all settings
and command line options but sets dbrepomode to "pull" and dbdir to
DIRECTORY/database. It also sets localbuilddir to DIRECTORY/build. Option
dbrepo must be set, this is used to create a local copy of the dependency
database in DIRECTORY/database. If there is a file "sumo.config" in the current
working directory it is copied to "sumo.config.bak". A new file "sumo.config"
is then created in the current working directory.

.. _reference-config-make:

config make FILENAME [OPTIONNAMES]
::::::::::::::::::::::::::::::::::

Create a new configuration file from the options read from configuration files
and options from the command line. If FILENAME is '-' dump to the console.
OPTIONNAMES is an optional list of long option names. If OPTIONNAMES are
specified, only options from this list are saved in the configuration file.

If this command is provided with option ``--getmodules BUILDTAG``, module specifications are updated from the specified build. This works like the command
:ref:`"build getmodules <reference-sumo-build-getmodules>`.

Here are two examples how to use this option:

If configure/MODULES does not yet exist, create a matching MODULES file for
build 'AUTO-004' for an application::

  sumo config make configure/MODULES alias module --getmodules AUTO-004

If configure/MODULES already exists (and is automatically loaded, see also
:ref:`sumo.config examples <configuration-files-config-examples>`), update
versions in MODULES file from the versions used in build 'AUTO-004'::

  sumo config make configure/MODULES alias module --getmodules AUTO-004

.. _reference-sumo-config-new:

config new DIRECTORY TEMPLATE
:::::::::::::::::::::::::::::

This command is used to create a new sumo directory with a new build directory
and a new dependency database. 

It creates a new configuration for sumo. DIRECTORY must not yet exist and is
created by this command. This command takes all settings and command line
options but sets dbdir to DIRECTORY/database. It also sets builddir to
DIRECTORY/build. TEMPLATE determines how the dependency database file is
created. Currently 2 values are known:

empty
  Create an empty dependency database.

github
  Create a sample dependency database file with some entries for EPICS base,
  ASYN, STREAMDEVICE, AREADETECTOR, SEQUENCER and more. In this sample all
  module repositories are fetched from the internet, mostly github.

If there is a file "sumo.config" in the current working directory it is copied
to "sumo.config.bak". A new file "sumo.config" is then created in the current
working directory.

.. _reference-sumo-config-show:

config show [OPTIONNAMES]
:::::::::::::::::::::::::

Show the configuration in JSON format.  OPTIONNAMES is an optional list of long
option names. If OPTIONNAMES are specified, only options from this list are
saved in the configuration file.

config standalone DIRECTORY
:::::::::::::::::::::::::::

This command is used to create a new sumo directory with an independent build
directory and an independent copy of the dependency database. 

It creates a new configuration for "standalone" builds. DIRECTORY is created if
it does not yet exist. This command takes all settings and command line options
but sets dbrepomode to "pull" and dbdir to DIRECTORY/database. It also sets
builddir to DIRECTORY/build. Option dbrepo must be set, this is used to create
a local copy of the dependency database in DIRECTORY/database. If there is a
file "sumo.config" in the current working directory it is copied to
"sumo.config.bak". A new file "sumo.config" is then created in the current
working directory.

subcommands for maincommand "db"
++++++++++++++++++++++++++++++++

db alias-add MODULE DEPENDENCY ALIAS
::::::::::::::::::::::::::::::::::::

Define a new :term:`alias` for a :term:`dependency` of a :term:`module`. MODULE
here is a :term:`modulespec` of the form MODULE:VERSION that specifies a single
version of a module.

db appconvert SCANFILE
::::::::::::::::::::::

Convert a :term:`scanfile` that was created by applying 
:doc:`"sumo-scan all"<reference-sumo-scan>` to an application to a list of
:term:`aliases` and :term:`modulespecs` in `JSON <http://www.json.org>`_
format. If SCANFILE is a dash "-" the program expects the scanfile on stdin.
The result is printed to the console. 

db check
::::::::

Do some consistency checks on the :term:`dependency database` file in the
directory specified by ``--dbdir``.

db clonemodule OLD-MODULE NEW-MODULE [VERSIONS]
:::::::::::::::::::::::::::::::::::::::::::::::

Copy all :term:`versions` of the existing old :term:`module` and add this with
the name of thew new :term:`module` to the :term:`dependency` database.
OLD-MODULE and NEW-MODULE here are just the module names since the versions may
follow as a separate argument. If there are no :term:`versions` specified, the
command copies all existing :term:`versions`. Note that this DOES NOT add the
new :term:`module` as :term:`dependency` to any other :term:`modules`.

db cloneversion MODULE OLD-VERSION NEW-VERSION [SOURCESPEC]
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

This command adds a new :term:`version` of a :term:`module` to the
:term:`dependency database` by copying the old :term:`version`. MODULE here is
just the name of the module since the version follows as a separate argument.

If SOURCESPEC is not given, the command copies the source specification from
OLD-VERSION but sets the tag to NEW-VERSION. Note that this is not allowed for
"path" and "tar" sources (see below).

If SOURCESPEC is given, the source specification from OLD-VERSION is copied an
the all values from SOURCESPEC are added.

A sourcespec has the form::
  NAME=VALUE[,VALUE...] [NAME=VALUE[,VALUE..] ...]

In general, NAME must start with a letter or underscore character and must be
following by a sequence of letters, underscores or digits.

A VALUE must be a JSON simple value (no map or list). If VALUE is a string, it
must be enclosed in double quotes '"' if it contains any of the characters '"',
',' or ' '.

These are possible names:

type
  The source type. Currently known are "path", "tar", "cvs", "svn", "darcs",
  "hg" and "git".

url
  This is the URL. For the types "path" and "tar" it may also be a filename.

tag
  This defines the revision tag.

rev
  This defines the revision hash key.

patches
  This defines names or URLs for patch files. This is the only name, where
  several values may be provided as a comma separated list.

commands
  This defines commands that are executed *after* the source code is checked
  out and *before* any patches are applied.

Note that you can define an empty value (on the bash shell) like in this
example::

  tag='""'

This means that the "tag" is removed from the source specification.

The command always asks for a confirmation of the action unless option "-y" is
used.

db commands MODULE LINES
::::::::::::::::::::::::

Define commands that are executed after a :term:`module` is checked out. See
also :ref:`"commands"<reference-sumo-db-commands>` in the chapter "The
dependency database".

MODULE here is a :term:`modulespec` of the form MODULE:VERSION that specifies a
single version of a module. LINES is a list of space separated strings. It is
recommended to enclose the line strings in single or double quotes.

Special variables and characters when you use double quotes:

- ``\"``: (bash) A literal double quote character.
- ``$(VAR)``: (make) Insert value of make or shell variable ``VAR``.
- ``$$``: (make) A dollar character passed to the shell.
- ``\\$$``: (make, bash) A literal dollar character passed to the shell.
- ``\\``: (json, bash) At the end of the json string this means line continuation for bash.

db convert SCANFILE
:::::::::::::::::::

Convert a :term:`scanfile` that was created by by 
:doc:`"sumo-scan all"<reference-sumo-scan>` to a new dependency database.  If
SCANFILE is a dash "-", the program expects the scanfile on stdin.  Note that
options ``--dbdir`` and ``--scandb`` are mandatory here. With ``--dbdir`` you
specify the directory where the new created 
:ref:`dependency database <reference-sumo-db-The-dependency-database>` file is
stored, with ``--scandb`` you specify the name of the scan database file. The
scan database file contains information on what moduleversion can be used with
what dependency version.

db dependency-add MODULE DEPENDENCY
:::::::::::::::::::::::::::::::::::

Add a :term:`dependency` to a :term:`module`. MODULE here is a
:term:`modulespec` of the form MODULE:VERSION that specifies a single version
of a module.

db dependency-delete MODULE DEPENDENCY
::::::::::::::::::::::::::::::::::::::

Delete a :term:`dependency` of a :term:`module`. MODULE here is a
:term:`modulespec` of the form MODULE:VERSION that specifies a single version
of a module.

.. _reference-sumo-db-edit:

db edit
:::::::

Start the editor specified by option ``--editor`` or the environment variables
"VISUAL" or "EDITOR" to edit the dependency database file. This command first
acquires a file-lock on the file, that prevents other users from accessing the
file at the same time.  When the editor program is terminated, sumo checks if
the file is still a valid `JSON <http://www.json.org>`_ file. If not, you can
start the editor again or abort the program. If the file is valid 
`JSON <http://www.json.org>`_, sumo commits the changes if option ``--dbrepo``
was specified.  If option ``--logmsg`` was given, this is used as commit log
message, otherwise an editor is started where you can enter a log message.
Finally the file lock is released. If you want to edit the dependency database
file you should always do it with this command.

.. _reference-sumo-db-extra:

db extra MODULE [LINES]
:::::::::::::::::::::::

Define extra lines that are appended to the generated RELEASE file of the
:term:`module`. See also :ref:`"extra"<reference-sumo-extra>` in the chapter
"The dependency database" of the documentation.

MODULE here is a :term:`modulespec` of the form MODULE:VERSION that specifies a
single version of a module. 

db find REGEXP
::::::::::::::

This command shows all :term:`modules` whose names or :term:`sources` match a
regexp.  Parameter REGEXP is a perl compatible :term:`regular expression`.  

db format
:::::::::

Just load and save the 
:ref:`dependency database <reference-sumo-db-The-dependency-database>`. 
This ensures that the file is formatted in the standard sumo format. This is
useful when the file was edited and you want to ensure that key sort order and
indentation are restored. If you specified a repository with ``--dbrepo,`` the
command will commit the changes. If you want a log message different from "db
format" use option ``--logmsg`` 

.. _reference-sumo-db-list:

db list MODULES
:::::::::::::::

If called with no argument, list the names of all :term:`modules`. If called
with '.', the wildcard symbol, list all :term:`versions` of all
:term:`modules`. If called with argument MODULES, a list of :term:`modulespecs`
MODULE:{+-}VERSION that specifies :term:`modules` and :term:`versions`, list
all the matching :term:`versions` of all specified :term:`modules`.

.. _reference-sumo-db-make-recipes:

db make-recipes MODULE [TARGET] [LINES]
:::::::::::::::::::::::::::::::::::::::

Define special make recipes for a :term:`module`. See also
:ref:`"make-recipes"<reference-sumo-make-recipes>` in the chapter "The
dependency database" of the documentation.

MODULE here is a :term:`modulespec` of the form MODULE:VERSION that specifies a
single version of a module. 

If TARGET is given, it must be "all", "clean", "config" or "distclean" and
specifies the make target for which a recipe is defined. LINES is a list of
space separated strings. It is recommended to enclose the line strings in
single or double quotes. If LINES is not given, all special rules for the
TARGET are removed.

If TARGET (and LINES) are not given, this defines *empty* make recipes. This
has to be done for modules that have no makefile at all. These modules are only
checked out by sumo, and possibly configured (see also
:ref:`"commands"<reference-sumo-db-commands>`).

Special variables and characters when you enclose LINES in double quotes:

- ``$DIR``: (sumo) The directory of the MODULE.
- ``\"``: (bash) A literal double quote character.
- ``$(VAR)``: (make) Insert value of make or shell variable ``VAR``.
- ``$$``: (make) A dollar character passed to the shell.
- ``\\$$``: (make, bash) A literal dollar character passed to the shell.
- ``\\``: (json, bash) At the end of the json string this means line continuation for bash.

db merge DB
:::::::::::

Merge the given :term:`dependency database` file with the 
:term:`dependency database` in the directory specified by ``--dbdir``. Sections
that do not exist in the original :term:`dependency database` are added.
Contradicting sections are treated as an error and abort the program. If a
module has an :ref:`"extra" <reference-sumo-extra>` section, only *new* lines
are appended to the existing :ref:`"extra" <reference-sumo-extra>` section. This
avoids having the same line several times in 
:ref:`"extra" <reference-sumo-extra>` after a merge operation.

db modconvert SCANFILE MODULES
::::::::::::::::::::::::::::::

Convert a :term:`scanfile` that was created by applying 
:doc:`"sumo-scan all"<reference-sumo-scan>` to the 
:ref:`dependency database <reference-sumo-db-The-dependency-database>`
format for all the selected modules. If SCANFILE is a dash "-" the program
expects the scanfile on stdin.  The result is printed to the console. This data
can be added to the dependency database using the command `db edit`_.

db releasefilename MODULE RELEASEFILENAME
:::::::::::::::::::::::::::::::::::::::::

This command defines an alternative filename for the RELEASE file of the
:term:`module`. Usually the RELEASE file is generated as "configure/RELEASE".
You can specify a different filename for the given :term:`module` with this
command. This may be useful for support :term:`modules` that have no regular
EPICS makefile system or for some special configurations of the EPICS base. If
you set the RELEASEFILENAME to an empty string or "configure/RELEASE", the
special entry for the filename is removed for this module in the
:term:`dependency database`.

db replaceversion MODULE OLD-VERSION NEW-VERSION
::::::::::::::::::::::::::::::::::::::::::::::::

This command replaces a :term:`version` of a :term:`module` with a new
:term:`version`. MODULE here is just the name of the module since the version
follows as a separate argument. All the data of the :term:`module` is copied.
If sourcespec is given, the command changes the source part according to this
parameter. A sourcespec has the form "path PATH", "tar TARFILE", "REPOTYPE URL"
or "REPOTYPE URL TAG".  REPOTYPE may be "darcs", "hg" or "git". Both, URL or
TAG may be ".", in this case the original URL or TAG remains unchanged.

.. _reference-sumo-db-show:

db show MODULES
:::::::::::::::

This command prints only the parts of the dependency database that contain the
given :term:`modules`. 

Parameter MODULES is a list of :term:`modulespecs` MODULE:{+-}VERSION that
specifies the :term:`modules` and :term:`versions` to operate on. 

db weight WEIGHT MODULES
::::::::::::::::::::::::

Set the weight factor for modules. A weight determines where a module is placed
in the generated RELEASE file. Modules there are sorted first by weight, then
by dependency. Parameter MODULES is a list of :term:`modulespecs`. Use
modulename:{+-}versionname to select more versions of a module.

Note that this command *does not* use the ``--modules`` command line option.

Parameter WEIGHT must be an integer.

subcommands for maincommand "build"
+++++++++++++++++++++++++++++++++++

build delete BUILDTAGS
::::::::::::::::::::::

The directories of the :term:`builds` are removed and their entries in the
:term:`build database` are deleted. If other builds depend on the
:term:`builds` to be deleted, the command fails unless option '--recursive' is
given. In this case all dependent builds are deleted, too.  The
:term:`buildtags` must be given as an argument.

build find MODULES
::::::::::::::::::

This command is used to find matching :term:`builds` for a given list of
:term:`modulespecs`. Each module in MODULES here is a :term:`modulespec` of the
form MODULE or MODULE:{+-}VERSION that specifies just a module name, a module
and some versions or a single version. For details on :term:`modulespecs` see
:doc:`Module Specifications <modulespecs>`.

With option ``--brief`` the command just prints :term:`buildtags` of matching
:term:`builds`. 

Otherwise each :term:`buildtag` is followed by a list of flags and
:term:`module` names. Each flag indicates whether the :term:`module` was found
with a matching :term:`version`, if it was found with a wrong :term:`version`
or if it is missing in the :term:`build`. 

If option ``--all-builds`` is given, builds whose :term:`state` is not 'stable'
or 'testing' are also shown.

Options ``--sort-build-dependencies-first`` and
``--sort-build-dependencies-last`` can be used to change the order reported
builds. Without these options, :term:`builds` are sorted by *match rank*.
Builds that have more :term:`modules` with matching :term:`versions` are placed
first, followed by the ones with more wrong :term:`versions` followed by the
ones with more missing :term:`versions`.

Option ``--detail`` determines, what is shown. This must be an integer between
0 and 2. With ``0``, the default, only :term:`builds` with matching
:term:`module` :term:`versions` are shown. With ``1``, also :term:`builds` with
wrong :term:`versions` are shown and with ``2`` even :term:`builds` with
missing :term:`modules` are shown.

This is the meaning of the *flags* in the output of this command:

- ``==``: The :term:`module` :term:`version` matches exactly.
- ``=~``: The :term:`module` :term:`version` matches the module specification.
- ``!=``: The :term:`module` has the wrong :term:`version`.
- ``-``: The :term:`module` is missing in the :term:`build`.

Here is an example::

  $ sumo build find MCAN ALARM:R3-7 --detail 1:
  MYAPP-002
      == ALARM:R3-7
      =~ MCAN:R2-6-3-gp
  MYAPP-001
      != ALARM:R3-8-modified
      =~ MCAN:R2-6-3-gp

We wanted *any* version of `MCAN` and version `R3-7` of `ALARM`. The command
found two builds, `MYAPP-002` and `MYAPP-001`.

In `MYAPP-002`, `ALARM` matches exactly the version we wanted, `MCAN` matches
our specification since we didn't define a version.

In `MYAPP-001`, `ALARM` has not the :term:`version` we specified, but this
:term:`build` is reported anyway since we used ``--detail 1``. `MCAN` matches
our specification since we didn't define a version.

Finally, if the command ``sumo build use`` doesn't find a build for your module
specifications, you may want to run ``sumo build find --detail 1`` or ``sumo
build find --detail 2``. This may help you finding errors in your module
specification in file `configure/MODULES`.

.. _reference-sumo-build-getmodules:

build getmodules BUILDTAG [MODULES]
:::::::::::::::::::::::::::::::::::

This command shows the modules in the form MODULE:VERSION of a :term:`build`.

The :term:`buildtag` is mandatory.

.. note::
   Sumo doesn't distinguish between modules defined on the command line or in
   configuration files like `configure/MODULES`. If modules *are somewhere*
   defined, they will be used by this command.

If :term:`modules` are specified, only these modules and
their dependent modules with the versions from the specified build are shown.
If the build doesn't contain all the requested modules, sumo stops with an
error message.

With option ``--lines`` for each build the output is a single line instead of a
number of indented lines. In this case, the output is compatible with the
``-m`` option of sumo. 

Here are some applications for this, please look also at :ref:`"config make
<reference-config-make>` with option ``--getmodules`` which does the same:

If configure/MODULES does not yet exist, create a matching MODULES file for
build 'AUTO-004' for an application::

  sumo config make configure/MODULES alias module -m "$(sumo build getmodules AUTO-004 --lines)"

If configure/MODULES already exists (and is automatically loaded, see also
:ref:`sumo.config examples <configuration-files-config-examples>`), update
versions in MODULES file from the versions used in build 'AUTO-004'::

  sumo config make configure/MODULES alias module -m "$(sumo build getmodules AUTO-004 --lines)"

.. _reference-sumo-build-list:

build list
::::::::::

This command lists the names of all builds. Options
``--sort-build-dependencies-first`` and ``--sort-build-dependencies-last`` can
be used to change the order of the builds shown. The command shows only builds
with state 'stable' or 'testing' unless option ``--all-builds`` is provided.

.. _reference-sumo-new:

build new MODULES
:::::::::::::::::

This command creates a new :term:`build`. Each module given in MODULES here is
a :term:`modulespec` of the form MODULE:VERSION that specifies a single version
of a module. If a build for the given :term:`modulespecs` already exists, the
command aborts with an error message, or terminates with a warning if option
``--no-err-build-exists`` is given.  If the :term:`buildtag` is not given as an
option, the program generates a :term:`buildtag` in the form "AUTO-nnn". A new
:term:`build` is created according to the :term:`modulespecs`. Your
module specifications must be *complete* and *exact* meaning that all
:term:`dependencies` are included and all :term:`modules` are specified with
exactly a single :term:`version`. Use command "build try" in order to create
:term:`module` specifications that can be used with command "build new".  This
command calls "make" and, after successful completion, sets the state of the
:term:`build` to "testing". If you want to skip this step, use option
``--no-make``. In order to provide arbitrary options to make use option
``--makeflags``. 

build remake BUILDTAG
:::::::::::::::::::::

This command recreates a :term:`build` by first calling "make clean" and
then "make all" with the build's makefile. If you develop a support
:term:`module` (see also "config standalone" and "config local") you want to
recompile the :term:`build` after changes in the sources. In order to provide
arbitrary options to make use option ``--makeflags``. 

.. _reference-sumo-build-show:

build show BUILDTAG
:::::::::::::::::::

This command shows the data of a :term:`build`. The :term:`buildtag` must be
given as an argument.

build showmodules [BUILDTAG]
::::::::::::::::::::::::::::

This command shows the modules in the form MODULE:VERSION of a :term:`build`.

The :term:`buildtag` is optional if :term:`modules` are also not specified.

Without a :term:`buildtag`, the command shows the modules for all builds with
state 'stable' or 'testing'. To see all builds regardless of their state use
option ``--all-builds``.

Options ``--sort-build-dependencies-first`` and
``--sort-build-dependencies-last`` can be used to change the order reported
builds. 

With option ``--lines`` for each build the output is a single line instead of a
number of indented lines. With ``-b``, the build name is not printed. If you
use ``--lines`` and ``-b``, the output is compatible with the ``-m`` option of
sumo. Here are some applications for this:

If configure/MODULES does not yet exist, create a matching MODULES file for
build 'AUTO-004' for an application::

  sumo config make configure/MODULES alias module -m "$(sumo build showmodules AUTO-004 --lines -b)"

Re-create a complete set of builds from an existing BUILDS.DB on a different
machine::

  [machine 1] $ sumo build showmodules --lines -b --sort-build-dependencies-first >  BUILDS.TXT

  [machine 2] $ cat BUILDS.TXT | while read line; do sumo build new -m "$line"; done

build showdependencies [BUILDTAG]
:::::::::::::::::::::::::::::::::

This command shows the builds that the given :term:`build` depends on. The
:term:`buildtag` is optional, if omitted the command shows the dependencies for
all builds with state 'stable' or 'testing'. To see all builds regardless of
their state use option ``--all-builds``.

Options 
``--sort-build-dependencies-first`` and ``--sort-build-dependencies-last``
can be used to change the order reported dependencies.


build showdependents [BUILDTAG]
:::::::::::::::::::::::::::::::

This command shows all builds that depend on the given :term:`build`.  The
:term:`buildtag` is optional, if omitted the command shows the dependents for
all builds with state 'stable' or 'testing'. To see all builds regardless of
their state use option ``--all-builds``.

Options 
``--sort-build-dependencies-first`` and ``--sort-build-dependencies-last``
can be used to change the order reported dependents.


build state BUILDTAG [NEW-STATE]
::::::::::::::::::::::::::::::::

This command is used to show or change the :term:`state` of a :term:`build`.
The :term:`buildtag` must be given as an argument. If there is no new
:term:`state` given, it just shows the current :term:`state` of the
:term:`build`. Otherwise the :term:`state` of the :term:`build` is changed to
the given value. If a :term:`build` is set to :term:`state` 'disabled', all
dependent builds are also set to this :term:`state`. In this case, unless
option '-y' or '--recursive' are given, sumo asks for your confirmation.

build try MODULES
:::::::::::::::::

This command is intended to help you create :term:`module` specifications for
the "build new" command. 

Each MODULE here is a :term:`modulespec` of the form MODULE or
MODULE:{+-}VERSION that specifies just a module name, a module and some
versions or a single version. You can specify an incomplete list of
:term:`modules`.

The detail of the output is determined by option ``--detail`` which is an
integer between 0 and 3. 0, the default, gives the shortest, 3 gives the
longest report. The program then shows which :term:`modules` you have to

In any case the command shows which :term:`modules` are missing since they
depend on other :term:`modules` of your specification and which ones are
missing an exact :term:`version`.

If you converted an existing support directory to sumo you have a scan database
file which you can specify with option ``--scandb`` to this command.

For a detailed example see :ref:`try example <example-sumo-build-try>`.

.. _reference-sumo-use:

build use MODULES
:::::::::::::::::

This command creates a configure/RELEASE file for an application. Each module
given in MODULES here is a :term:`modulespec` of the form MODULE:VERSION that
specifies a single version of a module. If option ``--buildtag`` is given, it
checks if this is compatible with the given :term:`modules`.  Otherwise it
looks for all :term:`builds` that have the :term:`modules` in the required
:term:`versions`. If more than one matching :term:`build` found it takes the
one with the alphabetically first buildtag. The RELEASE file created includes
only the :term:`modules` that are specified. Output to another file or the
console can be specified with option '-o'.

If no :term:`build` is found you may:

- Look if you module specification has an error by looking for *almost*
  matching :term:`builds` with:

  - ``sumo build find --detail 1``
  - ``sumo build find --detail 2``

- Create a :term:`build` matching your :term:`module` specification with:

  - ``sumo build new``

.. _reference-sumo-command-completion:

Command completion
------------------

Command completion means that you can press <TAB> on any incomplete sumo
command and you get a list of possibilities how to complete that command. By
pressing <TAB> several times you can try each possible completion.

Prerequisites
+++++++++++++

Command completion works with `bash` or `zsh` (Z-Shell), you need to have one
of these installed. Your environment variable `SHELL` must be set to the binary
file of the shell, e.g. `/usr/bin/bash` or `/usr/bin/zsh`.

In any case the package `bash-completion` must be installed.

If you use the Z-Shell, the following commands must be executed at start up.
Add them for example to the file `$HOME/.zshenv`::

  autoload -U +X compinit && compinit
  autoload -U +X bashcompinit && bashcompinit

There are two ways to activate command completion, described in the following
chapters.

Activate command completion on the fly
++++++++++++++++++++++++++++++++++++++

Enter this command::

  ``eval `sumo help completion-line```
 
Activate command completion permanently
+++++++++++++++++++++++++++++++++++++++

Enter this command::

  ``sumo help completion-script > $HOME/_sumo``

Then add the line::

  ``source $HOME/_sumo``

to your $HOME/.bashrc or $HOME/.zshrc

Completion cache files
++++++++++++++++++++++

Sumo will create cache files in your home directory to speed up command
completion. These are the files ".dbcache.sumo" and ".buildcache.sumo". If you
don't want this set the environment variable "SUMOHELP" in a way that it
contains the string "nocache" like in::

  export SUMOHELP="nocache"

If there are other help options defined in SUMOHELP, you should separate them
with commas ",".

The help pager
--------------

The build in pager allows you to navigate in long help texts that sumo displays
when you use command "help" or option "-h". There are three modes:

pager:off
  The pager is off, all help is printed directly to the console.

pager:on
  The pager is used only for long help texts (more than 24 lines).

pager:always
  The pager is always used, even for short help texts.

Mode "pager:on" is the default.

You define the pager mode by adding one of the three strings to the environment
variable "SUMOHELP" like in::

    export SUMOHELP="pager:off"

If there are other help options defined in SUMOHELP, you should separate them
with commas ",".

Options
-------

.. _reference-sumo-Options:

Here is a short overview on command line options:

``--#opt-postload FILES``
+++++++++++++++++++++++++

    This option does the same as --#postload but the file loading is optional.
    If they do not exist the program continues without an error.

``--#opt-preload FILES``
++++++++++++++++++++++++

    This option does the same as --#preload but the file loading is optional.
    If they do not exist the program continues without an error.

``--#postload FILES``
+++++++++++++++++++++

    Specify a an '#postload' directive in the configuration file. This option
    has only a meaning if a configuration file is created with the 'makeconfig'
    command. '#postload' means that the following file(s) are loaded after the
    rest of the configuration file.

``--#preload FILES``
++++++++++++++++++++

    Specify a an '#preload' directive in the configuration file. This option
    has only a meaning if a configuration file is created with the 'makeconfig'
    command. '#preload' means that the following file(s) are loaded before the
    rest of the configuration file.

``-a ALIAS, --alias ALIAS``
+++++++++++++++++++++++++++

    Define an alias for the command 'use'. An alias must have the form FROM:TO.
    The path of module named 'FROM' is put in the generated RELEASE file as a
    variable named 'TO'. You can specify more than one of these by repeating
    this option or by joining values in a single string separated by spaces. A
    default for this option can be put in a configuration file.

``--all-builds``
++++++++++++++++

    Some subcommands of 'build' show only information for builds that have the
    states 'stable' or 'testing'. If this option is given, the commands show
    *all* builds regardless of their state.

``-A, --append OPTIONNAME``
+++++++++++++++++++++++++++++++

    If an option with name OPTIONNAME is given here and it is a list option,
    the list from the command line is *appended* to the list from the
    configuration file. The default is that options from the command line
    *override* option values from the configuration file.

``-b, --brief``
+++++++++++++++

    Create a more brief output for some commands.

``--builddir BUILDDIR``
+++++++++++++++++++++++

    Specify the support directory. If this option is not given take the current
    working directory as support directory. A default for this option can be
    put in a configuration file.

``-t BUILDTAG, --buildtag BUILDTAG``
++++++++++++++++++++++++++++++++++++

    Specify a buildtag.

``--buildtag-stem STEM``
++++++++++++++++++++++++

    Specify the stem of a buildtag. This option has only an effect on the
    commands 'build new' and 'build try' if a buildtag is not specified. The
    program generates a new tag in the form 'stem-nnn' where 'nnn' is the
    smallest possible number that ensures that the buildtag is unique.

``-c FILE, --config FILE``
++++++++++++++++++++++++++

    Load options from the given configuration file. You can specify more than
    one of these.  Unless --no-default-config is given, the program always
    loads configuration files from several standard directories first before it
    loads your configuration file. The contents of all configuration files are
    merged.

.. _reference-sumo-Options-dbdir:

``--dbdir DBDIR``
+++++++++++++++++

    Define the directory where the dependency database file 'DEPS.DB' is found.
    A default for this option can be put in a configuration file.

.. _reference-sumo-Options-dbrepo:

``--dbrepo REPOSITORY``
+++++++++++++++++++++++

    Define a REPOSITORY for the db file. REPOSITORY must have the form
    'REPOTYPE URL' or 'type=REPOTYPE url=URL". REPOTYPE may be 'darcs', 'hg',
    'git', 'svn' or 'cvs'. Option :ref:`--dbdir <reference-sumo-Options-dbdir>`.
    must specify a directory that will
    contain the repository for the db file. What repository operations sumo performs 
    when it reads or writes the db file depends on option 
    :ref:`--dbrepomode <reference-sumo-Options-dbrepomode>`.
    A default for this option can be put in a configuration file.

.. _reference-sumo-Options-dbrepomode:

``--dbrepomode MODE``
+++++++++++++++++++++

    Specify how sumo should use the dependency database repository. There are
    three possible values: 'get', 'pull' and 'push'. Mode 'get' is the default.
    The meaning depends on the used version control system (VCS), if it is
    distributed (git,mercurial,darcs) or centralized (subversion,cvs). There
    are three possible operations on the dependency database:

      * init : create the dependency database if it doesn't exist
      * read : read the dependency database
      * write: write (change) the dependency database

    Here is what happens during these operations depending on the mode:

    +------+----------+--------------------------------------------+
    |mode  |operation |action                                      |
    +======+==========+============================================+
    |get   |init      |create the repository if it doesn't exist   |
    |      +----------+--------------------------------------------+
    |      |read      |none                                        |
    |      +----------+--------------------------------------------+
    |      |write     |distr. VCS: commit changes                  |
    |      |          +--------------------------------------------+
    |      |          |centr. VCS: none                            |
    +------+----------+--------------------------------------------+
    |pull  |init      |create the repository if it doesn't exist   |
    |      +----------+--------------------------------------------+
    |      |read      |distr. VCS: pull                            |
    |      |          +--------------------------------------------+
    |      |          |centr. VCS: update                          |
    |      +----------+--------------------------------------------+
    |      |write     |distr. VCS: commit changes                  |
    |      |          +--------------------------------------------+
    |      |          |centr. VCS: none                            |
    +------+----------+--------------------------------------------+
    |push  |init      |create the repository if it doesn't exist   |
    |      +----------+--------------------------------------------+
    |      |read      |distr. VCS: pull                            |
    |      |          +--------------------------------------------+
    |      |          |centr. VCS: update                          |
    |      +----------+--------------------------------------------+
    |      |write     |distr. VCS: pull, commit changes, push      |
    |      |          +--------------------------------------------+
    |      |          |centr. VCS: update, commit changes          |
    +------+----------+--------------------------------------------+

``--detail NO``
+++++++++++++++

    Control the output of command 'try'. The value must be an integer between 0
    (very short) and 3 (very long)."

``-D EXPRESSION, --dir-patch EXPRESSION``
+++++++++++++++++++++++++++++++++++++++++

    This option is used for commands ``db convert`` and ``db modconvert``. It
    specifies a directory patchexpression. Such an expression consists of a
    tuple of 2 python strings. The first is the match expression, the second
    one is the replacement string. The regular expression is applied to every
    source path generated. You can specify more than one patchexpression. A
    default for this option can be put in a configuration file.

.. _reference-sumo-disable-loading:

``--disable-loading``
+++++++++++++++++++++

    If given, disable execution of load commands like '#preload' in
    configuration files. In this case these keys are treated like ordinary
    keys.

``-n, --dry-run``
+++++++++++++++++

    Just show what the program would do.

``--dump-modules``
++++++++++++++++++

    Dump module specs, then stop the program.

``--dumpdb``
++++++++++++

    Dump the modified db on the console, currently only for the commands
    "weight", "merge", "cloneversion" and "replaceversion".

``--editor EDITOR``
+++++++++++++++++++

    Specify the preferred editor. If this is not given, sumo takes the name of
    the editor from environment variables "VISUAL" or EDITOR".

``--exceptions``
++++++++++++++++

    On fatal errors that raise python exceptions, don't catch these. This will
    show a python stacktrace instead of an error message and may be useful for
    debugging the program.

``-X REGEXP, --exclude-states REGEXP``
++++++++++++++++++++++++++++++++++++++

    For command 'try' exclude all 'dependents' whose state does match one of
    the regular expressions (REGEXP).

``-x EXTRALINE, --extra EXTRALLINE``
++++++++++++++++++++++++++++++++++++

    Specify an extra lines that are added to the generated RELEASE file. This
    option can be given more than once to specify more than one line. A default
    for this option can be put in a configuration file, there the value must be
    a list of strings, one for each line.

``--getmodules BUILDTAG``
+++++++++++++++++++++++++

    If this option is used with command `config make` it updates your module
    specifications like the command "build getmodules BUILDTAG`. See also 
    description of :ref:`config make <reference-config-make>`.

``-h [OPTIONS], --help [OPTIONS]``
++++++++++++++++++++++++++++++++++

    If other OPTIONS are given, show help for these options. If OPTIONS is
    'all', show help for all options. If OPTIONS is missing, show a short
    generic help message for the program.

``--jobs``
++++++++++

    Specify the maximum number of jobs in sumo to run simultaneously. Currently
    this is used when the sources for modules of a build are created by
    checking out from version control systems. This number should be an integer
    greater or equal to 0. 0 means that the job number is equal to the number
    of CPUs, 1 means that there is only 1 job running at the same time, all
    greater numbers specify the number of jobs running simultaneously. The
    default for this option is 0.

``--lines``
+++++++++++
 
    Show results of "build showmodules" in single lines.

``--list``
++++++++++

    Show information for automatic command completion.

``--localbuilddir BUILDDIR``
++++++++++++++++++++++++++++

    Specify a *local* support directory. Modules from the directory specifed
    by --builddir are used but this directory is not modfied. All new builds
    are created in the local build directory and only the build database file
    there is modified.

``--logmsg LOGMESSAGE``
+++++++++++++++++++++++

    Specify a logmessage for automatic commits when --dbrepo is used.

``--makeflags MAKEFLAGS``
+++++++++++++++++++++++++

    Specify extra option strings for make You can specify more than one of
    these by repeating this option or by joining values in a single string
    separated by spaces. A default for this option can be put in a
    configuration file.

``-m MODULE, --module MODULE``
++++++++++++++++++++++++++++++

    Define a :term:`modulespec`. If you specify modules with this option you
    don't have to put :term:`modulespecs` after some of the commands. You can
    specify more than one of these by repeating this option or by joining
    values in a single string separated by spaces. A default for this option
    can be put in a configuration file.

``--no-checkout``
+++++++++++++++++

    With this option, "build new" does not check out sources of support
    modules. This option is only here for test purposes.

``-C, --no-default-config``
+++++++++++++++++++++++++++

    If this option is not given and --no-default-config is not given, the
    program tries to load the default configuration file sumo-scan.config from
    several standard locations (see documentation on configuration files).

``-N, --no-err-build-exists``
+++++++++++++++++++++++++++++

    If "build new" finds that a build for the given :term:`modulespecs` already
    exists, it returns an error. If this option is given, the command in this
    case only prints a warning and terminates sumo without error.

``--no-make``
+++++++++++++

    With this option, "build new" does not call "make".

``--noignorecase``
++++++++++++++++++

    For command 'find', do NOT ignore case.

``--nolock``
++++++++++++

    Do not use file locking.

``-o OUTPUTFILE, --output OUTPUTFILE``
++++++++++++++++++++++++++++++++++++++

    Define the output for command 'use'. If this option is not given, 'use'
    writes to 'configure/RELEASE'. If this option is '-', the command writes to
    standard-out.",

``-p, --progress``
++++++++++++++++++

    Show progress of some commands on stderr. A default for this option can be
    put in a configuration file.

``--readonly``
++++++++++++++

    Do not allow modifying the database files or the support directory. A
    default for this option can be put in a configuration file.

``--recursive``
+++++++++++++++

    For command 'build delete', delete all dependend builds, too. For command
    'build state' with state 'disabled', disable all dependend builds, too.

``--scandb SCANDB``
+++++++++++++++++++

    Specify the (optional) :term:`SCANDB` file. The scan database file contains
    information on what moduleversion can be used with what dependency version.

``--sort-build-dependencies-first``
+++++++++++++++++++++++++++++++++++

    For commands "build list", "build find -b", "build showdependencies" and
    "build showdependents" sort the builds that dependencies of a build always
    come before the build. 

``--sort-build-dependencies-last``
++++++++++++++++++++++++++++++++++

    For commands "build list", "build find -b", "build showdependencies" and
    "build showdependents" sort the builds that dependencies of a build always
    come after the build. 

``--summary``
+++++++++++++
    Print a summary of the function of the program.

``--test``
++++++++++
    Perform some self tests.

``--trace``
+++++++++++

    Switch on some trace messages.

``--tracemore``
+++++++++++++++

    Switch on even more trace messages.

``-U EXPRESSION, --url-patch EXPRESSION``
+++++++++++++++++++++++++++++++++++++++++

    This option is used for commands ``db convert`` and ``db modconvert``.
    Specify a repository url patchexpression. Such an expression consists of a
    tuple of 2 python strings. The first is the match expression, the second
    one is the replacement string. The regular expression is applied to every
    source url generated. You can specify more than one patchexpression. A
    default for this option can be put in a configuration file.

``-v, --verbose``
+++++++++++++++++

    Show command calls. A default for this option can be put in a
    configuration file.

``--version``
+++++++++++++

    Show the program version and exit.

``-y, --yes``
+++++++++++++

    All questions the program may ask are treated as if the user replied 'yes'.

