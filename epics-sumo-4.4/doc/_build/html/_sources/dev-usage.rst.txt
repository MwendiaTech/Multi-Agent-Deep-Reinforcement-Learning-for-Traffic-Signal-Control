Develop support modules with sumo
=================================

sumo makes developing support modules easier. In this example we want to apply
changes in an existing support module, here "ALARM:R3-8". 

For our development we want to create a "sandbox" directory where we change and
compile the new support module. There are two ways to do this:

standalone:
  We use a local copy of the dependency database and build all support modules
  in a local directory.

local:
  We use a local copy of the dependency database, build all support modules in
  a local directory but use existing compiled support modules from a global
  build directory.

For both cases sumo create a configuration file "sumo.config" that contains all
needed settings and create the sandbox directory if it does not yet exist.

In the following example we create a sandbox in "local" mode.

Create the sandbox
------------------

Decide what the name of the sandbox should be, here we use "sandbox" and enter
this command::

  sumo config local sandbox

Create a "HEAD" version of a module
-----------------------------------

We now create a new entry in our local dependency database for the test version
of module "ALARM". The "tag" argument exactly in this form defines an *empty*
tag, this means we create an entry in the dependency database that uses no
tag::

  sumo db cloneversion ALARM R3-8 HEAD tag='""'

Answer 'y' when the program asks if the changes are correct.

Build the module for the first time
-----------------------------------

Note: If you have an application at hand that is used to test the support
module it is easier to continue at `Test in an application`_. How you change
and compile the support is described at `Change and recompile`_.

We first have to see which other modules are needed by "ALARM"::

  sumo build try ALARM:HEAD --detail 1

This produces the following output::

  Possible versions for unspecified/missing modules:
  
  BASE                R3-14-10-0-1 R3-14-12-2-1 R3-14-12-2-1-aragon2
                      R3-14-12-2-1-aragon3 R3-14-12-2-1-aragon4
                      R3-14-12-2-1-aragon5 R3-14-12-2-1-aragon6
                      R3-14-12-2-4 R3-14-12-2-5 R3-14-12-2-6
                      R3-14-12-2-7 R3-14-8-2-0 R3-14-8-2-1
  BSPDEP_TIMER        R4-0 R5-0 R5-1 R6-2
  MISC_DBC            R3-0
  
  Not all dependencies were included in module specifications, these modules
  have to be added:
      BASE
      BSPDEP_TIMER
      MISC_DBC
  
  Command 'new' would create build with tag 'local-BL-001'
  
  Your module specifications are still incomplete, command 'new' can not
  be used with these.

We specify the missing modules directly on the command line and create a new
build with the "HEAD" version of "ALARM"::

  sumo build new ALARM:HEAD BASE:R3-14-12-2-1-aragon6 BSPDEP_TIMER:R6-2 MISC_DBC:R3-0

We see the name of the new created build with::

  sumo build list | grep local-

Change and recompile
--------------------

We can now apply changes directly in directory::

  sandbox/build/ALARM/HEAD+local-BL-001

We recompile the module and it's dependencies with::

  sumo build remake local-BL-001

Test in an application
----------------------

In our application directory we first have to set up usage of the sumo sandbox::

  sumo config local sandbox

When asked "Directory 'sandbox' already exists, use it ?" answer "y".

In order to test our support change the definition of "ALARM" in file
"configure/MODULES" to::

  ALARM:HEAD

Then use the new support with::

  sumo build use

then create the application::

  make clean && make

You can now test the support in your application.

Commit the changes and define a tag
-----------------------------------

When the new version of the support is shown to work, we should first commit
all changes in our version control system. The new version should have tag
"R3-9" in this example.

Commands for darcs::

  cd sandbox/build/ALARM/HEAD+local-BL-001
  darcs record
  darcs tag R3-9
  darcs push
  
Commands for mercurial::

  cd sandbox/build/ALARM/HEAD+local-BL-001
  hg commit
  hg tag R3-9
  hg push

Commands for git::

  cd sandbox/build/ALARM/HEAD+local-BL-001
  git commit -a
  git tag R3-9
  git push

Commands for subversion::

  cd sandbox/build/ALARM/HEAD+local-BL-001
  svn commit 
  svn tag R3-9

Commands for cvs::

  cd sandbox/build/ALARM/HEAD+local-BL-001
  cvs commit 
  cvs tag R3-9

Add the new support to the dependency database
----------------------------------------------

Finally we have to add the new version of the support module to the dependency
database. 

We must ensure that we do not use the sandbox this time but the global sumo
database. This means that sumo must not load the file "sumo.config" that was
created by the command "sumo config local". Since sumo always loads
"sumo.config" from current working directory, we change to a different
directory before we issue the command::

  cd sandbox/database
  sumo db cloneversion ALARM R3-8 R3-9

We can now use the new version of the support in our applications.
