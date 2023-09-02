"""mercurial support
"""

# pylint: disable=invalid-name

import os.path
import re
import time
import sys

import sumolib.system
import sumolib.utils
import sumolib.lock

__version__="4.4" #VERSION#

assert __version__==sumolib.system.__version__

def TRACE(st):
    """trace message"""
    sys.stdout.flush()
    sys.stderr.write("%s\n" % st)
    sys.stderr.flush()

def PTRACE(st, verbose):
    """trace message"""
    if verbose:
        time.sleep(1)
        print("%s\n" % st)

# -----------------------------------------------
# CVS properties
# -----------------------------------------------

def _first_line(path):
    """return the first line of a text file."""
    # pylint: disable=consider-using-with
    f= open(path, "r")
    for line in f:
        f.close()
        return line

def _cvs_root(path):
    """get first line of CVS/Root."""
    return _first_line(os.path.join(path,"CVS/Root")).strip()

def _cvs_repository(path):
    """get first line of CVS/Repository."""
    return _first_line(os.path.join(path,"CVS/Repository")).strip()

def _make_url(root, repo):
    """Create a sumo url from CVS Root and Repository.
    """
    path= os.path.join(root, repo)
    if ":" in repo:
        if path.startswith(":ext:"):
            path= path.replace(":ext:", "", 1)
        return "ssh://%s" % path
    return path

def _parse_url(url):
    """parse a sumo URL and create paths for CVS.

    returns:
      (cvs_root, repo_name, is_ssh)
    """
    is_ssh= False
    if url.startswith("ssh://"):
        is_ssh= True
        path= url.replace("ssh://", "")
        path= ":ext:" + path
    elif url.startswith("file://"):
        path= url.replace("file://", "")
    else:
        path= url
    (root, name)= os.path.split(path)
    return(root, name, is_ssh)

_old_cvs_ssh= None

def _cvs_set_ssh():
    """enable ssh in cvs.
    """
    # pylint: disable=global-statement
    global _old_cvs_ssh
    _old_cvs_ssh= os.environ.get("CVS_RSH")
    os.environ["CVS_RSH"]= "ssh"

def _cvs_unset_ssh():
    """set CVS_RSH to it's old state."""
    if _old_cvs_ssh is None:
        del os.environ["CVS_RSH"]
    else:
        os.environ["CVS_RSH"]= _old_cvs_ssh

# -----------------------------------------------
# CVS status matcher
# -----------------------------------------------

def _cvs_managed_subdirs(path):
    """return CVS managed subdirectories.

    Note: directories without files are skipped.
    """
    dirs=[]
    for(dirpath, dirnames, filenames) in sumolib.utils.dirwalk(path):
        if not "CVS" in dirnames:
            # skip directories not managed by CVS:
            continue
        if os.path.split(dirpath)[-1]=="CVS":
            # skip the CVS directories
            continue
        if not filenames:
            continue
        dirs.append(dirpath)
    return dirs

def _regexp_groups(rx, st):
    """match a regexp and return captured values."""
    m= rx.match(st)
    if m is None:
        return None
    return [s.strip() for s in m.groups()]

_rx_stat_file=re.compile(r'^File:\s+(.*)\s+Status:\s*(.*)')
_rx_stat_stickytag=re.compile(r'^Sticky Tag:\s+(\S+)')
_rx_stat_workingrev=re.compile(r'^Working revision:\s+(\S+)')

def _cvs_dir_status(path, verbose, dry_run):
    """parse "cvs status" for a single directory.

    Returns a dictionary of the form:
      { FILE1 : { "rev": REVISION,
                 "tag": TAG
                },
        FILE2 : { ... }
        ...
      }
    """
    cmd="cvs status -l \"%s\"" % path
    # since the command prints something on stderr, we catch stderr, too.
    (reply,_)= sumolib.system.system(cmd, True, True, None, verbose, dry_run)
    data= {}
    filename= None
    for line in reply.splitlines():
        line= line.strip()
        r= _regexp_groups(_rx_stat_file, line)
        if r:
            filename= os.path.join(path, r[0])
            data[filename]={}
            continue
        r= _regexp_groups(_rx_stat_stickytag, line)
        if r:
            data[filename]["tag"]= r[0]
            continue
        r= _regexp_groups(_rx_stat_workingrev, line)
        if r:
            data[filename]["rev"]= r[0]
    return data

def _cvs_status(path, verbose, dry_run):
    """parse "cvs status" for a directory tree.

    Returns a dictionary of the form:
      { PATH1 : { "rev": REVISION,
                 "tag": TAG
                },
        PATH2 : { ... }
        ...
      }

    Note: _cvs_status(".") returns for example:
      {
       './b/fileb.txt': {'tag': 'Tag1', 'rev': '1.1'},
       './sub/c/filec.txt': {'tag': 'Tag1', 'rev': '1.1'},
       './a/filea.txt': {'tag': 'Tag1', 'rev': '1.1'}
      }
    """
    cwd= sumolib.system.changedir(path, verbose, dry_run=False)
    data= {}
    dotslash= os.path.join(".","")
    try:
        for directory in _cvs_managed_subdirs("."):
            if directory.startswith(dotslash):
                directory= directory.replace(dotslash,"",1)
            data.update(_cvs_dir_status(directory, verbose, dry_run))
    finally:
        sumolib.system.changedir(cwd, verbose, dry_run=False)
    return data

# -----------------------------------------------
# Repo class
# -----------------------------------------------

def assert_cvs():
    """ensure that cvs exists."""
    sumolib.system.test_program("cvs")

class Repo():
    """represent a cvs repository."""
    # pylint: disable=R0902
    #                          Too many instance attributes
    def _tag_on_top(self):
        """returns True when a tag identifies the working copy.

        This is the case when all files of the project have the same sticky
        tag.
        Returns the found tag or None if no tag on top was found.
        """
        data= _cvs_status(self.directory, self.verbose, self.dry_run)
        tag= None
        for (_, properties) in data.items():
            t= properties.get("tag")
            if not t:
                return None
            if t=="(none)":
                return None
            if tag is None:
                # first occurence of a tag
                tag= t
                continue
            if tag!=t:
                # different tag
                return None
        return tag
    def _find_remote(self, patcher):
        """find and contact the remote repository."""
        assert_cvs()
        default_repo= _make_url(_cvs_root(self.directory),
                                _cvs_repository(self.directory))
        if patcher is not None:
            default_repo= patcher.apply(default_repo)
        # try to reach the remote repository:
        (root, _, is_ssh)= _parse_url(default_repo)
        if is_ssh:
            _cvs_set_ssh()
        cmd= "cvs -n -q -d %s update %s" % (root, self.directory)
        (_,_,rc)= sumolib.system.system_rc(cmd, True, True, None,
                                           self.verbose, self.dry_run)
        if is_ssh:
            _cvs_unset_ssh()
        if rc!=0:
            # contacting the remote repo failed
            return None
        return default_repo
    def _local_changes(self, matcher):
        """returns True if there are uncomitted changes.

        Does basically "cvs -n -q update". All lines that match the matcher
        object are ignored. The matcher parameter may be <None>.
        """
        assert_cvs()
        (root, _, is_ssh)= _parse_url(self.remote_url)
        if is_ssh:
            _cvs_set_ssh()
        cmd= "cvs -n -q -d %s update %s" % (root, self.directory)
        (reply,stderr,rc)= sumolib.system.system_rc(cmd, True, True, None,
                                                    self.verbose,
                                                    self.dry_run)
        if is_ssh:
            _cvs_unset_ssh()
        if rc:
            sys.stdout.flush()
            sys.stderr.write(stderr)
            sys.stderr.flush()
            msg="error, 'cvs -n -q update' failed"
            raise IOError(msg)
        # flags from cvs update -n -q that indicate a modification:
        # A: added
        # R: removed
        # M: modified
        # C: conflict (also modified)
        mod_flags= set(("A","R","M","C"))
        changes= False
        for line in reply.splitlines():
            if len(line)>=2:
                if line[1]!=" ":
                    # not a regular flag line, ignore:
                    continue
            if line.startswith("? "):
                # ignore unknown files
                continue
            if line[0] not in mod_flags:
                continue
            if matcher is not None:
                # Up to column 2 there are flags followed by the filename.
                # ignore if the filename matches:
                if matcher.search(line[2:]):
                    continue
            # any line remaining means that there were changes:
            changes= True
            break
        return changes
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
        if self.directory is None:
            return
        # With CVS there is no global revision number for the working
        # copy, each file has it's own revision number. For this
        # reason, property current_revision is not set here.
        self.remote_url= self._find_remote(self._hint("url patcher"))
        if self.remote_url:
            # if the remote repo cannot be contacted, we cannot see if there
            # are local changes:
            self.local_changes= \
                    self._local_changes(self._hint("ignore changes"))
        if self._hint("force local"):
            raise ValueError("error, 'force local' not "
                             "supported for cvs")
        self.tag_on_top= self._tag_on_top()
    def __str__(self):
        """return a human readable representation."""
        lines= [ "cvs repo",
                 "dir: %s" % repr(self.directory),
                 "local_changes: %s" % repr(self.local_changes),
                 "remote url: %s" % repr(self.remote_url),
                 "tag on top: %s" % repr(self.tag_on_top) ]
        return "\n".join(lines)
    @staticmethod
    def name():
        """return the repo type name."""
        # pylint: disable=R0201
        #                          Method could be a function
        return "cvs"
    @staticmethod
    def distributed_repo():
        """True for distributed version controls systems, False otherwise."""
        return False
    def get_tag_on_top(self):
        """return the "tag on top" property."""
        return self.tag_on_top
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
        repodir= os.path.join(directory,"CVS")
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
        d= {"type":"cvs"}
        if self.tag_on_top is not None:
            d["tag"]= self.tag_on_top

        if self.remote_url is None:
            raise AssertionError("no remote_url")
        d["url"]= self.remote_url
        return d
    @staticmethod
    def checkout(spec, destdir, lock_timeout, verbose, dry_run):
        """spec must be a dictionary with "url" and "tag" (optional).
        """
        # pylint: disable= too-many-locals
        assert_cvs()
        url= spec.get("url")
        if url is None:
            raise ValueError("spec '%s' has no url" % repr(spec))
        (destdir_head, destdir_tail)= os.path.split(destdir)
        # Note: destdir_head may be empty but destdir_tail has always
        # a value.
        (root, repo, is_ssh)= _parse_url(url)
        # create lock since we have to create a directory with the name <repo>,
        # we rename this directory later:
        try:
            if destdir_head:
                cwd= sumolib.system.changedir(destdir_head, verbose, dry_run)
            if is_ssh:
                _cvs_set_ssh()
            cmd_l= ["cvs", "-d", root, "checkout"]
            tag= spec.get("tag")
            if tag is not None:
                cmd_l.append("-r '%s'" % tag)
            cmd_l.append(repo)
            cmd= " ".join(cmd_l)
            mylock= sumolib.lock.MyLock(repo, lock_timeout)
            mylock.lock()
            # we catch stdout and throw it away in order to keep cvs
            # quiet:
            (_, stderr, rc)= sumolib.system.system_rc(cmd, True, True, None,
                                                      verbose, dry_run)
            if rc:
                sys.stdout.flush()
                sys.stderr.write(stderr)
                sys.stderr.flush()
                msg="error, 'cvs checkout' failed"
                raise IOError(msg)
            if is_ssh:
                _cvs_unset_ssh()
            sumolib.system.os_rename(repo, destdir_tail, verbose, dry_run)
        finally:
            mylock.unlock()
            if destdir_head:
                sumolib.system.changedir(cwd, verbose, dry_run)
    def commit(self, logmessage):
        """commit changes to the repository.

        """
        # With cvs, a "commit" always contacts the central repository.
        assert_cvs()
        self.update()
        if not logmessage:
            m_param=""
            # if cvs starts an editor, we must not catch stdout:
            catch_stdout= False
        else:
            m_param=" -m '%s'" % logmessage
            # with a log message provided with "-m", cvs doesn't start an
            # editor. In order to keep it silent, we catch stdout in this case:
            catch_stdout= True
        cmd="cvs commit%s" % m_param
        try:
            cwd= sumolib.system.changedir(self.directory,
                                          self.verbose, self.dry_run)
            (_,stderr,rc)= sumolib.system.system_rc(cmd,
                                                    catch_stdout, True, None,
                                                    self.verbose,
                                                    self.dry_run)
        finally:
            sumolib.system.changedir(cwd, self.verbose, self.dry_run)
        if rc:
            sys.stdout.flush()
            sys.stderr.write(stderr)
            sys.stderr.flush()
            msg="error, 'cvs commit' failed"
            raise IOError(msg)
        self.local_changes= False
    def update(self):
        """update repo."""
        # use "-u" to update to head:
        assert_cvs()
        (root, _, is_ssh)= _parse_url(self.remote_url)
        cmd="cvs -d %s -q update %s" % (root, self.directory)
        if is_ssh:
            _cvs_set_ssh()
        (stdout,stderr,rc)= sumolib.system.system_rc(cmd, \
                                           True, True, None, \
                                           self.verbose, self.dry_run)
        if is_ssh:
            _cvs_unset_ssh()
        if stderr:
            # ensure that output on stderr is always printed to the console:
            sys.stdout.flush()
            sys.stderr.write(stderr)
            sys.stderr.flush()
        for l in stdout.splitlines()+stderr.splitlines():
            if l.startswith("C "):
                msg="error, 'cvs update' had a conflict"
                raise IOError(msg)
        if rc:
            msg="error, 'cvs update' failed"
            raise IOError(msg)
