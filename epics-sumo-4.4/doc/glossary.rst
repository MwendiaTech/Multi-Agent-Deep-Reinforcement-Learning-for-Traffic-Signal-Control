========
Glossary
========

Here we define some of the terms used in the following text.

.. glossary:: :sorted:

  configuration file
      A file where values for some of the command line options can be
      specified. Youn usually prepare a configuration file globally or for your
      EPICS application or both. More details on this topic can be found at
      :doc:`"configuration files "<configuration-files>`.

  modules
      See :term:`module`.

  module
      A *module* is a software package, an 
      `EPICS <http://www.aps.anl.gov/epics>`_ support module or an 
      `EPICS <http://www.aps.anl.gov/epics>`_ base. Each module has a
      :term:`modulename` and a :term:`versionname`. 
      
      Usually modules that have the same :term:`modulename` share the same
      source tree but differ in their source :term:`versions`. 
      
      A working copy of the source code of the module is placed in a
      :term:`support directory`. and is usually managed by a version control
      system. The module is compiled in this directory, the binary files are
      installed within the directory structure.

  versions
      See :term:`version`.

  version
      A :term:`module` has several *versions*. A *version* is a state of the
      :term:`module` source directory that can be recreated anywhere either by
      copying a source directory or be checking out a version from the version
      control system with parameters that identify the version.
  
  modulenames
      See :term:`modulename`.

  modulename
      Each :term:`module` has a unique name, the *modulename*. Note that each
      :term:`version` of the same :term:`module` has the same *modulename*.

  moduleversions
      See :term:`version`.
  
  moduleversion
      See :term:`version`.
  
  versionnames
      See :term:`versionname`.

  versionname
      In sumo, each :term:`version` of a :term:`module` has a *versionname* that is
      unique for that :term:`module`. The :term:`modulename` together with the
      *versionname* identify a specific version of the :term:`module`. 

  modulespecifications
      See :term:`modulespec`.

  modulespecs
      See :term:`modulespec`.

  modulespec
      This is a string that specifies a :term:`module` and its :term:`version`.
      Module specifications are an important concept in sumo, see also
      :doc:`Module Specifications <modulespecs>`.

  versionspec
      This is a string that specifies the :term:`version` of a :term:`module`.
      See :doc:`Module Specifications <modulespecs>` for further details.

  support directory
      This is the directory where the compiled versions of :term:`modules` are
      stored.

  sources
      See :term:`source`.

  source
      Each :term:`version` of a :term:`module` has a *source*. The *source*
      defines how we can obtain a copy of the sources for the :term:`version`.
      Sumo supports paths and some version control systems in the *source*
      definitions.
  
  dependencies
      This means the set of every :term:`dependency` of a :term:`module`.

  dependency
      A :term:`version` of a :term:`module` may depend on specific
      :term:`versions` of other modules. This means that the :term:`module`
      cannot be built and without all these other :term:`modules`.  A
      *dependency* is the :term:`modulename` and :term:`versionname` of one of
      these other modules.

  aliases
      See :term:`alias`.

  alias
      For each :term:`module` in the :term:`dependency` list there may be an
      *alias* definition.  When a RELEASE file is created for a :term:`module`,
      the variable names that are put into the file are the same as each
      :term:`modulename` of each :term:`dependency` except where an *alias*
      exists. In this case, the value of the *alias* is taken as variable name.
  
  tag
      This is a string that may by part of the :term:`source` of a
      :term:`module`. A *tag* helps to identify the :term:`version` of the
      :term:`module` within the version control system. In sumo, a *versionname*
      is always the same as the *tag* if the *tag* exists.
  
  states
      See :term:`state`.

  state
      This is a string describing the maturity of a :term:`build`. A *state*
      may be one of the following strings:
  
      stable
        This set of modules is known to work.
  
      testing
        This set of modules was built successfully.
  
      unstable
        This set of modules is not yet built successfully.
  
      disabled
        This set of modules should no longer be used by applications or newer
        builds. It has a defect or cannot be recreated due to changes in the
        dependency database.

      incomplete
        This is the state of a build while it is created with "sumo build new".
        When all module directories were created, it's state is set to
        "unstable".

      broken
        This can happen if a build was to be deleted but some of the files
        couldn't be removed. A build with this state can no longer be used and
        should be deleted soon.
  
  builds
      See :term:`build`.

  build
      A *build* is a set of modules where all modules are compiled.
      Information on all build is kept in the build database (:term:`BUILDS.DB`).
      Each *build* has a unique :term:`buildtag`.

  buildtags
      See :term:`buildtag`.

  buildtag
      A *buildtag* is a name that identifies each :term:`build`. Information
      for each :term:`build` can be found in the build database
      (:term:`BUILDS.DB`) by looking up the *buildtag*.

  regular expression
      A regular expression is a way to specify a pattern in order to match
      strings.  For further information on regular expressions see `re -
      Regular expressions <http://docs.python.org/3/library/re.html>`_. For an
      introduction to regular expressions see 
      `Regular Expression HOWTO <http://docs.python.org/3/howto/regex.html#regex-howto>`_.

  scanfile
      This is the file created by :doc:`"sumo-scan all"<reference-sumo-scan>`.
      This `JSON <http://www.json.org>`_ file can be converted to a :term:`DEPS.DB`
      file with by :doc:`"sumo db convert"<reference-sumo>`.

  dependency database
      See :term:`DEPS.DB`.

  scan database
      See :term:`SCANDB`.

  build database
      See :term:`BUILDS.DB`.

  DEPS.DB
      The dependency database. For further details see
      :ref:`reference-sumo-db-The-dependency-database`.

  BUILDS.DB
      The build database. For further details see
      :ref:`reference-sumo-The-build-database`.

  SCANDB
      This scan database is also called :term:`SCANDB`. It is a file in `JSON
      <http://www.json.org>`_ format which contains information on what
      :term:`version` of a :term:`module` was used which what :term:`version`
      of a :term:`dependency`. This file is not essential in order to use sumo.
      It can be used when you start using sumo in order to see what
      :term:`versions` of :term:`modules` are probably compatible with each
      other. If you start creating :term:`builds`, this :term:`version`
      information will also be gathered from your successful :term:`builds` and
      at some point you will no longer need the scan database.

  commandline options
      See :term:`commandline option`.

  commandline option
      This means an argument to a program that has the form "-[letter]" or
      "--[word]". Some commandline options may require that an argument
      immediately follows the option.

  commands
      See :term:`command`.

  command
      This is an argument to a program that doesn't start with a dash "-". In
      all programs here, you can give only *one* command while there may be
      several :term:`commandline options`. Commands may be immediately followed
      by command arguments. 
