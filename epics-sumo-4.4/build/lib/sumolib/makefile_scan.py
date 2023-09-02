"""
=============
makefile_scan
=============

Scan definitions in a makefile or a list of makefiles. This module
actually calls "make" in order to examine the files and returns the
values of all variables or makefile macros as a dictionary.

The main function in this module is "scan". "scan" is called like this::

  data= scan(filenames, verbose, dry_run)

Parameters are:

filenames
  A single filename or a list of filenames

verbose
  A boolean, if True print all system command calls to the console.

dry_run
  A boolean, if True just print the system command calls but do not
  execute them.

"""

# pylint: disable= invalid-name

import os.path
import re

import sumolib.system
import sumolib.utils

__version__="4.4" #VERSION#

assert __version__==sumolib.system.__version__

# -----------------------------------------------
# makefile scanning
# -----------------------------------------------

# bash allows almost *any* character except '=' as variable name:
rx_def= re.compile(r'^([^=]+)=(.*)$')

def _scan(filenames, external_definitions= None,
          warnings= True,
          verbose= False, dry_run= False):
    """scan makefile-like definitions.

    may raise:
    IOError
    """
    # pylint: disable=too-many-locals, too-many-branches
    for f in filenames:
        if not os.path.exists(f):
            # pylint: disable= consider-using-f-string
            raise IOError("file \"%s\" does not exist" % f)
    if filenames:
        include_cmd= "include " + (" ".join(filenames))
    else:
        include_cmd= ""
    extra= ""
    if external_definitions:
        l= []
        for (k,v) in external_definitions.items():
            # pylint: disable= consider-using-f-string
            l.append("%s=\"%s\"" % (k,v))
        l.append("")
        extra= " ".join(l)
    cmd=("/bin/echo -e \"%s\\n" +\
         ".EXPORT_ALL_VARIABLES:\\n" +\
	 "scan_makefile_pe:\\n" +\
	 "\\t@printenv\\n\" | %s " +\
	 "make -s -f - scan_makefile_pe") % (include_cmd,extra)
    data= {}
    # may raise IOError:
    (reply,_)= sumolib.system.system(cmd, True, False, None, verbose, dry_run)
    if dry_run:
        return data
    name= None
    value= None
    for line in reply.splitlines():
        m= rx_def.match(line)
        # pylint:disable= no-else-continue
        if m is None:
            if name is None:
                # shouldn't happen
                if warnings:
                    # pylint: disable= consider-using-f-string
                    sumolib.utils.errmessage(\
                        ("\nmakefile_scan.py: warning:\n"
                         "\tline not parsable in %s\n"
                         "\t%s\n" % \
                         (" ".join(filenames),repr(line))), wrap= False)
                continue
            # assume that this belongs to a multi-line value:
            value+= "\n"
            value+= line
            continue
        else:
            if name is not None:
                # store the previous one:
                data[name]= value
            name= m.group(1)
            value= m.group(2)
    if name is not None:
        # store the last one:
        data[name]= value
    return data

def scan(filenames, external_definitions= None, pre= None,
         warnings= True,
         verbose= False, dry_run= False):
    """scan makefile-like definitions.

    This takes a makefile name or a list of makefile names and returns a
    dictionary with all definitions made in these files. All definitions
    are resolved meaning that all variables that are used in the values
    of definitions are replaces with their values.

    may raise:
    IOError

    filenames
        a single filename (string) or a list of filenames (list of strings)

    external_definitions
        A dict with variable settings that are pre-defined.

    pre
        None or a dict. For consecutive calls of this function providing an
        initially empty dictionary here speeds up calls by a factor of 2.

    warnings
        print a warning when a line cannot be parsed

    verbose
        if True, print command calls to the console

    dry_run
        if True, only print command calls to the console, do not return
        anything.

    """
    # pylint: disable=R0913
    #                          Too many arguments
    if isinstance(filenames, str):
        filenames= [filenames]
    if pre is None:
        pre= _scan([], external_definitions, warnings, verbose, dry_run)
    else:
        if not pre: # empty dict
            pre.update(_scan([], external_definitions, warnings,
                             verbose, dry_run))

    # _scan may raise IOError here:
    post= _scan(filenames, external_definitions, warnings, verbose, dry_run)
    new= {}
    for (k,v) in post.items():
        if k in pre:
            if pre[k]==v:
                continue
        new[k]= v
    return new
