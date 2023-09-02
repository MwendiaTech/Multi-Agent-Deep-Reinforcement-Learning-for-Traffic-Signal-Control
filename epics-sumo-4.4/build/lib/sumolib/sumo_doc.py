commands=\
{
'_order': ['maincommands', 'subcommands for maincommand "config"', 'subcommands for maincommand "db"', 'subcommands for maincommand "build"'],
'maincommands': {
'_order': ['help COMMAND', 'config SUBCOMMAND', 'lock FILE', 'unlock FILE', 'db SUBCOMMAND', 'build SUBCOMMAND'],
"": r"""
maincommands
++++++++++++

""",
'help COMMAND': r"""
help COMMAND
::::::::::::

This command prints help for the given command. It can be invoked as:

  help
  help MAINCOMMAND
  help SUBCOMMAND
  help MAINCOMMAND SUBCOMMAND

You get a list of all known MAINCOMMANDS with:

  help maincommand
""",
'config SUBCOMMAND': r"""
config SUBCOMMAND
:::::::::::::::::

Show the configuration or create or modify a configuration file. These
are known subcommands here:

- list       - list loaded configuration files
- local      - create configuration for "local" builds
- make       - create configuration file
- new        - create a new configuration file from one of the
  provided templates
- show       - show configuration data
- standalone - create configuration for "standalone" builds

You get help on each subcommand with:

  help SUBCOMMAND
""",
'lock FILE': r"""
lock FILE
:::::::::

Lock a FILE, then exit sumo. This is useful if you want to read or
write a database file without sumo interfering. Don't forget to remove
the lock later with the "unlock" command.

This command must be followed by a *filename*.
""",
'unlock FILE': r"""
unlock FILE
:::::::::::

Unlock a FILE, then exit sumo. If you locked a database with "lock"
before you should always unlock it later, otherwise sumo can't access
the file.

This command must be followed by a *filename*.
""",
'db SUBCOMMAND': r"""
db SUBCOMMAND
:::::::::::::

This is the maincommand for all operations that work with the
dependency database or DEPS.DB file.

For all of the db subcommands you have to specify the dependency
database directory with option --dbdir or a configuration file.

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

You get help on each subcommand with:

  help SUBCOMMAND
""",
'build SUBCOMMAND': r"""
build SUBCOMMAND
::::::::::::::::

This is the maincommand for all operations that work with builds and
the build database (BUILDS.DB).

For all of the build subcommands you have to specify the dependency
database directory and the build directory with --dbdir and --builddir
or a configuration file.

These are the known subcommands:

delete
  delete a build

find
  look for builds that match a module specification

getmodules
  From a missing or incomplete module specification create a valid
  module specification from an existing build.

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

You get help on each subcommand with:

  help SUBCOMMAND
""",
},
'subcommands for maincommand "config"': {
'_order': ['config list', 'config local DIRECTORY', 'config make FILENAME [OPTIONNAMES]', 'config new DIRECTORY TEMPLATE', 'config show [OPTIONNAMES]', 'config standalone DIRECTORY'],
"": r"""
subcommands for maincommand "config"
++++++++++++++++++++++++++++++++++++

""",
'config list': r"""
config list
:::::::::::

List all configuration files that were loaded.
""",
'config local DIRECTORY': r"""
config local DIRECTORY
::::::::::::::::::::::

This command is used to create a new sumo directory with a new build
directory but using existing builds from your current build directory.
It also creates an independent copy of the dependency database.

DIRECTORY is created if it does not yet exist. This command takes all
settings and command line options but sets dbrepomode to "pull" and
dbdir to DIRECTORY/database. It also sets localbuilddir to
DIRECTORY/build. Option dbrepo must be set, this is used to create a
local copy of the dependency database in DIRECTORY/database. If there
is a file "sumo.config" in the current working directory it is copied
to "sumo.config.bak". A new file "sumo.config" is then created in the
current working directory.

""",
'config make FILENAME [OPTIONNAMES]': r"""
config make FILENAME [OPTIONNAMES]
::::::::::::::::::::::::::::::::::

Create a new configuration file from the options read from
configuration files and options from the command line. If FILENAME is
'-' dump to the console. OPTIONNAMES is an optional list of long
option names. If OPTIONNAMES are specified, only options from this
list are saved in the configuration file.

If this command is provided with option --getmodules BUILDTAG, module
specifications are updated from the specified build. This works like
the command "build getmodules.

Here are two examples how to use this option:

If configure/MODULES does not yet exist, create a matching MODULES
file for build 'AUTO-004' for an application:

  sumo config make configure/MODULES alias module --getmodules
  AUTO-004

If configure/MODULES already exists (and is automatically loaded, see
also sumo.config examples), update versions in MODULES file from the
versions used in build 'AUTO-004':

  sumo config make configure/MODULES alias module --getmodules
  AUTO-004

""",
'config new DIRECTORY TEMPLATE': r"""
config new DIRECTORY TEMPLATE
:::::::::::::::::::::::::::::

This command is used to create a new sumo directory with a new build
directory and a new dependency database.

It creates a new configuration for sumo. DIRECTORY must not yet exist
and is created by this command. This command takes all settings and
command line options but sets dbdir to DIRECTORY/database. It also
sets builddir to DIRECTORY/build. TEMPLATE determines how the
dependency database file is created. Currently 2 values are known:

empty
  Create an empty dependency database.

github
  Create a sample dependency database file with some entries for EPICS
  base, ASYN, STREAMDEVICE, AREADETECTOR, SEQUENCER and more. In this
  sample all module repositories are fetched from the internet, mostly
  github.

If there is a file "sumo.config" in the current working directory it
is copied to "sumo.config.bak". A new file "sumo.config" is then
created in the current working directory.

""",
'config show [OPTIONNAMES]': r"""
config show [OPTIONNAMES]
:::::::::::::::::::::::::

Show the configuration in JSON format.  OPTIONNAMES is an optional
list of long option names. If OPTIONNAMES are specified, only options
from this list are saved in the configuration file.
""",
'config standalone DIRECTORY': r"""
config standalone DIRECTORY
:::::::::::::::::::::::::::

This command is used to create a new sumo directory with an
independent build directory and an independent copy of the dependency
database.

It creates a new configuration for "standalone" builds. DIRECTORY is
created if it does not yet exist. This command takes all settings and
command line options but sets dbrepomode to "pull" and dbdir to
DIRECTORY/database. It also sets builddir to DIRECTORY/build. Option
dbrepo must be set, this is used to create a local copy of the
dependency database in DIRECTORY/database. If there is a file
"sumo.config" in the current working directory it is copied to
"sumo.config.bak". A new file "sumo.config" is then created in the
current working directory.
""",
},
'subcommands for maincommand "db"': {
'_order': ['db alias-add MODULE DEPENDENCY ALIAS', 'db appconvert SCANFILE', 'db check', 'db clonemodule OLD-MODULE NEW-MODULE [VERSIONS]', 'db cloneversion MODULE OLD-VERSION NEW-VERSION [SOURCESPEC]', 'db commands MODULE LINES', 'db convert SCANFILE', 'db dependency-add MODULE DEPENDENCY', 'db dependency-delete MODULE DEPENDENCY', 'db edit', 'db extra MODULE [LINES]', 'db find REGEXP', 'db format', 'db list MODULES', 'db make-recipes MODULE [TARGET] [LINES]', 'db merge DB', 'db modconvert SCANFILE MODULES', 'db releasefilename MODULE RELEASEFILENAME', 'db replaceversion MODULE OLD-VERSION NEW-VERSION', 'db show MODULES', 'db weight WEIGHT MODULES'],
"": r"""
subcommands for maincommand "db"
++++++++++++++++++++++++++++++++
""",
'db alias-add MODULE DEPENDENCY ALIAS': r"""
db alias-add MODULE DEPENDENCY ALIAS
::::::::::::::::::::::::::::::::::::

Define a new alias for a dependency of a module. MODULE here is a
modulespec of the form MODULE:VERSION that specifies a single version
of a module.
""",
'db appconvert SCANFILE': r"""
db appconvert SCANFILE
::::::::::::::::::::::

Convert a scanfile that was created by applying "sumo-scan all" to an
application to a list of aliases and modulespecs in JSON
<http://www.json.org> format. If SCANFILE is a dash "-" the program
expects the scanfile on stdin. The result is printed to the console.
""",
'db check': r"""
db check
::::::::

Do some consistency checks on the dependency database file in the
directory specified by --dbdir.
""",
'db clonemodule OLD-MODULE NEW-MODULE [VERSIONS]': r"""
db clonemodule OLD-MODULE NEW-MODULE [VERSIONS]
:::::::::::::::::::::::::::::::::::::::::::::::

Copy all versions of the existing old module and add this with the
name of thew new module to the dependency database. OLD-MODULE and
NEW-MODULE here are just the module names since the versions may
follow as a separate argument. If there are no versions specified, the
command copies all existing versions. Note that this DOES NOT add the
new module as dependency to any other modules.
""",
'db cloneversion MODULE OLD-VERSION NEW-VERSION [SOURCESPEC]': r"""
db cloneversion MODULE OLD-VERSION NEW-VERSION [SOURCESPEC]
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

This command adds a new version of a module to the dependency database
by copying the old version. MODULE here is just the name of the module
since the version follows as a separate argument.

If SOURCESPEC is not given, the command copies the source
specification from OLD-VERSION but sets the tag to NEW-VERSION. Note
that this is not allowed for "path" and "tar" sources (see below).

If SOURCESPEC is given, the source specification from OLD-VERSION is
copied an the all values from SOURCESPEC are added.

A sourcespec has the form:
  NAME=VALUE[,VALUE...] [NAME=VALUE[,VALUE..] ...]

In general, NAME must start with a letter or underscore character and
must be
following by a sequence of letters, underscores or digits.

A VALUE must be a JSON simple value (no map or list). If VALUE is a
string, it must be enclosed in double quotes '"' if it contains any of
the characters '"', ',' or ' '.

These are possible names:

type
  The source type. Currently known are "path", "tar", "cvs", "svn",
  "darcs", "hg" and "git".

url
  This is the URL. For the types "path" and "tar" it may also be a
  filename.

tag
  This defines the revision tag.

rev
  This defines the revision hash key.

patches
  This defines names or URLs for patch files. This is the only name,
  where several values may be provided as a comma separated list.

commands
  This defines commands that are executed *after* the source code is
  checked out and *before* any patches are applied.

Note that you can define an empty value (on the bash shell) like in
this example:

  tag='""'

This means that the "tag" is removed from the source specification.

The command always asks for a confirmation of the action unless option
"-y" is used.
""",
'db commands MODULE LINES': r"""
db commands MODULE LINES
::::::::::::::::::::::::

Define commands that are executed after a module is checked out. See
also "commands" in the chapter "The dependency database".

MODULE here is a modulespec of the form MODULE:VERSION that specifies
a single version of a module. LINES is a list of space separated
strings. It is recommended to enclose the line strings in single or
double quotes.

Special variables and characters when you use double quotes:

- \": (bash) A literal double quote character.
- $(VAR): (make) Insert value of make or shell variable VAR.
- $$: (make) A dollar character passed to the shell.
- \\$$: (make, bash) A literal dollar character passed to the shell.
- \\: (json, bash) At the end of the json string this means line
  continuation for bash.
""",
'db convert SCANFILE': r"""
db convert SCANFILE
:::::::::::::::::::

Convert a scanfile that was created by by "sumo-scan all" to a new
dependency database.  If SCANFILE is a dash "-", the program expects
the scanfile on stdin.  Note that options --dbdir and --scandb are
mandatory here. With --dbdir you specify the directory where the new
created dependency database file is stored, with --scandb you specify
the name of the scan database file. The scan database file contains
information on what moduleversion can be used with what dependency
version.
""",
'db dependency-add MODULE DEPENDENCY': r"""
db dependency-add MODULE DEPENDENCY
:::::::::::::::::::::::::::::::::::

Add a dependency to a module. MODULE here is a modulespec of the form
MODULE:VERSION that specifies a single version of a module.
""",
'db dependency-delete MODULE DEPENDENCY': r"""
db dependency-delete MODULE DEPENDENCY
::::::::::::::::::::::::::::::::::::::

Delete a dependency of a module. MODULE here is a modulespec of the
form MODULE:VERSION that specifies a single version of a module.

""",
'db edit': r"""
db edit
:::::::

Start the editor specified by option --editor or the environment
variables "VISUAL" or "EDITOR" to edit the dependency database file.
This command first acquires a file-lock on the file, that prevents
other users from accessing the file at the same time.  When the editor
program is terminated, sumo checks if the file is still a valid JSON
<http://www.json.org> file. If not, you can start the editor again or
abort the program. If the file is valid JSON <http://www.json.org>,
sumo commits the changes if option --dbrepo was specified.  If option
--logmsg was given, this is used as commit log message, otherwise an
editor is started where you can enter a log message. Finally the file
lock is released. If you want to edit the dependency database file you
should always do it with this command.

""",
'db extra MODULE [LINES]': r"""
db extra MODULE [LINES]
:::::::::::::::::::::::

Define extra lines that are appended to the generated RELEASE file of
the module. See also "extra" in the chapter "The dependency database"
of the documentation.

MODULE here is a modulespec of the form MODULE:VERSION that specifies
a single version of a module.
""",
'db find REGEXP': r"""
db find REGEXP
::::::::::::::

This command shows all modules whose names or sources match a regexp.
Parameter REGEXP is a perl compatible regular expression.
""",
'db format': r"""
db format
:::::::::

Just load and save the dependency database. This ensures that the file
is formatted in the standard sumo format. This is useful when the file
was edited and you want to ensure that key sort order and indentation
are restored. If you specified a repository with --dbrepo, the command
will commit the changes. If you want a log message different from "db
format" use option --logmsg

""",
'db list MODULES': r"""
db list MODULES
:::::::::::::::

If called with no argument, list the names of all modules. If called
with '.', the wildcard symbol, list all versions of all modules. If
called with argument MODULES, a list of modulespecs MODULE:{+-}VERSION
that specifies modules and versions, list all the matching versions of
all specified modules.

""",
'db make-recipes MODULE [TARGET] [LINES]': r"""
db make-recipes MODULE [TARGET] [LINES]
:::::::::::::::::::::::::::::::::::::::

Define special make recipes for a module. See also "make-recipes" in
the chapter "The dependency database" of the documentation.

MODULE here is a modulespec of the form MODULE:VERSION that specifies
a single version of a module.

If TARGET is given, it must be "all", "clean", "config" or "distclean"
and specifies the make target for which a recipe is defined. LINES is
a list of space separated strings. It is recommended to enclose the
line strings in single or double quotes. If LINES is not given, all
special rules for the TARGET are removed.

If TARGET (and LINES) are not given, this defines *empty* make
recipes. This has to be done for modules that have no makefile at all.
These modules are only checked out by sumo, and possibly configured
(see also "commands").

Special variables and characters when you enclose LINES in double
quotes:

- $DIR: (sumo) The directory of the MODULE.
- \": (bash) A literal double quote character.
- $(VAR): (make) Insert value of make or shell variable VAR.
- $$: (make) A dollar character passed to the shell.
- \\$$: (make, bash) A literal dollar character passed to the shell.
- \\: (json, bash) At the end of the json string this means line
  continuation for bash.
""",
'db merge DB': r"""
db merge DB
:::::::::::

Merge the given dependency database file with the dependency database
in the directory specified by --dbdir. Sections that do not exist in
the original dependency database are added. Contradicting sections are
treated as an error and abort the program. If a module has an "extra"
section, only *new* lines are appended to the existing "extra"
section. This avoids having the same line several times in "extra"
after a merge operation.
""",
'db modconvert SCANFILE MODULES': r"""
db modconvert SCANFILE MODULES
::::::::::::::::::::::::::::::

Convert a scanfile that was created by applying "sumo-scan all" to the
dependency database format for all the selected modules. If SCANFILE
is a dash "-" the program expects the scanfile on stdin.  The result
is printed to the console. This data can be added to the dependency
database using the command "db edit".
""",
'db releasefilename MODULE RELEASEFILENAME': r"""
db releasefilename MODULE RELEASEFILENAME
:::::::::::::::::::::::::::::::::::::::::

This command defines an alternative filename for the RELEASE file of
the module. Usually the RELEASE file is generated as
"configure/RELEASE". You can specify a different filename for the
given module with this command. This may be useful for support modules
that have no regular EPICS makefile system or for some special
configurations of the EPICS base. If you set the RELEASEFILENAME to an
empty string or "configure/RELEASE", the special entry for the
filename is removed for this module in the dependency database.
""",
'db replaceversion MODULE OLD-VERSION NEW-VERSION': r"""
db replaceversion MODULE OLD-VERSION NEW-VERSION
::::::::::::::::::::::::::::::::::::::::::::::::

This command replaces a version of a module with a new version. MODULE
here is just the name of the module since the version follows as a
separate argument. All the data of the module is copied. If sourcespec
is given, the command changes the source part according to this
parameter. A sourcespec has the form "path PATH", "tar TARFILE",
"REPOTYPE URL" or "REPOTYPE URL TAG".  REPOTYPE may be "darcs", "hg"
or "git". Both, URL or TAG may be ".", in this case the original URL
or TAG remains unchanged.

""",
'db show MODULES': r"""
db show MODULES
:::::::::::::::

This command prints only the parts of the dependency database that
contain the given modules.

Parameter MODULES is a list of modulespecs MODULE:{+-}VERSION that
specifies the modules and versions to operate on.
""",
'db weight WEIGHT MODULES': r"""
db weight WEIGHT MODULES
::::::::::::::::::::::::

Set the weight factor for modules. A weight determines where a module
is placed in the generated RELEASE file. Modules there are sorted
first by weight, then by dependency. Parameter MODULES is a list of
modulespecs. Use modulename:{+-}versionname to select more versions of
a module.

Note that this command *does not* use the --modules command line
option.

Parameter WEIGHT must be an integer.
""",
},
'subcommands for maincommand "build"': {
'_order': ['build delete BUILDTAGS', 'build find MODULES', 'build getmodules BUILDTAG [MODULES]', 'build list', 'build new MODULES', 'build remake BUILDTAG', 'build show BUILDTAG', 'build showmodules [BUILDTAG]', 'build showdependencies [BUILDTAG]', 'build showdependents [BUILDTAG]', 'build state BUILDTAG [NEW-STATE]', 'build try MODULES', 'build use MODULES'],
"": r"""
subcommands for maincommand "build"
+++++++++++++++++++++++++++++++++++
""",
'build delete BUILDTAGS': r"""
build delete BUILDTAGS
::::::::::::::::::::::

The directories of the builds are removed and their entries in the
build database are deleted. If other builds depend on the builds to be
deleted, the command fails unless option '--recursive' is given. In
this case all dependent builds are deleted, too.  The buildtags must
be given as an argument.
""",
'build find MODULES': r"""
build find MODULES
::::::::::::::::::

This command is used to find matching builds for a given list of
modulespecs. Each module in MODULES here is a modulespec of the form
MODULE or MODULE:{+-}VERSION that specifies just a module name, a
module and some versions or a single version. For details on
modulespecs see Module Specifications .

With option --brief the command just prints buildtags of matching
builds.

Otherwise each buildtag is followed by a list of flags and module
names. Each flag indicates whether the module was found with a
matching version, if it was found with a wrong version or if it is
missing in the build.

If option --all-builds is given, builds whose state is not 'stable' or
'testing' are also shown.

Options --sort-build-dependencies-first and --sort-build-dependencies-
last can be used to change the order reported builds. Without these
options, builds are sorted by *match rank*. Builds that have more
modules with matching versions are placed first, followed by the ones
with more wrong versions followed by the ones with more missing
versions.

Option --detail determines, what is shown. This must be an integer
between 0 and 2. With 0, the default, only builds with matching module
versions are shown. With 1, also builds with wrong versions are shown
and with 2 even builds with missing modules are shown.

This is the meaning of the *flags* in the output of this command:

- ==: The module version matches exactly.
- =~: The module version matches the module specification.
- !=: The module has the wrong version.
- -: The module is missing in the build.

Here is an example:

  $ sumo build find MCAN ALARM:R3-7 --detail 1:
  MYAPP-002
      == ALARM:R3-7
      =~ MCAN:R2-6-3-gp
  MYAPP-001
      != ALARM:R3-8-modified
      =~ MCAN:R2-6-3-gp

We wanted *any* version of `MCAN` and version `R3-7` of `ALARM`. The
command found two builds, `MYAPP-002` and `MYAPP-001`.

In `MYAPP-002`, `ALARM` matches exactly the version we wanted, `MCAN`
matches our specification since we didn't define a version.

In `MYAPP-001`, `ALARM` has not the version we specified, but this
build is reported anyway since we used --detail 1. `MCAN` matches our
specification since we didn't define a version.

Finally, if the command sumo build use doesn't find a build for your
module specifications, you may want to run sumo build find --detail 1
or sumo build find --detail 2. This may help you finding errors in
your module specification in file `configure/MODULES`.

""",
'build getmodules BUILDTAG [MODULES]': r"""
build getmodules BUILDTAG [MODULES]
:::::::::::::::::::::::::::::::::::

This command shows the modules in the form MODULE:VERSION of a build.

The buildtag is mandatory.

   Sumo doesn't distinguish between modules defined on the command
   line or in configuration files like `configure/MODULES`. If modules
   *are somewhere* defined, they will be used by this command.

If modules are specified, only these modules and their dependent
modules with the versions from the specified build are shown. If the
build doesn't contain all the requested modules, sumo stops with an
error message.

With option --lines for each build the output is a single line instead
of a number of indented lines. In this case, the output is compatible
with the -m option of sumo.

Here are some applications for this, please look also at :ref:`"config
make <reference-config-make>` with option --getmodules which does the
same:

If configure/MODULES does not yet exist, create a matching MODULES
file for build 'AUTO-004' for an application:

  sumo config make configure/MODULES alias module -m "$(sumo build
  getmodules AUTO-004 --lines)"

If configure/MODULES already exists (and is automatically loaded, see
also sumo.config examples), update versions in MODULES file from the
versions used in build 'AUTO-004':

  sumo config make configure/MODULES alias module -m "$(sumo build
  getmodules AUTO-004 --lines)"

""",
'build list': r"""
build list
::::::::::

This command lists the names of all builds. Options --sort-build-
dependencies-first and --sort-build-dependencies-last can be used to
change the order of the builds shown. The command shows only builds
with state 'stable' or 'testing' unless option --all-builds is
provided.

""",
'build new MODULES': r"""
build new MODULES
:::::::::::::::::

This command creates a new build. Each module given in MODULES here is
a modulespec of the form MODULE:VERSION that specifies a single
version of a module. If a build for the given modulespecs already
exists, the command aborts with an error message, or terminates with a
warning if option --no-err-build-exists is given.  If the buildtag is
not given as an option, the program generates a buildtag in the form
"AUTO-nnn". A new build is created according to the modulespecs. Your
module specifications must be *complete* and *exact* meaning that all
dependencies are included and all modules are specified with exactly a
single version. Use command "build try" in order to create module
specifications that can be used with command "build new".  This
command calls "make" and, after successful completion, sets the state
of the build to "testing". If you want to skip this step, use option
--no-make. In order to provide arbitrary options to make use option
--makeflags.
""",
'build remake BUILDTAG': r"""
build remake BUILDTAG
:::::::::::::::::::::

This command recreates a build by first calling "make clean" and then
"make all" with the build's makefile. If you develop a support module
(see also "config standalone" and "config local") you want to
recompile the build after changes in the sources. In order to provide
arbitrary options to make use option --makeflags.

""",
'build show BUILDTAG': r"""
build show BUILDTAG
:::::::::::::::::::

This command shows the data of a build. The buildtag must be given as
an argument.
""",
'build showmodules [BUILDTAG]': r"""
build showmodules [BUILDTAG]
::::::::::::::::::::::::::::

This command shows the modules in the form MODULE:VERSION of a build.

The buildtag is optional if modules are also not specified.

Without a buildtag, the command shows the modules for all builds with
state 'stable' or 'testing'. To see all builds regardless of their
state use option --all-builds.

Options --sort-build-dependencies-first and --sort-build-dependencies-
last can be used to change the order reported builds.

With option --lines for each build the output is a single line instead
of a number of indented lines. With -b, the build name is not printed.
If you use --lines and -b, the output is compatible with the -m option
of sumo. Here are some applications for this:

If configure/MODULES does not yet exist, create a matching MODULES
file for build 'AUTO-004' for an application:

  sumo config make configure/MODULES alias module -m "$(sumo build
  showmodules AUTO-004 --lines -b)"

Re-create a complete set of builds from an existing BUILDS.DB on a
different machine:

  [machine 1] $ sumo build showmodules --lines -b --sort-build-
  dependencies-first >  BUILDS.TXT

  [machine 2] $ cat BUILDS.TXT | while read line; do sumo build new -m
  "$line"; done
""",
'build showdependencies [BUILDTAG]': r"""
build showdependencies [BUILDTAG]
:::::::::::::::::::::::::::::::::

This command shows the builds that the given build depends on. The
buildtag is optional, if omitted the command shows the dependencies
for all builds with state 'stable' or 'testing'. To see all builds
regardless of their state use option --all-builds.

Options --sort-build-dependencies-first and --sort-build-dependencies-
last can be used to change the order reported dependencies.

""",
'build showdependents [BUILDTAG]': r"""
build showdependents [BUILDTAG]
:::::::::::::::::::::::::::::::

This command shows all builds that depend on the given build.  The
buildtag is optional, if omitted the command shows the dependents for
all builds with state 'stable' or 'testing'. To see all builds
regardless of their state use option --all-builds.

Options --sort-build-dependencies-first and --sort-build-dependencies-
last can be used to change the order reported dependents.

""",
'build state BUILDTAG [NEW-STATE]': r"""
build state BUILDTAG [NEW-STATE]
::::::::::::::::::::::::::::::::

This command is used to show or change the state of a build. The
buildtag must be given as an argument. If there is no new state given,
it just shows the current state of the build. Otherwise the state of
the build is changed to the given value. If a build is set to state
'disabled', all dependent builds are also set to this state. In this
case, unless option '-y' or '--recursive' are given, sumo asks for
your confirmation.
""",
'build try MODULES': r"""
build try MODULES
:::::::::::::::::

This command is intended to help you create module specifications for
the "build new" command.

Each MODULE here is a modulespec of the form MODULE or
MODULE:{+-}VERSION that specifies just a module name, a module and
some versions or a single version. You can specify an incomplete list
of modules.

The detail of the output is determined by option --detail which is an
integer between 0 and 3. 0, the default, gives the shortest, 3 gives
the longest report. The program then shows which modules you have to

In any case the command shows which modules are missing since they
depend on other modules of your specification and which ones are
missing an exact version.

If you converted an existing support directory to sumo you have a scan
database file which you can specify with option --scandb to this
command.

For a detailed example see try example.

""",
'build use MODULES': r"""
build use MODULES
:::::::::::::::::

This command creates a configure/RELEASE file for an application. Each
module given in MODULES here is a modulespec of the form
MODULE:VERSION that specifies a single version of a module. If option
--buildtag is given, it checks if this is compatible with the given
modules.  Otherwise it looks for all builds that have the modules in
the required versions. If more than one matching build found it takes
the one with the alphabetically first buildtag. The RELEASE file
created includes only the modules that are specified. Output to
another file or the console can be specified with option '-o'.

If no build is found you may:

- Look if you module specification has an error by looking for
  *almost* matching builds with:

  - sumo build find --detail 1 - sumo build find --detail 2

- Create a build matching your module specification with:

  - sumo build new

""",
},
}
completion=\
{
'_order': ['Command completion'],
'Command completion': r"""
Command completion
------------------

Command completion means that you can press <TAB> on any incomplete
sumo command and you get a list of possibilities how to complete that
command. By pressing <TAB> several times you can try each possible
completion.

Prerequisites
+++++++++++++

Command completion works with `bash` or `zsh` (Z-Shell), you need to
have one of these installed. Your environment variable `SHELL` must be
set to the binary file of the shell, e.g. `/usr/bin/bash` or
`/usr/bin/zsh`.

In any case the package `bash-completion` must be installed.

If you use the Z-Shell, the following commands must be executed at
start up. Add them for example to the file `$HOME/.zshenv`:

  autoload -U +X compinit && compinit
  autoload -U +X bashcompinit && bashcompinit

There are two ways to activate command completion, described in the
following chapters.

Activate command completion on the fly
++++++++++++++++++++++++++++++++++++++

Enter this command:

  eval `sumo help completion-line`

Activate command completion permanently
+++++++++++++++++++++++++++++++++++++++

Enter this command:

  sumo help completion-script > $HOME/_sumo

Then add the line:

  source $HOME/_sumo

to your $HOME/.bashrc or $HOME/.zshrc

Completion cache files
++++++++++++++++++++++

Sumo will create cache files in your home directory to speed up
command completion. These are the files ".dbcache.sumo" and
".buildcache.sumo". If you don't want this set the environment
variable "SUMOHELP" in a way that it contains the string "nocache"
like in:

  export SUMOHELP="nocache"

If there are other help options defined in SUMOHELP, you should
separate them with commas ",".
""",
}
pager=\
{
'_order': ['The help pager'],
'The help pager': r"""
The help pager
--------------

The build in pager allows you to navigate in long help texts that sumo
displays when you use command "help" or option "-h". There are three
modes:

pager:off
  The pager is off, all help is printed directly to the console.

pager:on
  The pager is used only for long help texts (more than 24 lines).

pager:always
  The pager is always used, even for short help texts.

Mode "pager:on" is the default.

You define the pager mode by adding one of the three strings to the
environment variable "SUMOHELP" like in:

    export SUMOHELP="pager:off"

If there are other help options defined in SUMOHELP, you should
separate them with commas ",".
""",
}
options=\
{
'_order': ['Options'],
'Options': {
'_order': ['``--#opt-postload FILES``', '``--#opt-preload FILES``', '``--#postload FILES``', '``--#preload FILES``', '``-a ALIAS, --alias ALIAS``', '``--all-builds``', '``-A, --append OPTIONNAME``', '``-b, --brief``', '``--builddir BUILDDIR``', '``-t BUILDTAG, --buildtag BUILDTAG``', '``--buildtag-stem STEM``', '``-c FILE, --config FILE``', '``--dbdir DBDIR``', '``--dbrepo REPOSITORY``', '``--dbrepomode MODE``', '``--detail NO``', '``-D EXPRESSION, --dir-patch EXPRESSION``', '``--disable-loading``', '``-n, --dry-run``', '``--dump-modules``', '``--dumpdb``', '``--editor EDITOR``', '``--exceptions``', '``-X REGEXP, --exclude-states REGEXP``', '``-x EXTRALINE, --extra EXTRALLINE``', '``--getmodules BUILDTAG``', '``-h [OPTIONS], --help [OPTIONS]``', '``--jobs``', '``--lines``', '``--list``', '``--localbuilddir BUILDDIR``', '``--logmsg LOGMESSAGE``', '``--makeflags MAKEFLAGS``', '``-m MODULE, --module MODULE``', '``--no-checkout``', '``-C, --no-default-config``', '``-N, --no-err-build-exists``', '``--no-make``', '``--noignorecase``', '``--nolock``', '``-o OUTPUTFILE, --output OUTPUTFILE``', '``-p, --progress``', '``--readonly``', '``--recursive``', '``--scandb SCANDB``', '``--sort-build-dependencies-first``', '``--sort-build-dependencies-last``', '``--summary``', '``--test``', '``--trace``', '``--tracemore``', '``-U EXPRESSION, --url-patch EXPRESSION``', '``-v, --verbose``', '``--version``', '``-y, --yes``'],
"": r"""
Options
-------


Here is a short overview on command line options:
""",
'``--#opt-postload FILES``': r"""
--#opt-postload FILES
+++++++++++++++++++++

    This option does the same as --#postload but the file loading is
    optional. If they do not exist the program continues without an
    error.
""",
'``--#opt-preload FILES``': r"""
--#opt-preload FILES
++++++++++++++++++++

    This option does the same as --#preload but the file loading is
    optional. If they do not exist the program continues without an
    error.
""",
'``--#postload FILES``': r"""
--#postload FILES
+++++++++++++++++

    Specify a an '#postload' directive in the configuration file. This
    option has only a meaning if a configuration file is created with
    the 'makeconfig' command. '#postload' means that the following
    file(s) are loaded after the rest of the configuration file.
""",
'``--#preload FILES``': r"""
--#preload FILES
++++++++++++++++

    Specify a an '#preload' directive in the configuration file. This
    option has only a meaning if a configuration file is created with
    the 'makeconfig' command. '#preload' means that the following
    file(s) are loaded before the rest of the configuration file.
""",
'``-a ALIAS, --alias ALIAS``': r"""
-a ALIAS, --alias ALIAS
+++++++++++++++++++++++

    Define an alias for the command 'use'. An alias must have the form
    FROM:TO. The path of module named 'FROM' is put in the generated
    RELEASE file as a variable named 'TO'. You can specify more than
    one of these by repeating this option or by joining values in a
    single string separated by spaces. A default for this option can
    be put in a configuration file.
""",
'``--all-builds``': r"""
--all-builds
++++++++++++

    Some subcommands of 'build' show only information for builds that
    have the states 'stable' or 'testing'. If this option is given,
    the commands show *all* builds regardless of their state.
""",
'``-A, --append OPTIONNAME``': r"""
-A, --append OPTIONNAME
+++++++++++++++++++++++

    If an option with name OPTIONNAME is given here and it is a list
    option, the list from the command line is *appended* to the list
    from the configuration file. The default is that options from the
    command line *override* option values from the configuration file.
""",
'``-b, --brief``': r"""
-b, --brief
+++++++++++

    Create a more brief output for some commands.
""",
'``--builddir BUILDDIR``': r"""
--builddir BUILDDIR
+++++++++++++++++++

    Specify the support directory. If this option is not given take
    the current working directory as support directory. A default for
    this option can be put in a configuration file.
""",
'``-t BUILDTAG, --buildtag BUILDTAG``': r"""
-t BUILDTAG, --buildtag BUILDTAG
++++++++++++++++++++++++++++++++

    Specify a buildtag.
""",
'``--buildtag-stem STEM``': r"""
--buildtag-stem STEM
++++++++++++++++++++

    Specify the stem of a buildtag. This option has only an effect on
    the commands 'build new' and 'build try' if a buildtag is not
    specified. The program generates a new tag in the form 'stem-nnn'
    where 'nnn' is the smallest possible number that ensures that the
    buildtag is unique.
""",
'``-c FILE, --config FILE``': r"""
-c FILE, --config FILE
++++++++++++++++++++++

    Load options from the given configuration file. You can specify
    more than one of these.  Unless --no-default-config is given, the
    program always loads configuration files from several standard
    directories first before it loads your configuration file. The
    contents of all configuration files are merged.

""",
'``--dbdir DBDIR``': r"""
--dbdir DBDIR
+++++++++++++

    Define the directory where the dependency database file 'DEPS.DB'
    is found. A default for this option can be put in a configuration
    file.

""",
'``--dbrepo REPOSITORY``': r"""
--dbrepo REPOSITORY
+++++++++++++++++++

    Define a REPOSITORY for the db file. REPOSITORY must have the form
    'REPOTYPE URL' or 'type=REPOTYPE url=URL". REPOTYPE may be
    'darcs', 'hg', 'git', 'svn' or 'cvs'. Option --dbdir. must specify
    a directory that will contain the repository for the db file. What
    repository operations sumo performs when it reads or writes the db
    file depends on option --dbrepomode. A default for this option can
    be put in a configuration file.

""",
'``--dbrepomode MODE``': r"""
--dbrepomode MODE
+++++++++++++++++

    Specify how sumo should use the dependency database repository.
    There are three possible values: 'get', 'pull' and 'push'. Mode
    'get' is the default. The meaning depends on the used version
    control system (VCS), if it is distributed (git,mercurial,darcs)
    or centralized (subversion,cvs). There are three possible
    operations on the dependency database:

      * init : create the dependency database if it doesn't exist *
      read : read the dependency database * write: write (change) the
      dependency database

    Here is what happens during these operations depending on the
    mode:

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
""",
'``--detail NO``': r"""
--detail NO
+++++++++++

    Control the output of command 'try'. The value must be an integer
    between 0 (very short) and 3 (very long)."
""",
'``-D EXPRESSION, --dir-patch EXPRESSION``': r"""
-D EXPRESSION, --dir-patch EXPRESSION
+++++++++++++++++++++++++++++++++++++

    This option is used for commands db convert and db modconvert. It
    specifies a directory patchexpression. Such an expression consists
    of a tuple of 2 python strings. The first is the match expression,
    the second one is the replacement string. The regular expression
    is applied to every source path generated. You can specify more
    than one patchexpression. A default for this option can be put in
    a configuration file.

""",
'``--disable-loading``': r"""
--disable-loading
+++++++++++++++++

    If given, disable execution of load commands like '#preload' in
    configuration files. In this case these keys are treated like
    ordinary keys.
""",
'``-n, --dry-run``': r"""
-n, --dry-run
+++++++++++++

    Just show what the program would do.
""",
'``--dump-modules``': r"""
--dump-modules
++++++++++++++

    Dump module specs, then stop the program.
""",
'``--dumpdb``': r"""
--dumpdb
++++++++

    Dump the modified db on the console, currently only for the
    commands "weight", "merge", "cloneversion" and "replaceversion".
""",
'``--editor EDITOR``': r"""
--editor EDITOR
+++++++++++++++

    Specify the preferred editor. If this is not given, sumo takes the
    name of the editor from environment variables "VISUAL" or EDITOR".
""",
'``--exceptions``': r"""
--exceptions
++++++++++++

    On fatal errors that raise python exceptions, don't catch these.
    This will show a python stacktrace instead of an error message and
    may be useful for debugging the program.
""",
'``-X REGEXP, --exclude-states REGEXP``': r"""
-X REGEXP, --exclude-states REGEXP
++++++++++++++++++++++++++++++++++

    For command 'try' exclude all 'dependents' whose state does match
    one of the regular expressions (REGEXP).
""",
'``-x EXTRALINE, --extra EXTRALLINE``': r"""
-x EXTRALINE, --extra EXTRALLINE
++++++++++++++++++++++++++++++++

    Specify an extra lines that are added to the generated RELEASE
    file. This option can be given more than once to specify more than
    one line. A default for this option can be put in a configuration
    file, there the value must be a list of strings, one for each
    line.
""",
'``--getmodules BUILDTAG``': r"""
--getmodules BUILDTAG
+++++++++++++++++++++

    If this option is used with command `config make` it updates your
    module specifications like the command "build getmodules
    BUILDTAG`. See also description of config make.
""",
'``-h [OPTIONS], --help [OPTIONS]``': r"""
-h [OPTIONS], --help [OPTIONS]
++++++++++++++++++++++++++++++

    If other OPTIONS are given, show help for these options. If
    OPTIONS is 'all', show help for all options. If OPTIONS is
    missing, show a short generic help message for the program.
""",
'``--jobs``': r"""
--jobs
++++++

    Specify the maximum number of jobs in sumo to run simultaneously.
    Currently this is used when the sources for modules of a build are
    created by checking out from version control systems. This number
    should be an integer greater or equal to 0. 0 means that the job
    number is equal to the number of CPUs, 1 means that there is only
    1 job running at the same time, all greater numbers specify the
    number of jobs running simultaneously. The default for this option
    is 0.
""",
'``--lines``': r"""
--lines
+++++++

    Show results of "build showmodules" in single lines.
""",
'``--list``': r"""
--list
++++++

    Show information for automatic command completion.
""",
'``--localbuilddir BUILDDIR``': r"""
--localbuilddir BUILDDIR
++++++++++++++++++++++++

    Specify a *local* support directory. Modules from the directory
    specifed by --builddir are used but this directory is not modfied.
    All new builds are created in the local build directory and only
    the build database file there is modified.
""",
'``--logmsg LOGMESSAGE``': r"""
--logmsg LOGMESSAGE
+++++++++++++++++++

    Specify a logmessage for automatic commits when --dbrepo is used.
""",
'``--makeflags MAKEFLAGS``': r"""
--makeflags MAKEFLAGS
+++++++++++++++++++++

    Specify extra option strings for make You can specify more than
    one of these by repeating this option or by joining values in a
    single string separated by spaces. A default for this option can
    be put in a configuration file.
""",
'``-m MODULE, --module MODULE``': r"""
-m MODULE, --module MODULE
++++++++++++++++++++++++++

    Define a modulespec. If you specify modules with this option you
    don't have to put modulespecs after some of the commands. You can
    specify more than one of these by repeating this option or by
    joining values in a single string separated by spaces. A default
    for this option can be put in a configuration file.
""",
'``--no-checkout``': r"""
--no-checkout
+++++++++++++

    With this option, "build new" does not check out sources of
    support modules. This option is only here for test purposes.
""",
'``-C, --no-default-config``': r"""
-C, --no-default-config
+++++++++++++++++++++++

    If this option is not given and --no-default-config is not given,
    the program tries to load the default configuration file sumo-
    scan.config from several standard locations (see documentation on
    configuration files).
""",
'``-N, --no-err-build-exists``': r"""
-N, --no-err-build-exists
+++++++++++++++++++++++++

    If "build new" finds that a build for the given modulespecs
    already exists, it returns an error. If this option is given, the
    command in this case only prints a warning and terminates sumo
    without error.
""",
'``--no-make``': r"""
--no-make
+++++++++

    With this option, "build new" does not call "make".
""",
'``--noignorecase``': r"""
--noignorecase
++++++++++++++

    For command 'find', do NOT ignore case.
""",
'``--nolock``': r"""
--nolock
++++++++

    Do not use file locking.
""",
'``-o OUTPUTFILE, --output OUTPUTFILE``': r"""
-o OUTPUTFILE, --output OUTPUTFILE
++++++++++++++++++++++++++++++++++

    Define the output for command 'use'. If this option is not given,
    'use' writes to 'configure/RELEASE'. If this option is '-', the
    command writes to standard-out.",
""",
'``-p, --progress``': r"""
-p, --progress
++++++++++++++

    Show progress of some commands on stderr. A default for this
    option can be put in a configuration file.
""",
'``--readonly``': r"""
--readonly
++++++++++

    Do not allow modifying the database files or the support
    directory. A default for this option can be put in a configuration
    file.
""",
'``--recursive``': r"""
--recursive
+++++++++++

    For command 'build delete', delete all dependend builds, too. For
    command 'build state' with state 'disabled', disable all dependend
    builds, too.
""",
'``--scandb SCANDB``': r"""
--scandb SCANDB
+++++++++++++++

    Specify the (optional) SCANDB file. The scan database file
    contains information on what moduleversion can be used with what
    dependency version.
""",
'``--sort-build-dependencies-first``': r"""
--sort-build-dependencies-first
+++++++++++++++++++++++++++++++

    For commands "build list", "build find -b", "build
    showdependencies" and "build showdependents" sort the builds that
    dependencies of a build always come before the build.
""",
'``--sort-build-dependencies-last``': r"""
--sort-build-dependencies-last
++++++++++++++++++++++++++++++

    For commands "build list", "build find -b", "build
    showdependencies" and "build showdependents" sort the builds that
    dependencies of a build always come after the build.
""",
'``--summary``': r"""
--summary
+++++++++
    Print a summary of the function of the program.
""",
'``--test``': r"""
--test
++++++
    Perform some self tests.
""",
'``--trace``': r"""
--trace
+++++++

    Switch on some trace messages.
""",
'``--tracemore``': r"""
--tracemore
+++++++++++

    Switch on even more trace messages.
""",
'``-U EXPRESSION, --url-patch EXPRESSION``': r"""
-U EXPRESSION, --url-patch EXPRESSION
+++++++++++++++++++++++++++++++++++++

    This option is used for commands db convert and db modconvert.
    Specify a repository url patchexpression. Such an expression
    consists of a tuple of 2 python strings. The first is the match
    expression, the second one is the replacement string. The regular
    expression is applied to every source url generated. You can
    specify more than one patchexpression. A default for this option
    can be put in a configuration file.
""",
'``-v, --verbose``': r"""
-v, --verbose
+++++++++++++

    Show command calls. A default for this option can be put in a
    configuration file.
""",
'``--version``': r"""
--version
+++++++++

    Show the program version and exit.
""",
'``-y, --yes``': r"""
-y, --yes
+++++++++

    All questions the program may ask are treated as if the user
    replied 'yes'.
""",
},
}
