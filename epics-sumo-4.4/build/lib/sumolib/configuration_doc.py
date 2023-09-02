text=\
{
'_order': ['Configuration Files'],
'Configuration Files': r"""
Configuration Files
===================

The philosphy
-------------

In sumo all parameters for a command are given with command line
options and arguments. Configuration files are files that have
defaults for command line options.

All command line options start with a dash "-". Short command line
options have the form "-<char>", long command line options have the
form "--<string>".

All command line options have a long form, some also have a short
form.

Some command line options take no argument, some options require an
argument. Some command line options may be given more than once with
an argument, they are used to define lists of values.

The configuration file defines a map where keys are names of long
command line options and values are booleans, strings or lists of
strings. Only some of the command line options can be put in a
configuration file.

For sumo-scan you find a list of these at "Keys in the sumo-scan
configuration file".

For sumo you find a list of these at "Keys in the sumo configuration
file".

File format
-----------

A configuration file is always in JSON <http://www.json.org> format.
Each key is the long name of a command line option, each value is a
boolean, a string or a list of strings.

Here is an example of such a file:

  {
      "dbdir": "/opt/Epics/sumo/database",
      "makeflags": [
          "-s"
      ],
      "builddir": "/opt/Epics/sumo/build"
  }

Environment variable expansion
------------------------------

A few keys in the configuration file of sumo have environment variable
expansion. This means that strings of the form $VARNAME are
substituted with the value of environment variable VARNAME if it
exists. If you want to use the string $VARNAME literally, precede it
with a backslash like in \$VARNAME. The list "Keys in the sumo
configuration file" shows you which keys have environment variable
expansion.


Using more than one configuration file
--------------------------------------

Sumo can read more than just one configuration file, in this case the
data is *merged*.

The files are read one by one and their keys and values are combined
in the in the following way:

Keys not yet defined are simply added. For keys that already exist and
whose values are not lists, the last value overwrites the first one.
For keys that already exist and whose values are lists, the lists are
concatenated.

Default paths
-------------


Sumo reads and merges configuration files from various places, which
ones depends on your environment variable settings and command line
options.

First the program tries to read the file sumo.config from a list of
default paths. The list of default paths can be set by the environment
variable SUMOCONFIG which must be a colon (on Unix systems) or
semicolon (on Windows systems) separated list of paths.

If SUMOCONFIG *is not set*, these are the predefined default paths:

- /etc
- [python-libdir]/sumolib
- $HOME
- your current working directory

Note the sumo reads *all* the configuration files it finds, not just
the first one.

If you use the --no-default-config command line option, the list of
default paths is made empty.

The config option
-----------------

After configuration files from default paths were read the program
continues with all configuration files specified by the -c or --config
option.

Load commands in configuration files
------------------------------------


In a configuration file you can specify names of other configuration
files that must or may be loaded. These files are merged as described
above.

There are 4 special keys in the configuration file that are used to
specify other files:

#preload [file list]
  Load files *before* all other definitions

#opt-preload [file list]
  Load files *before* all other definitions, if they exist.

#postload [file list]
  Load files *after* all other definitions

#opt-postload [file list]
  Load files *after* all other definitions, if they exist.

Note that the loaded files can also contain one or more these special
keys.

The configuration file for sumo-scan
------------------------------------

The default name of this file is sumo-scan.config.

Keys in the sumo-scan configuration file
++++++++++++++++++++++++++++++++++++++++

The following keys may be part of a configuration file for sumo-scan:

#preload
  A list of files to *preload*, see Loading other files.

#opt-preload
  A list of optional files to *preload*, see Loading other files.

#postload
  A list of files to *postload*, see Loading other files.

#opt-postload
  A list of optional files to *postload*, see Loading other files.

dir
  A list of directories to parse, for details see sumo-scan options.

exclude-deps
  A list of regular expressions for dependencies to exclude, for
  details see sumo-scan options.

exclude-path
  A list of regular expressions for paths to exclude, for details see
  sumo-scan options.

group-basedir
  A list of existing support directories, for details see sumo-scan
  options.

hint
  A list of conversion hints, for details see sumo-scan options.

ignore-changes
  A list of regular expressions for changes to ignore, for details see
  sumo-scan options.

ignore-name
  A list of names that are ignored in RELEASE files, for details see
  sumo-scan options.

missing-repo
  A boolean flag that controls the printing of warnings, for details
  see sumo-scan options.

missing-tag
  A boolean flag that controls the printing of warnings, for details
  see sumo-scan options.

progress
  A boolean flag that controls the printing of progress markers, for
  details see sumo-scan options.

dir-patch
  A list of directory patch expressions, for details see sumo-scan
  options.

url-patch
  A list of url patch expressions, for details see sumo-scan options.

verbose
  A boolean flag that controls the verbosity level, for details see
  sumo-scan options.

The configuration file for sumo
-------------------------------

The default name of this file is sumo.config.

Keys in the sumo configuration file
+++++++++++++++++++++++++++++++++++

The following keys may be part of a configuration file for sumo:

#opt-postload
  A list of optional files to *postload*, see Loading other files.

#opt-preload
  A list of optional files to *preload*, see Loading other files.

#postload
  A list of files to *postload*, see Loading other files.

#preload
  A list of files to *preload*, see Loading other files.

alias
  A list of module aliases in the form FROM:TO, for details see sumo
  options.

builddir
  The build directory, for details see sumo options. This key has
  "Environment variable expansion".

buildtag-stem
  A string that specifies a buildtag stem, for details see sumo
  options.

dbdir
  The directory where the dependency database file is found for
  details see sumo options. This key has "Environment variable
  expansion".

dbrepo
  The url of the dependency database foreign repository, for details
  see sumo options. This key has "Environment variable expansion".

dbrepomode
  A string that specifies the mode for the dependency database
  repository, for details see sumo options.

dir-patch
  A list of directory patch expressions for the db convert and db
  modconvert commands. For details see sumo options.

editor
  A string that specifies the editor for command sumo db edit, for
  details see sumo options.

extra
  A list of strings that defines extra lines that are put in generated
  RELEASE files, for details see sumo options.

jobs
  Specify the maximum number of jobs in sumo to run simultaneously
  within sumo, for details see sumo options.

localbuilddir
  The local build directory, for details see sumo options. This key
  has "Environment variable expansion".

makeflags
  A list of strings that specify extra options for "make", for details
  see sumo options.

module
  A list of module specifications, for details see sumo options.

no-err-build-exists
  When with build new a build matching the modulespecs already exists,
  just print a warning and terminate without an error. For details see
  sumo options.

progress
  A boolean flag that controls the printing of progress markers, for
  details see sumo options.

readonly
  A boolean flag that sets sumo in read-only mode, for details see
  sumo options.

scandb
  The filename of the scan database, for details see sumo options.

url-patch
  A list of url patch expressions for the db convert and db modconvert
  commands. For details see for details see sumo options.

verbose
  A boolean flag that controls the verbosity level, for details see
  sumo options.

Example of a sumo configuration file
++++++++++++++++++++++++++++++++++++


Here is an example of our global sumo configuration file here at HZB:

  {
      "#opt-preload": [
          "configure/MODULES.HOST",
          "configure/MODULES"
      ],
      "dbdir": "/opt/Epics/sumo/database",
      "dbrepo": "darcs rcsadm@repo.acc.bessy.de:/opt/repositories/cont
      rols/darcs/epics/support/sumo-deps-db",
      "dbrepomode": "push",
      "builddir": "/opt/Epics/sumo/build"
  }

Explanation:

builddir
  This defines the directory where the builds are created and the
  build database file BUILDS.DB resides.
dbdir
  The directory where the dependency database file DEPS.DB is found,
  for details see sumo options.
dbrepo
  This defines that the directory of the dependency database file in
  this example is a darcs repository. You could also use mercurial,
  git, subversion or cvs here. The long string after "darcs" is an
  *URL* that defines the location of the remote darcs repository. We
  use the same value of "dbrepo" on other build hosts in order to keep
  the dependency databases files on all build hosts identical. For
  details on the "dbrepo" string, see sumo option --dbrepo.

dbrepomode
  Mode "push" means that before each read operation on the dependency
  database, sumo performs a "pull" and "merge" command and for all
  write operations it commits all changes and pushes them to the
  central repository.
#opt-preload
  This defines that sumo tries to load "configure/MODULES.HOST" and
  "configure/MODULES" first, if these files exist. In our application
  our definition of used EPICS <http://www.aps.anl.gov/epics> support
  modules is placed in these two files. If we run "sumo build use" in
  the top directory of our application, sumo uses module definitions
  from these two files.

Example of MODULES files
++++++++++++++++++++++++

Module definitions are configuration files where only the keys "alias"
and "module" are defined. These are specific for each EPICS
<http://www.aps.anl.gov/epics> application. Here are examples of
MODULES.HOST and MODULES for our control system application:

MODULES.HOST:

  {
      "alias": [
          "BASE:EPICS_BASE"
      ],
      "module": [
          "BASE:R3-14-12-2-7"
      ]
  }

MODULES:

  {
      "alias": [
          "AGILENT-SUPPORT:AGILENT_SUPPORT",
          "APPS_CRATECTRL:CRATECTRL",
          "APPS_GENERICBOOT:GENERIC_BOOT",
          "APPS_GENERICTEMPLATE:GENERICTEMPLATE",
          "APPS_IOCWATCH:IOCWATCHAPP",
          "APPS_MOTOR:MOTORAPP",
          "APPS_SCOPESAVERESTORE:SCOPE_SAVE_RESTORE",
          "APPS_STREAMTEMPLATESANDPROTOCOLS:STAP",
          "APPS_VACUUM:VACUUMAPP",
          "BESSY_RULES:BESSYRULES",
          "BSPDEP_CPUBOARDINIT:CPU_BOARD_INIT",
          "BSPDEP_ENABLED32:ENABLE_D32",
          "BSPDEP_TIMER:TIMER",
          "CAPUTLOG:CA_PUT_LOG",
          "DEVGPIB:DEV_GPIB",
          "DEVIOCSTATS:IOCSTATS",
          "DISTVERSION:DIST_VERSION",
          "GENSUB:GEN_SUB",
          "HIGHLAND-V375:V375",
          "HIGHLAND-V680:V680",
          "RFM2G-OSI:RFM2G",
          "SEQ:SNCSEQ",
          "STREAMDEVICE:STREAM",
          "VXBOOTPARAMS:VX_BOOT_PARAMS",
          "VXI-11:VXI_11"
      ],
      "module": [
          "AGILENT-SUPPORT:R0-14",
          "AGILENT:R2-3",
          "ALARM:R3-8",
          "APPS_CRATECTRL:R4-1-1",
          "APPS_GENERICBOOT:R0-9",
          "APPS_GENERICTEMPLATE:R3-7",
          "APPS_IOCWATCH:R3-1",
          "APPS_MOTOR:R3-1-3",
          "APPS_SCOPESAVERESTORE:R2-1",
          "APPS_STREAMTEMPLATESANDPROTOCOLS:R2-0",
          "APPS_VACUUM:R1-5-2",
          "ASYN:R4-17-2",
          "AUTOSAVE:R4-8-bessy2",
          "BESSYRULES:R2-15",
          "BINP:R2-5",
          "BSPDEP_CPUBOARDINIT:R4-1",
          "BSPDEP_ENABLED32:R4-2",
          "BSPDEP_TIMER:R6-2",
          "BSPDEP_VMETAS:R2-0",
          "CAPUTLOG:R3-3-2",
          "CSM:R3-7",
          "DEVGPIB:R2-2-0",
          "DEVIOCSTATS:R3-1-9-bessy3",
          "DEVLIB2:R2-3-1",
          "DISTVERSION:R2-2",
          "DYNCON:R3-2",
          "EK:R2-2",
          "ESD:R2-1",
          "GENSUB:R1-6-1",
          "HIGHLAND_V375:R1-2-3",
          "HIGHLAND_V680:R1-3",
          "HIGHLAND_V850:R2-3-2",
          "MCAN:R2-6-3-2",
          "MISC_DBC:R3-0",
          "MISC_DEBUGMSG:R3-0",
          "MOTOR:R6-5-2-2",
          "MUXV:R2-3",
          "RFM2G-OSI:R1-2",
          "SEQ:R2-1-16",
          "SOFT_DEVHWCLIENT:R3-0",
          "STD:R2-8-bessy2",
          "STREAMDEVICE:R2-4-0-4",
          "TDU:R4-2",
          "TOOLS_DBOPT:R0-4",
          "TOOLS_MSI:R1-5-bessy3",
          "VCT6:R2-3",
          "VPDU:R2-3",
          "VXBOOTPARAMS:R2-3",
          "VXI-11:R3-0",
          "WAVEPROC:R1-0-1"
      ]
  }
""",
}
