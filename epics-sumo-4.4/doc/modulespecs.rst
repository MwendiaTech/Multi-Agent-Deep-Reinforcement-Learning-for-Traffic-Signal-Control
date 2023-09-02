Module Specifications
=====================

:term:`Module` specifications are central to many :term:`commands` in 
:doc:`sumo <reference-sumo>`. They provide a powerful way to
specify what :term:`modules` and what :term:`versions` to use.

A module specification is a string with a certain format. "Module
specifications" means a list of these strings.

Sources of module specifications
--------------------------------

Module specifications can come from three sources (not taking into account
:term:`commands` that read files):

The configuration file
++++++++++++++++++++++

This is a `JSON <http://www.json.org>`_ file that contains settings for some or
all of the :term:`commandline options`. Modules are stored here with the key
"module" as a list of strings.

The command line option "-m" or "--module"
++++++++++++++++++++++++++++++++++++++++++

The argument of this :term:`commandline option` is a string that is a single
:term:`module` specification or a whitespace separated list of :term:`module`
specifications. In order to give more than one :term:`module` specification you
can also use this option more than once.

Arguments to a command
++++++++++++++++++++++

Some :term:`commands` may be followed by arguments that must be module
specifications.

Combining all module specifications
-----------------------------------

There are two possibilities, how module specifications from these three sources
are combined:

Override mode
+++++++++++++

Each new set of module specifications overrides the previous one in this order:

- configuration file
- command line options
- command arguments

Append mode
+++++++++++

When command line option::

  -A module

is given, module specifications from all three sources are combined into a
single list in this order:

- configuration file
- command line options
- command arguments

Processing the list
+++++++++++++++++++

This list is then processed in order to get a list of module specifications
where each module is mentioned just once. The order of modules is the same as
they were given in the sources.

If a module is specified more than once the last specification overwrites the
first one. Here is an example:

A_Module:Version1 B_Module:Version2 A_Module:Version3

becomes:

A_Module:Version3 B_Module:Version2 

The format of a module specification
------------------------------------

Module versions
+++++++++++++++

A module can be specified in these forms:

=============================   ======================================
schema                          meaning
=============================   ======================================
modulename                      modulename 
modulename:versionspec          modulename and version
=============================   ======================================

A :term:`versionspec` defines the :term:`version` the module should have.

Here are some examples:

+-----------------------------------------+---------------------------------------------+
| module specification                    | meaning                                     |
+=========================================+=============================================+
| ALARM                                   | modulename "ALARM", version not specified   |
+-----------------------------------------+---------------------------------------------+
| ALARM:R3-9                              | modulename "ALARM", version "R3-9"          |
+-----------------------------------------+---------------------------------------------+
| ALARM:-R3-9                             | modulename "ALARM", version "R3-9" or below |
+-----------------------------------------+---------------------------------------------+
| ALARM:+R3-9                             | modulename "ALARM", version "R3-9" or above |
+-----------------------------------------+---------------------------------------------+

Commands
++++++++

These are *commands* for the merging process. Commands always start with a
colon ":", arguments to commands must be separated by colons. A command has
this form:

:command{arguments}

where arguments is a colon separated list of arguments. Here are some examples
how a command looks like:

=============  ======================================
command        remark
=============  ======================================
:clear         command "clear" which has no arguments
:load:myfile   command "load" with argument "myfile"
=============  ======================================

Here are the known commands:

clear
:::::

This command clears the list of module specifications so far. For example this
module specifications list::

  module1 module2 :clear module3 module4

becomes::

  module3 module4

rm
::

This command removes single module from the list. For example this module
specifications list::

  module1 module2 module3 :rm:module2 

becomes::

  module1 module3

load
::::

This command loads module specifications from a `JSON <http://www.json.org>`_
file. It must be followed by the name of the file. The 
`JSON <http://www.json.org>`_ file must contain a key "module" which is a list
of strings. These are then inserted at the place in the list where the command
was found.

If for example file "mymodules" has this content::

  {
      "module": [
          "AGILENT-SUPPORT:R0-11", 
          "AGILENT:R2-3", 
  }

The module specification::

  ASYN:R4-17-2 :load:mymodules EK:R2-2

becomes after merging::

  ASYN:R4-17-2 AGILENT-SUPPORT:R0-11 AGILENT:R2-3 EK:R2-2

build
:::::

This command takes all module specifications from a :term:`build` and inserts
them in the llist of module specifications. It must be followed by the name of
the :term:`build`, the :term:`buildtag`.

If for example, build "MLS-01" contains the modules "AGILENT-SUPPORT:R0-11" and
"AGILENT:R2-3", the module specification::

  ASYN:R4-17-2 :build:MLS-01 EK:R2-2

becomes after merging::

  ASYN:R4-17-2 AGILENT-SUPPORT:R0-11 AGILENT:R2-3 EK:R2-2

