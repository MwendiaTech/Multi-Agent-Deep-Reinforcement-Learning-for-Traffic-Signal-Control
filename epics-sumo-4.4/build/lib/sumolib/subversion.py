"""mercurial support
"""

# pylint: disable=invalid-name

import os.path
import sys
import sumolib.system

__version__="4.4" #VERSION#

assert __version__==sumolib.system.__version__

# -----------------------------------------------
# Repo class
# -----------------------------------------------

def assert_svn():
    """ensure that subversion exists."""
    sumolib.system.test_program("svn")

class Repo():
    """represent a subversion repository."""
    # pylint: disable=R0902
    #                          Too many instance attributes
    def _tag_on_top(self):
        """returns True when a tag identifies the working copy.

        Returns the found tag or None if no tag on top was found.
        """
        def format_tag(t):
            """simple tag formatting."""
            t= t.strip()
            if t.endswith("/"):
                return t[0:-1]
            return t
        curr_rev= self.current_revision
        assert_svn()
        if not self.remote_url:
            raise ValueError("error, no remote url")
        path= os.path.join(self.remote_url, "tags")
        # first get a raw list of tags:
        cmd= "svn ls %s" % path
        (reply,_)= sumolib.system.system(cmd, True, False, None,
                                         self.verbose, self.dry_run)
        tags= [format_tag(t) for t in reply.splitlines()]
        # now get a list of tags together with revision numbers: since the
        # format of the following command is not really documented, we dont'w
        # want to rely on column numbers. Instead we match the line with the
        # list of tags from the command above.
        cmd= "svn ls %s -v" % path
        (reply,_)= sumolib.system.system(cmd, True, False, None,
                                         self.verbose, self.dry_run)

        found_tags= []
        for line in reply.splitlines():
            line= line.strip()
            if not line.startswith(curr_rev):
                continue
            for tag in tags:
                if tag in line:
                    found_tags.append(tag)
        if not tags:
            # no tags found:
            return None
        # return the first tag of the sorted list:
        tags.sort()
        return tags[0]
    def _default_repo(self):
        """return the default repo."""
        assert_svn()
        # note: the following code doesn't show an error message on *any*
        # error that occurs with the command:
        (reply,_,rc)= sumolib.system.system_rc(\
                              "svn info %s" % self.directory,
                              True, True, None,
                              self.verbose, self.dry_run)
        if rc!=0:
            # probably no repo found
            return None
        for line in reply.splitlines():
            if line.lower().startswith("repository root:"):
                return line.split(":",1)[1].strip()
        return None
    def _find_remote(self, patcher):
        """find and contact the remote repository."""
        default_repo= self._default_repo()
        if default_repo is None:
            return None
        if patcher is not None:
            default_repo= patcher.apply(default_repo)
        assert_svn()
        cmd= "svn ls %s --depth empty" % default_repo
        # note: the following code doesn't show an error message on *any*
        # error that occurs with the command:
        (_,_,rc)= sumolib.system.system_rc(cmd, True, True, None,
                                           self.verbose, self.dry_run)
        if rc!=0:
            # contacting the remote repo failed
            return None
        return default_repo
    def _local_changes(self, matcher):
        """returns True if there are uncomitted changes.

        Does basically "svn status". All lines that match the matcher
        object are ignored. The matcher parameter may be <None>.
        """
        assert_svn()
        cmd= "svn status %s" % self.directory
        (reply,_)= sumolib.system.system(cmd, True, False, None,
                                         self.verbose, self.dry_run)
        # flags from svn status that indicate a modification:
        mod_flags= set(("A","C","D","M","R","!","~"))
        changes= False
        for line in reply.splitlines():
            # svn status has return code 0 even if the working copy path
            # doesn't exist:
            if "not a working copy" in line:
                raise IOError("error, 'svn status' failed : %s" % line)
            if line.startswith("? "):
                # ignore unknown files
                continue
            if line[0] not in mod_flags:
                continue
            if matcher is not None:
                # up to column 8 there are flags, followed by a revision number
                # and finally the filename,
                # ignore if the filename matches:
                if matcher.search(line[8:]):
                    continue
            # any line remaining means that there were changes:
            changes= True
            break
        return changes
    def _current_revision(self):
        """returns the revision of the working copy.
        """
        assert_svn()
        (reply,_)= sumolib.system.system(\
                                "svnversion %s" % self.directory,
                                True, False, None,
                                self.verbose, self.dry_run)
        result= reply.splitlines()[0].strip()
        # possible results:
        # 4168          normal working copy
        # 4123:4168     mixed revision working copy
        # 4168M         modified working copy
        # 4123S         switched working copy
        # 4123P         partial working copy, from a sparse checkout
        # 4123:4168MS   mixed revision, modified, switched working copy

        # we handle here just "normal working copy" and "modified working
        # copy", for all other cases we return None.
        result= result.replace("M","")
        try:
            int(result)
        except ValueError as _:
            return None
        return result
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
        self.tag_on_top= None
        self.current_revision= None
        if self.directory is None:
            return
        self.current_revision= self._current_revision()
        self.local_changes= \
                self._local_changes(self._hint("ignore changes"))
        self.remote_url= self._find_remote(self._hint("url patcher"))
        if self._hint("force local"):
            raise ValueError("error, 'force local' not "
                             "supported for subversion")
        self.tag_on_top= self._tag_on_top() # uses self._current_revision
    def __str__(self):
        """return a human readable representation."""
        lines= [ "subversion repo",
                 "dir: %s" % repr(self.directory),
                 "current revision: %s" % repr(self.current_revision),
                 "local_changes: %s" % repr(self.local_changes),
                 "remote url: %s" % repr(self.remote_url),
                 "tag on top: %s" % repr(self.tag_on_top) ]
        return "\n".join(lines)
    @staticmethod
    def name():
        """return the repo type name."""
        # pylint: disable=R0201
        #                          Method could be a function
        return "svn"
    @staticmethod
    def distributed_repo():
        """True for distributed version controls systems, False otherwise."""
        return False
    def get_tag_on_top(self):
        """return the "tag on top" property."""
        return self.tag_on_top
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
        repodir= os.path.join(directory,".svn")
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
        d= {"type":"svn"}
        if self.tag_on_top is not None:
            d["tag"]= self.tag_on_top
        else:
            d["rev"]= self.current_revision

        if self.remote_url is None:
            raise AssertionError("no remote_url")
        d["url"]= self.remote_url
        return d
    @staticmethod
    def checkout(spec, destdir, _, verbose, dry_run):
        """spec must be a dictionary with "url" and "tag" (optional).
        """
        assert_svn()
        cmd_l= ["svn", "checkout"]
        url= spec.get("url")
        if url is None:
            raise ValueError("spec '%s' has no url" % repr(spec))
        tag= spec.get("tag")
        rev= spec.get("rev")
        if tag is None:
            cmd_l.append(url)
        else:
            cmd_l.append(os.path.join(url,"tags",tag))
        if tag and rev:
            raise ValueError("you cannot specify both, tag '%s' and "
                             "revision '%s'" % (tag,rev))
        if rev is not None:
            cmd_l.append("-r '%s'" % rev)
        cmd_l.append("-q")
        cmd_l.append(destdir)
        cmd= " ".join(cmd_l)
        sumolib.system.system(cmd, False, False, None, verbose, dry_run)
    def commit(self, logmessage):
        """commit changes to the repository.

        NOTE: with subversion, after "svn commit" a following "svn
        log" will not show the commit message of this last commit.
        This will only be the case when you run "svn update"
        explicitly.
        """
        # With subversion, a "commit" always contacts the central
        # repository. We may get an error message like "File 'XXX' is
        # out of date" when the file was changed in the meantime by
        # someone else at the central repository. To handle this, we
        # do a "pull_merge" first, which is "svn update" here. This
        # command may detect a conflict and raise an IOError exception:
        self.update()
        if not logmessage:
            m_param=""
            # if subversion starts an editor, we must not catch stdout:
            catch_stdout= False
        else:
            m_param="-m '%s'" % logmessage
            # with a log message provided with "-m", subversion doesn't start
            # an editor. In order to keep it silent, we catch stdout in this
            # case:
            catch_stdout= True
        assert_svn()
        cmd="svn commit %s" % m_param
        cwd= sumolib.system.changedir(self.directory,
                                      self.verbose, self.dry_run)
        (_,_,rc)= sumolib.system.system_rc(cmd,
                                           catch_stdout, False, None,
                                           self.verbose, self.dry_run)
        sumolib.system.changedir(cwd,
                                 self.verbose, self.dry_run)
        if rc:
            msg="error, 'svn commit' failed"
            raise IOError(msg)
        self.local_changes= False
    def update(self):
        """update repo."""
        # use "-u" to update to head:
        assert_svn()
        cmd="svn update --non-interactive"
        stderr= None
        cwd= sumolib.system.changedir(self.directory,
                                      self.verbose, self.dry_run)

        (stdout,stderr,rc)= sumolib.system.system_rc(cmd, \
                                                True, True, None, \
                                                self.verbose, self.dry_run)
        sumolib.system.changedir(cwd,
                                 self.verbose, self.dry_run)
        flushed= False
        if stderr:
            # ensure that output on stderr is always printed to the console:
            sys.stdout.flush()
            sys.stderr.write(stderr)
            sys.stderr.flush()
            flushed= True
        for l in stdout.splitlines()+stderr.splitlines():
            if "conflict" in l.lower():
                msg="error, 'svn update' had a conflict"
                if not flushed:
                    sys.stdout.flush()
                    flushed= True
                raise IOError(msg)
        if rc:
            if not flushed:
                sys.stdout.flush()
            msg="error, 'svn update' failed"
            raise IOError(msg)
