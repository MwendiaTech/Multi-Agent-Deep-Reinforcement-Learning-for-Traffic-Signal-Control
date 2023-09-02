Release 4.0.1
-------------

Date: 2020-03-10

(Changes with respect to relase 4.0)

Bugfixes
++++++++

- With python 3.2.3, errors while checking out modules were not recognized.
- error messages from checking out darcs repos are now reproducible

Release 4.0.2
-------------

Date: 2020-06-02

Internal changes
++++++++++++++++

- Platforms where tests succeeded are now documented in test/tests.log

Bugfixes
++++++++

- Do not use "git -C" since older versions of git don't support this

Release 4.1
-----------

Date: 2020-08-30

Internal changes
++++++++++++++++

- All docker scripts were moved to administration_tools/docker
- Various improvements in dockerscripts, can now use podman instead of docker
- Package support for fedora-30 was removed, fedora-32 was added instead
- removed pylint warnings in various files
- add a test that checks what happens if we try to create a build that 
  already exists
- Support for creating code coverage statistics of the tests was added
- some comments in the code regarding "sumo build try" were added.
- optimized "git clone", if a tag or branch is given, it is now provided 
  with option "-b" to git

Bugfixes
++++++++

- Small bugfix in the documentation
- fixed a misleadung error message when locking file DEPS.DB fails
- option "--dry-run" sometimes raised an exception when sumo should have
  created a file. With "--dry-run" sumo should only show what it would have 
  done, but not make any changes on files.
- give a proper error message when "sumo build try ... --exclude-states"
  gets an invalid regular expression, added testcode for this
- Option "--dry-run" is now better supported. All functions that do changes
  to files shouldn't change anything when "--dry-run" is used and just
  print to the console what they would have done.

Documentation
+++++++++++++

- "configuration file" was added to the glossary
- small improvements
- an example how to re-create a build with the help of "sumo build showmodules"
  was added

New/Changed functions
+++++++++++++++++++++

- The help of command line options is now sorted alphabetically
- added "sumo build showmodules", this list all modules used in a build in 
  the form MODULE:VERSION which is compatible with the format sumo option
  "-m" expects. An example how to use this is in the documentation.
- added "sumo build showdependencies", this shows all builds the given 
  build depends on
- added "sumo build showdependents", this shows all builds the depend
  on the given build
- "sumo build new" now first checks if a matching build exists. If it does,
  the command aborts with an error message. If option --no-err-build-exists
  is given, the command prints a warning and stops without error code.
- many "sumo build" commands that print information about builds can now sort
  the builds by their dependency relations. With
  --sort-build-dependencies-first, dependencies of a build always come before
  the build.  With --sort-build-dependencies-last, dependencies of a build
  always come after the build. 
- commands that list or show builds now ignore builds that do not have the 
  state "stable" or "testing". You must use option "--all-builds" to see
  the other builds, too.
- the template for "sumo config new ... github" was extended and improved,
  some modules were updated and AREADETECTOR was added.

Compatibility
+++++++++++++

- Command "sumo build list" now only shows builds with the state "stable" or
  "testing". Before sumo 4.1 it used to show *all* builds. In order for the
  command to do the same as in older versions of sumo, add option
  "--all-builds" like in "sumo build list --all-builds".

Release 4.1.1
-------------

Date: 2020-09-11

Internal changes
++++++++++++++++

- test/tests.log was updated

Documentation
+++++++++++++

- small bugfixes
- a file RELEASES.rst was added. This contains information about changes
  between releases.

Bugfixes
++++++++

- "sumo -h all" printed the option help twice, this was fixed

Release 4.1.2
-------------

Date: 2020-09-14

Internal changes
++++++++++++++++

- added RELEASES.rst to the distribution
- removed supported of sumo repository at bitbucket
- update of new version recipe in administration_tools/README.rst

Release 4.1.3
-------------

Date: 2021-03-09

Bugfixes
++++++++

- A git source specification didn't work when a revision was given.
- administration_tools/show-last-release.sh was added. The should have been
  added in some previous release. It is just a small utility to create new
  revisions of the program.
- Compatibility fix for Darcs 2.16.

Documentation
+++++++++++++

- test/README.rst now lists the version control systems needed to run the
  tests.

Management
++++++++++

- Support for packages for debian-8 and fedora-31 was removed, support for
  packages for debian-11 and fedora-33 was added.

Release 4.1.4
-------------

Date: 2021-08-19

Internal changes
++++++++++++++++

- Some changes in Builds.py due to pylint warnings.
- test/tests.log was updated

Bugfixes
++++++++

- Builds.py: The "multiple build tag" warning didn't show the build name.

Release 4.1.5
-------------

Date: 2022-03-02

Data files
++++++++++

- Added BASE:R3-15-9 to data/templates/github/DEPS.DB, BASE:R3-15-8 cannot
  always be built.

Package building
++++++++++++++++

- Support for building RPM packages for fedora-34 and fedora-35 was added,
  support for fedora-32 and fedora-33 was removed.

Release 4.2
-----------

Date: 2022-04-07

Bugfixes
++++++++

- One of the tests no longer worked although the program had no error
- A read-only file system is now treated the same as missing write permissions

Internal changes
++++++++++++++++

- pylint warnings were removed in all files
- sumo build use now opens DEPS.DB only once instead of twice
- The multiprocessing implementation now uses multiprocessing pool
- all programe check for python version >= 3.2
- init.sh script prepares the "test" directory
- administration_tools/README.rst has a hint on running the tests

Changes in warnings
+++++++++++++++++++

- Warning messages are now formatted in a more readable way.
- Better warning when global and local builddir have builds of the same name
- sumo messages no longer call a build a "buildtree"

Documentation
+++++++++++++

- Possible values for --dbdir are now better documented
- Configuration file documentation: Tags are now in alphabetical order

New/Changed functions
+++++++++++++++++++++

- sumo --readonly implies repomode "get".
- "sumo --jobs JOBNUMBER" replaces "sumo --no-multiprocessing"

Release 4.3
-----------

Date: 2022-06-09

Internal changes
++++++++++++++++

- Small changes in administration_tools/README.rst.

Documentation
+++++++++++++

- Some spelling errors were removed.

Error checking
++++++++++++++

- "sumo config make FILENAME [OPTIONNAMES]" checks if OPTIONNAMES are valid.

New/Changed functions
+++++++++++++++++++++

- "sumo build find" now shows matching/non-matching/missing modules.
- "sumo build getmodules" and the "sumo config make --getmodules" were added.

Release 4.3.1
-------------

Date: 2022-09-28

Improvements
++++++++++++

- sumo-scan: Option "--doc" doesn't do anything and was removed.

Distribution
++++++++++++

- Create rpm packages for Fedora 35 and Fedora 36.

Documentation
+++++++++++++

- Small changes and fixes in the documentation and sumo-scan online-help.

Release 4.3.2
-------------

Date: 2022-10-14

Internal changes
++++++++++++++++

- Some pylint warnings in sumo were removed.

Documentation
+++++++++++++

- The online help for main-commands in sumo was fixed.
- A recipe for a complete demo for sumo was added to the documentation.

Release 4.4
-------------

Date: 2022-11-29

Documentation
+++++++++++++

- Document "make distclean" for the test directory in test/README.rst.

Internal changes
++++++++++++++++

- sumo-scan: Obsolete function "scan_config_file" was removed.

Improvements
++++++++++++

- sumo-scan: Do not abort on errors caused by faulty RELEASE files.

