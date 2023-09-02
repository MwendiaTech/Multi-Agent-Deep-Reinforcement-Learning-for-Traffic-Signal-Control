"""path support
"""

# pylint: disable=invalid-name

import os.path
import sumolib.system

__version__="4.4" #VERSION#

assert __version__==sumolib.system.__version__

# -----------------------------------------------
# Repo class
# -----------------------------------------------

class Repo():
    """represent a path."""
    def _hint(self, name):
        """return the value of hint "name"."""
        return self.hints.get(name)
    def __init__(self, directory, hints, verbose, dry_run):
        """initialize."""
        self.hints= dict(hints) # shallow copy
        patcher= self._hint("dir patcher")
        if patcher is not None:
            directory= patcher.apply(directory)
        self.directory= directory
        self.verbose= verbose
        self.dry_run= dry_run
        if directory is not None:
            if not os.path.exists(directory):
                raise IOError("path '%s' doesn't exist" % directory)
    def __str__(self):
        """return a human readable representation."""
        lines= [ "directory",
                 "dir: %s" % repr(self.directory)]
        return "\n".join(lines)
    def name(self):
        """return the repo type name."""
        # pylint: disable=R0201
        #                          Method could be a function
        return "path"
    @classmethod
    def scan_dir(cls, directory, hints, verbose, dry_run):
        """return a Repo object."""
        # pylint: disable=W0613
        #                          Unused argument
        return cls(directory, hints, verbose, dry_run)
    def source_spec(self):
        """return a complete source specification (for SourceSpec class).
        """
        if self.directory is None:
            raise AssertionError("cannot create source_spec from "
                                 "empty object")
        d= {"type":"path",
            "url" : self.directory
           }
        return d
    @staticmethod
    def checkout(spec, destdir, _, verbose, dry_run):
        """spec must be a string.
        """
        url= spec.get("url")
        if url is None:
            raise ValueError("spec '%s' has no url" % repr(spec))
        #cmd= "scp -r -p \"%s\" %s" % (url, destdir)
        # join(url,"") effectively adds a "/" at the end of the path. This is
        # needed in order for rsync to work as intended here.
        cmd= "rsync -a -u -L --chmod=Fu+w \"%s\" %s" % \
             (os.path.join(url,""), destdir)
        sumolib.system.system(cmd, False, False, None, verbose, dry_run)
