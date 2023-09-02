"""mercurial support
"""

# pylint: disable=invalid-name

import re
import os.path
import sumolib.system

__version__="4.4" #VERSION#

assert __version__==sumolib.system.__version__

# -----------------------------------------------
# Repo class
# -----------------------------------------------

def assert_hg():
    """ensure that mercurial exists."""
    sumolib.system.test_program("hg")

class Repo():
    """represent a mercurial repository."""
    # pylint: disable=R0902
    #                          Too many instance attributes
    rx_tag=re.compile(r'^(.*)\s+([0-9]+):([a-z0-9]+)$')
    rx_heads=re.compile(r'\bheads\b')
    def _default_repo(self):
        """return the default repo."""
        assert_hg()
        try:
            (reply,_)= sumolib.system.system(\
                                  "hg paths default -R %s" % self.directory,
                                  True, False, None,
                                  self.verbose, self.dry_run)
        except IOError as _:
            # probably no repo found
            return None
        st= reply.splitlines()[0].strip()
        if st.startswith("not found"):
            return None
        return st
    def _find_remote(self, patcher):
        """find and contact the remote repository."""
        default_repo= self._default_repo()
        if default_repo is None:
            return None
        if patcher is not None:
            default_repo= patcher.apply(default_repo)
        assert_hg()
        cmd= "hg -R %s incoming %s" % \
                 (self.directory, default_repo)
        # note: the following code doesn't show an error message on *any*
        # error that occurs with the command:
        (_,_,rc)= sumolib.system.system_rc(cmd, True, True, None,
                                           self.verbose, self.dry_run)
        if rc not in (0,1):
            # contacting the remote repo failed
            return None
        return default_repo
    def _local_changes(self, matcher):
        """returns True if there are uncomitted changes.

        Does basically "hg status". All lines that match the matcher
        object are ignored. The matcher parameter may be <None>.
        """
        assert_hg()
        cmd= "hg status -a -m -r -d -R %s" % self.directory
        (reply,_,rc)= sumolib.system.system_rc(cmd, True, False, None,
                                               self.verbose, self.dry_run)
        # Note: a return code 1 is normal with mercurial
        if rc not in (0,1):
            raise IOError(rc, "cmd \"%s\" failed" % cmd)
        changes= False
        for line in reply.splitlines():
            line= line.strip()
            if matcher is not None:
                # ignore if line matches:
                if matcher.search(line):
                    continue
            # any line remaining means that there were changes:
            changes= True
            break
        return changes
    def _local_patches(self):
        """returns True when there are unpushed patches.

        """
        if self.remote_url is None:
            raise AssertionError("cannot compute local patches without "
                                 "a reachable remote repository.")
        assert_hg()
        cmd= "hg -R %s outgoing" % self.directory
        (_,_,rc)= sumolib.system.system_rc(cmd, True, False, None,
                                           self.verbose, self.dry_run)
        if rc not in (0,1):
            raise IOError(rc, "cmd \"%s\" failed" % cmd)
        return rc==0
    def _current_revision(self):
        """returns the revision of the working copy.
        """
        assert_hg()
        (reply,_)= sumolib.system.system(\
                                "hg identify -i -R %s" % self.directory,
                                True, False, None,
                                self.verbose, self.dry_run)
        # for uncomitted changes, the revision ends with a "+":
        return reply.splitlines()[0].strip().replace("+","")
    def _tag_on_top(self):
        """returns True when a tag identifies the working copy.

        These automatically generated tags are ignored:
          tip, qtip, qbase, qparent

        Returns the found tag or None if no tag on top was found.
        """
        ignore= set(("tip","qtip","qbase","qparent"))
        curr_rev= self.current_revision
        assert_hg()
        cmd= "hg tags -R %s" % self.directory
        (reply,_)= sumolib.system.system(cmd, True, False, None,
                                         self.verbose, self.dry_run)
        tags= []
        for line in reply.splitlines():
            line= line.strip()
            m= self.__class__.rx_tag.search(line)
            if m is None:
                raise AssertionError("cannot parse: '%s' % line")
            tag= m.group(1).strip()
            if tag in ignore:
                continue
            if m.group(3)==curr_rev:
                tags.append(m.group(1).strip())
        if not tags:
            # no tags found:
            return None
        # return the first tag of the sorted list:
        tags.sort()
        return tags[0]
    def _hint(self, name):
        """return the value of hint "name"."""
        return self.hints.get(name)
    def __init__(self, directory, hints, verbose, dry_run):
        """initialize.

        Hints must be a dictionary. This gives hints how the directory should
        be scanned. Currently we know these keys in the dictionary:

        "ignore changes": sumolib.utils.RegexpMatcher
            All local changes in files that match the RegexpMatcher object are
            ignored. By this we can get the remote repository and tag from a
            directory although there are uncomitted changes. A common
            application is to ignore changes in file "configure/RELEASE".
        "dir patcher": sumolib.utils.RegexpPatcher
            This patcher is applied to the directory that is stored in the
            object.
        "url patcher": sumolib.utils.RegexpPatcher
            This patcher is applied to the URL that is stored in the object.
        "force local": bool
            If this is True, the returns repository object does not contain a
            remote repoistory url even if there was one.
        """
        self.hints= dict(hints) # shallow copy
        patcher= self._hint("dir patcher")
        if patcher is not None:
            directory= patcher.apply(directory)
        self.directory= directory
        self.verbose= verbose
        self.dry_run= dry_run
        self.local_changes= None
        self.remote_url= None
        self.local_patches= None
        self.tag_on_top= None
        self.current_revision= None
        if self.directory is None:
            return
        self.current_revision= self._current_revision()
        self.local_changes= \
                self._local_changes(self._hint("ignore changes"))
        self.remote_url= self._find_remote(self._hint("url patcher"))
        if self.remote_url is not None:
            self.local_patches= self._local_patches()
        if self._hint("force local"):
            self.remote_url= None
        self.tag_on_top= self._tag_on_top() # uses self._current_revision
    def __str__(self):
        """return a human readable representation."""
        lines= [ "mercurial repo",
                 "dir: %s" % repr(self.directory),
                 "current revision: %s" % repr(self.current_revision),
                 "local_changes: %s" % repr(self.local_changes),
                 "remote url: %s" % repr(self.remote_url),
                 "local patches: %s" % repr(self.local_patches),
                 "tag on top: %s" % repr(self.tag_on_top) ]
        return "\n".join(lines)
    @staticmethod
    def name():
        """return the repo type name."""
        # pylint: disable=R0201
        #                          Method could be a function
        return "hg"
    @staticmethod
    def distributed_repo():
        """True for distributed version controls systems, False otherwise."""
        return True
    def get_tag_on_top(self):
        """return the "tag on top" property."""
        return self.tag_on_top
    def get_remote_url(self):
        """return the "remote_url" property, this may be None."""
        return self.remote_url
    def get_revision(self):
        """return the current revision."""
        return self.current_revision
    @classmethod
    def scan_dir(cls, directory, hints, verbose, dry_run):
        """return a Repo object if a mercurial repo was found.

        This function returns <None> if no working repo was found.

        If bool(hints["write check"]) is True, return <None> if the repository
        directory is not writable.

        For parameter "hints" see comment at __init__.
        """
        # pylint: disable=R0201
        #                          Method could be a function
        repodir= os.path.join(directory,".hg")
        if not os.path.exists(repodir):
            return None
        if hints.get("write check"):
            if not os.access(repodir, os.W_OK):
                return None
        obj= cls(directory, hints, verbose, dry_run)
        return obj
    def source_spec(self):
        """return a complete source specification (for SourceSpec class).
        """
        if self.directory is None:
            raise AssertionError("cannot create source_spec from "
                                 "empty object")
        if self.local_changes:
            raise AssertionError("cannot create spec from repo '%s' with "
                                 "unrecorded changes" % self.directory)
        d= {"type":"hg"}
        if self.tag_on_top is not None:
            d["tag"]= self.tag_on_top
        else:
            d["rev"]= self.current_revision

        if self.remote_url is None:
            d["url"]= self.directory
        elif self.local_patches:
            d["url"]= self.directory
        else:
            d["url"]= self.remote_url
        return d
    @staticmethod
    def checkout(spec, destdir, _, verbose, dry_run):
        """spec must be a dictionary with "url" and "tag" (optional).
        """
        assert_hg()
        cmd_l= ["hg", "clone"]
        url= spec.get("url")
        if url is None:
            raise ValueError("spec '%s' has no url" % repr(spec))
        tag= spec.get("tag")
        rev= spec.get("rev")
        if tag and rev:
            raise ValueError("you cannot specify both, tag '%s' and "
                             "revision '%s'" % (tag,rev))
        if tag is not None:
            cmd_l.extend(["-u '%s'" % tag])
        elif rev is not None:
            cmd_l.extend(["-u '%s'" % rev])
        cmd_l.append("-q")
        cmd_l.append(url)
        cmd_l.append(destdir)
        cmd= " ".join(cmd_l)
        sumolib.system.system(cmd, False, False, None, verbose, dry_run)
    def commit(self, logmessage):
        """commit changes."""
        if not logmessage:
            m_param=""
        else:
            m_param="-m '%s'" % logmessage
        assert_hg()
        cmd="hg -R %s commit %s" % (self.directory, m_param)
        sumolib.system.system(cmd,
                              False, False, None,
                              self.verbose, self.dry_run)
        self.local_changes= False
    def push(self):
        """push all changes changes."""
        if self.remote_url is None:
            raise AssertionError("cannot push local patches without "
                                 "a reachable remote repository.")
        assert_hg()
        cmd="hg push -R %s %s" % (self.directory, self.remote_url)
        sumolib.system.system(cmd,
                              True, False, None,
                              self.verbose, self.dry_run)
    def pull_merge(self):
        """pull changes and try to merge."""
        if self.remote_url is None:
            raise AssertionError("cannot pull patches without "
                                 "a reachable remote repository.")
        assert_hg()
        # use "-u" to update to head:
        cmd="hg pull -R %s -u %s" % \
                (self.directory, self.remote_url)
        # system_rc cannot throw an exception:
        (stdout,_,rc)= sumolib.system.system_rc(cmd,
                                                True, False, None,
                                                self.verbose, self.dry_run)
        if rc!=0:
            msg="error, 'hg pull -u' failed"
            raise IOError(msg)
        must_merge= False
        for l in stdout.splitlines():
            if self.__class__.rx_heads.search(l):
                must_merge= True
                break
        if not must_merge:
            return
        cmd=("hg merge -q -R %s --config ui.merge=internal:merge") % \
                self.directory
        (_,_,rc)= sumolib.system.system_rc(cmd,
                                           False, False, None,
                                           self.verbose, self.dry_run)
        if rc:
            msg="error, 'hg merge' failed"
            raise IOError(msg)
        cmd="hg commit -m 'automatic merge' -R %s " % self.directory
        # the follwing command may raise IOError or OSError:
        sumolib.system.system(cmd,
                              False, False, None,
                              self.verbose, self.dry_run)
