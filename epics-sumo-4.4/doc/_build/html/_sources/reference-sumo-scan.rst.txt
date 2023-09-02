sumo-scan
=========

What the script does
--------------------

This script scans an existing `EPICS <http://www.aps.anl.gov/epics>`_ support
module directory tree and collects all information necessary to generate a
dependency database :term:`DEPS.DB` file.  The data is formatted in 
`JSON <http://www.json.org>`_ format and printed to the console. You can either
save this output in a file or combine this script with 
:doc:`sumo db <reference-sumo>` in a pipe to directly create a :term:`DEPS.DB`
file.

The script takes one or mode commands and has a number of options. Single
character options always start with a single dash "-", long options start with
a double dash "--", commands are simple words on the command line.

How it works
------------

The program collects information in several phases. The output of each phase is
taken as an input for the next phase. If you use the command "all", the first
three phases are run at a time. If you run some phases alone by using the
commands "deps", "groups" or "repos" you have to provide the input of a phase
from a file by using the command line option ``--info-file``.

All three phases that are needed to create the data for generating a dependency
database with :doc:`sumo db <reference-sumo>` are combined with the command
"all". 

Two other phases "name2paths" and "path2names" are implemented to get
information on the existing module support tree but are not needed to create a
dependency database.

Phase I, RELEASE file scanning
++++++++++++++++++++++++++++++

Information on dependencies of `EPICS <http://www.aps.anl.gov/epics>`_ modules
is stored in files named "RELEASE" in directory "configure". For each module
the module depends on, there is a variable with a path. This is a short example
of what you could find in a RELEASE file::

  SUPPORT=/opt/Epics/R3.14.8/support
  MISC=$(SUPPORT)/misc/2-4
  ALARM=$(SUPPORT)/alarm/3-1
  SOFT=$(SUPPORT)/soft/2-2

The script calls "make" for each "RELEASE" file found to generate a list of all
generated variables. By calling make it is ensured that all macros, e.g.
"SUPPORT" in the example above, are resolved. By calling "make" twice, one time
without and one time with the "RELEASE" file the script computes a difference
of the set of defined variables of both runs. This difference contains all the
changes in variables that are caused by parsing the "RELEASE" file.

From this set of variable names and values the script removes names which match
a given list. For example, "TOP" usually refers to a directory that is not an
`EPICS <http://www.aps.anl.gov/epics>`_ support.

The remaining variable definitions are assumed to be module dependencies. 

The program builds a map where the keys are absolute paths of support modules.
The values are maps which map variable names to absolute paths which are in
fact the module's dependencies. Here is a short `JSON <http://www.json.org>`_
example of the created data structure::

  {
      "dependencies": {
          "/srv/csr/Epics/R3.14.8/support/alarm/3-3": {
              "EPICS_BASE": "/srv/csr/Epics/R3.14.8/base/3-14-8-2-0",
              "MISC": "/srv/csr/Epics/R3.14.8/support/misc/2-4",
              "TIMER": "/srv/csr/Epics/R3.14.8/support/bspDep/timer/4-0"
          },
          "/srv/csr/Epics/R3.14.8/support/alarm/3-4": {
              "EPICS_BASE": "/srv/csr/Epics/R3.14.8/base/3-14-8-2-0",
              "MISC": "/srv/csr/Epics/R3.14.8/support/misc/2-4",
              "TIMER": "/srv/csr/Epics/R3.14.8/support/bspDep/timer/5-0"
          },
          "/srv/csr/Epics/R3.14.8/support/csm/3-2": {
              "EPICS_BASE": "/srv/csr/Epics/R3.14.8/base/3-14-8-2-0"
          },
          "/srv/csr/Epics/R3.14.8/support/csm/3-3": {
              "EPICS_BASE": "/srv/csr/Epics/R3.14.8/base/3-14-8-2-0"
          },
      }
  }

.. _reference-sumo-scan-Phase-II-Grouping:

Phase II, Grouping
++++++++++++++++++

In this phase the program tries to build groups of modules. A group is a
collection all the versions of a support module. This is done by parsing module
paths. The program assumes that each module has a path of the form
"[BASEDIR]/[MODULEPATH]/[VERSION]". [VERSION] is simply the last part of the
path that contains no slashes "/". [BASEDIR] is given as a command line option
to the program (see option ``--group-basedir``) and [MODULEPATH] is all that
remains of the path. In order to create a *modulename* the program changes all
characters in [MODULEPATH] to uppercase and replaces all slashes "/" with
underscore "_" characters. Here is an example of the created datastructure in 
`JSON <http://www.json.org>`_ format::

  {
      "groups": {
          "AGILENT": {
              "/srv/csr/Epics/R3.14.8/support/agilent": [
                  "2-0",
                  "2-1",
                  "2-2",
                  "head"
              ]
          },
          "ALARM": {
              "/srv/csr/Epics/R3.14.8/support/alarm": [
                  "3-0",
                  "3-1",
                  "3-2",
                  "3-3",
                  "3-4",
                  "3-5",
                  "base-3-14"
              ]
          },
      }
  }

.. _reference-sumo-scan-Phase-III-repository-scan:

Phase III, repository scan
++++++++++++++++++++++++++

Usually your support modules are managed by a version control system. Currently
the program supports *darcs*, *mercurial*, *git*, *subversion* and *cvs*.

In each module the program looks for the data of a supported version control
system. If no version control data is found, the program marks the source of
the module as a *path* meaning that `sumo build <reference-sumo>` will
copy the sources from exactly that path.

If version control data is found the program it looks for a repository tag. It
only accepts a tag if it matches the last part of the support module path. The
program creates a version number from both, the path and the tag and only if
this number is equal, the tag is accepted. Here are some examples:

============================    =======   ============
path                            tag       tag accepted
============================    =======   ============
/Epics/support/NewDyncon/3-1    R3-1      yes
/Epics/support/NewDyncon/3-0    ver-3-0   yes
/Epics/support/NewDyncon/2-9    R2-8      no
/Epics/support/NewDyncon/2-7    R2-8      no
============================    =======   ============

The program also looks for the path of the foreign repository, this is assumed
to be the central repository we should refer to. If this is not found, the
program takes the path of the working copy as the source repository. In this
case, any version tag is ignored.

Here is an example of the generated data
in `JSON <http://www.json.org>`_ format::

  {
     "repos": {
        "/srv/csr/Epics/R3.14.10/base/3-14-10-0-1": {
            "tag": "R3-14-10-0-1",
            "type": "darcs",
            "url": "rcsadm@aragon.acc.bessy.de:/opt/repositories/controls/darcs/epics/base/3-14-10"
        },
        "/srv/csr/Epics/R3.14.12/base/3-14-12-2-1": {
            "type": "darcs",
            "url": "rcsadm@aragon.acc.bessy.de:/opt/repositories/controls/darcs/epics/base/3-14-12-2"
        },
        "/srv/csr/Epics/R3.14.8/support/apps/wlsSupport/work": {
            "type": "path",
            "url": "rcsadm@aragon.acc.bessy.de:/opt/Epics/R3.14.8/support/apps/wlsSupport/work"
        },
        "/srv/csr/Epics/R3.14.8/support/NewDyncon/3-0": {
            "tag": "R3-0",
            "type": "darcs",
            "url": "rcsadm@aragon.acc.bessy.de:/opt/repositories/controls/darcs/epics/support/dyncon"
        },
        "/srv/csr/Epics/R3.14.8/support/NewDyncon/3-1": {
            "tag": "R3-1",
            "type": "darcs",
            "url": "rcsadm@aragon.acc.bessy.de:/opt/repositories/controls/darcs/epics/support/dyncon"
        }
      }
  }

Optional 

Optional Phase IV, name to paths map
++++++++++++++++++++++++++++++++++++

This optional phase that is started with the command "name2paths" creates a map
that shows what paths were found for modules. Here is an example of the created
datastructure in `JSON <http://www.json.org>`_ format::

  {
      "name2paths": {
          "ALARM": [
              "/srv/csr/Epics/R3.14.8/support/alarm/3-2",
              "/srv/csr/Epics/R3.14.8/support/alarm/3-3",
              "/srv/csr/Epics/R3.14.8/support/alarm/3-5"
          ],
          "MOTOR": [
              "/srv/csr/Epics/R3.14.8/support/motor/6-4-4-1",
              "/srv/csr/Epics/R3.14.8/support/motor/6-5-1",
              "/srv/csr/Epics/R3.14.8/support/motor/6-5-2",
              "/srv/csr/Epics/R3.14.8/support/synApps/5-1-1-0/support/motor/5-9",
              "/srv/csr/Epics/R3.14.8/support/synApps/5-2-0-1/support/motor/6-1",
              "/srv/csr/Epics/R3.14.8/support/synApps/5-2-0/support/motor/6-1",
              "/srv/csr/Epics/R3.14.8/support/synApps/5-4-1/support/motor/6-4-3",
          ],
      }
  }

Optional Phase V, paths to names map
++++++++++++++++++++++++++++++++++++

This optional phase that is started with the command "path2names" creates a map
that shows what module names were used for what module paths. Here is an
example of the created datastructure in `JSON <http://www.json.org>`_ format::

  {
      "path2names": {
          "/srv/csr/Epics/R3.14.8/support/alarm/3-0": [
              "ALARM"
          ],
          "/srv/csr/Epics/R3.14.8/support/alarm/3-1": [
              "ALARM"
          ],
          "/srv/csr/Epics/R3.14.8/support/alarm/3-2": [
              "ALARM"
          ],
          "/srv/csr/Epics/R3.14.8/support/synApps/5-2-0-1/support/genSub/1-6a": [
              "GENSUB",
              "GEN_SUB"
          ],
      }
  }

Program output
++++++++++++++

The output of all phases that are run is combined in a single 
`JSON <http://www.json.org>`_ datastructure that is printed on the console.

From the paths of each RELEASE file, a module name is constructed. Each path of
a support module from a RELEASE is added to the list of dependencies of that
module.

Since all the consecutive calls of "make" may take some time, the results of
the RELEASE file scan can be saved as a file and used later on with other
commands like "path2names" or "groups". This is the meaning of the ``-i`` or
``--info-file`` option.

Commands
--------

This is a list of all commands. Note that if no command is provided, the
program assumes command "all". This is the command you want to use in most
cases.

config list
+++++++++++

List all configuration files that were loaded.

config show [OPTIONNAMES]
+++++++++++++++++++++++++

Show the configuration in JSON format.  OPTIONNAMES is an optional list of long
option names. If OPTIONNAMES are specified, only options from this list are
saved in the configuration file.

config make FILENAME [OPTIONNAMES]
++++++++++++++++++++++++++++++++++

Create a new configuration file from the options read from configuration files
and options from the command line. If FILENAME is '-' dump to the console.
OPTIONNAMES is an optional list of long option names. If OPTIONNAMES are
specified, only options from this list are saved in the configuration file.

all
+++

This is the most important command. "all" combines the commands "deps",
"groups" and "repos". The output of the commands is combined in a single large
`JSON <http://www.json.org>`_ structure and printed to the console. You can use
the output of this command as input for :doc:`sumo db <reference-sumo>` in
order to create a dependency database.

deps
++++

This command collects dependencies from all "RELEASE" files and returns the
structure in `JSON <http://www.json.org>`_ format. For details see 
`Phase I, RELEASE file scanning`_.

groups
++++++

This command collects modules of the same name but of different versions in
groups. For details see `Phase II, Grouping`_.

repos
+++++

This command collects information about repositories and returns the structure
in `JSON <http://www.json.org>`_ format. For details see 
`Phase III, repository scan`_.

name2paths
++++++++++

This command shows what module paths were found for module names. You do not
need this command in order to generate a dependency database. For details see
`Optional Phase IV, name to paths map`_.


path2names
++++++++++

This command shows what module names were used for what module paths. You do not
need this command in order to generate a dependency database. For details see
`Optional Phase V, paths to names map`_.

.. _reference-sumo-scan-Options:

Options
-------

Here is a short overview on command line options:

``--version``
    show program's version number and exit
``-h, --help``
    show this help message and exit
``--summary``
    Print a summary of the function of the program.
``--test``
    Perform some self tests.
``-c FILE, --config FILE``
    Load options from the given configuration file. You can specify more than
    one of these.  Unless --no-default-config is given, the program always
    loads configuration files from several standard directories first before it
    loads your configuration file. The contents of all configuration files are
    merged.
``-C, --no-default-config``
    If this option is given the program doesn't load the default configuration.
``--disable-loading``
    If given, disable execution of load commands like '#preload' in
    configuration files. In this case these keys are treated like ordinary
    keys.
``-A``, ``--append OPTIONNAME``
    If an option with name OPTIONNAME is given here and it is a list option,
    the list from the command line is *appended* to the list from the
    configuration file. The default is that options from the command line
    *override* option values from the configuration file.
``--#preload FILES`` 
    Specify a an '#preload' directive in the configuration file. This option
    has only a meaning if a configuration file is created with the 'makeconfig'
    command. '#preload' means that the following file(s) are loaded before the
    rest of the configuration file.
``--#opt-preload FILES`` 
    This option does the same as --#preload but the file loading is optional.
    If they do not exist the program continues without an error.
``--#postload FILES`` 
    Specify a an '#postload' directive in the configuration file. This option
    has only a meaning if a configuration file is created with the 'makeconfig'
    command. '#postload' means that the following file(s) are loaded after the
    rest of the configuration file.
``--#opt-postload FILES`` 
    This option does the same as --#postload but the file loading is optional.
    If they do not exist the program continues without an error.
``-d DIR, --dir DIR``
    Parse all RELEASE files in directory DIR. You can specify more than one of
    these by repeating this option or by joining values in a single string
    separated by spaces. A default for this option can be put in a
    configuration file.
``-i INFOFILE, --info-file INFOFILE``
    Read information from INFOFILE. This is a scan file generated by this
    script in a prevous run.
``-N NAME, --ignore-name NAME``
    Define names of variables in RELEASE files that should be ignored. You
    usually want to ignore the names like 'TOP' or 'SUPPORT'. You can specify
    more than one of these by repeating this option or by joining values in a
    single string separated by spaces. A default for this option can be put in
    a configuration file. If this option isn't provided, the program uses these
    defaults: TOP EPICS_SUPPORT SUPPORT MSI TEMPLATE_TOP
``-g DIR, --group-basedir DIR``
    Option "-g" or "--group-basedir" must be followed by a directory name. It
    defines the part of the directory path that is the same for all support
    modules. This is needed in order to generate a module name from the
    module's directory path.  You can specify more than one of these by
    repeating this option or by joining values in a single string separated by
    spaces. A default for this option can be put in a configuration file.
    Directories (option --dir) are always appended to the list of
    group-basedirs.
``--exclude-path REGEXP``
    Exclude all paths that match REGEXP from dependencies.  You can specify
    more than one of these by repeating this option or by joining values in a
    single string separated by spaces. A default for this option can be put in
    a configuration file.
``--exclude-deps REGEXP``
    Exclude all paths whose dependencies match REGEXP. A default for this
    option can be put in a configuration file.
``--ignore-changes REGEXP``
    Ignore all uncomitted changes in files that match the REGEXP. Usually
    uncomitted changes mean that we cannot use the repository as such but must
    copy the whole directory (source type is always 'path'). A common
    application for this option is to ignore changes in 'configure/RELEASE'.
    You can specify more than one of these by repeating this option or by
    joining values in a single string separated by spaces. A default for this
    option can be put in a configuration file.
``-D EXPRESSION, --dir-patch EXPRESSION``
    Specify a directory patchexpression. Such an expression consists of a tuple
    of 2 python strings. The first is the match expression, the second one is
    the replacement string. The regular expression is applied to every source
    path generated. You can specify more than one patchexpression. A default
    for this option can be put in a configuration file.
``-U EXPRESSION, --url-patch EXPRESSION``
    Specify a repository url patchexpression. Such an expression consists of a
    tuple of 2 python strings. The first is the match expression, the second
    one is the replacement string. The regular expression is applied to every
    source url generated. You can specify more than one patchexpression. A
    default for this option can be put in a configuration file.
``--hint HINT``
    Specify a HINT. A HINT has the form REGEXP,FLAG{,FLAG}.  REGEXP is a
    regular expression that is matched with the module path. FLAG is a string
    that gives hints how to treat that module.  You can specify more than one
    hint. Currently known FLAGS are "path" and "tagless". A default for this
    option can be put in a configuration file.
``--missing-tag``
    Show directories where a repository was found but no tag. A default for
    this option can be put in a configuration file.
``--missing-repo``
    Show directories where no repository was found. A default for this option
    can be put in a configuration file.
``-t BUILDTAG, --buildtag BUILDTAG``
    Scan only directories of the given buildtag.
``-p, --progress``
    Show progress on stderr. A default for this option can be put in a
    configuration file.
``-t, --trace``
    Switch on some trace messages.
``--exceptions``
    On fatal errors that raise python exceptions, don't catch these. This will
    show a python stacktrace instead of an error message and may be useful for
    debugging the program."
``-v, --verbose``
    Show command calls. A default for this option can be put in a
    configuration file
``-n, --dry-run``
    Just show what the program would do.

