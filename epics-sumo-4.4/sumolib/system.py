"""System utilities.
"""

# pylint: disable=invalid-name

import os
import shutil
import subprocess

__version__="4.4" #VERSION#

# -----------------------------------------------
# basic system utilities
# -----------------------------------------------

# standard set of environment variables here:
_new_env = dict(os.environ)

# Only on Unix-Like systems:
# Ensure that language settings for called commands are english, keep current
# character encoding:
if os.name=="posix" and "LANG" in _new_env:
    _l= _new_env["LANG"].split(".")
    if len(_l)==2:
        _l[0]= "en_US"
        _new_env["LANG"]= ".".join(_l)

def copy_env():
    """create a new environment that the user may change."""
    return dict(_new_env)

def system_rc(cmd, catch_stdout, catch_stderr, env, verbose, dry_run):
    """execute a command.

    execute a command and return the programs output
    may raise:
    IOError(errcode,stderr)
    OSError(errno,strerr)
    ValueError
    """
    # pylint: disable=too-many-arguments
    def to_str(data):
        """decode byte stream to unicode string."""
        if data is None:
            return None
        return data.decode()
    if dry_run or verbose:
        print(">", cmd)
        if dry_run:
            return (None, None, 0)
    if catch_stdout:
        stdout_par=subprocess.PIPE
    else:
        stdout_par=None

    if catch_stderr:
        stderr_par=subprocess.PIPE
    else:
        stderr_par=None
    if env is None:
        env= _new_env

    # pylint: disable=consider-using-with
    p= subprocess.Popen(cmd, shell=True,
                        stdout=stdout_par, stderr=stderr_par,
                        close_fds=True,
                        env= env
                       )
    (child_stdout, child_stderr) = p.communicate()
    # pylint: disable=E1101
    #         "Instance 'Popen'has no 'returncode' member
    return (to_str(child_stdout), to_str(child_stderr), p.returncode)

def system(cmd, catch_stdout, catch_stderr, env, verbose, dry_run):
    """execute a command with returncode.

    execute a command and return the programs output
    may raise:
    IOError(errcode,stderr)
    OSError(errno,strerr)
    ValueError
    """
    # pylint: disable=too-many-arguments
    (child_stdout, child_stderr, rc)= system_rc(cmd,
                                                catch_stdout, catch_stderr,
                                                env,
                                                verbose, dry_run)
    if rc!=0:
        # pylint: disable=no-else-raise
        if catch_stderr:
            raise IOError(rc,
                          "cmd \"%s\", errmsg \"%s\"" % (cmd,child_stderr))
        else:
            raise IOError(rc,
                          "cmd \"%s\", rc %d" % (cmd, rc))
    return (child_stdout, child_stderr)

def os_remove(dir_, verbose, dry_run):
    """call os.remove with verbose and dry_run support."""
    if verbose or dry_run:
        print(">>> os.remove(%s)" % repr(dir_))
    if dry_run:
        return
    os.remove(dir_)

def os_rename(src, dest, verbose, dry_run):
    """call os.rename with verbose and dry_run support."""
    if verbose or dry_run:
        print(">>> os.rename(%s, %s)" % (repr(src), repr(dest)))
    if dry_run:
        return
    os.rename(src, dest)

def os_rmdir(dir_, verbose, dry_run):
    """call os.rmdir with verbose and dry_run support."""
    if verbose or dry_run:
        print(">>> os.rmdir(%s)" % repr(dir_))
    if dry_run:
        return
    os.rmdir(dir_)

def os_makedirs(dir_, verbose, dry_run):
    """call os.makedirs with verbose and dry_run support."""
    if verbose or dry_run:
        print(">>> os.makedirs(%s)" % repr(dir_))
    if dry_run:
        return
    os.makedirs(dir_)

def shutil_move(src, dest, verbose, dry_run):
    """call shutil.move with verbose and dry_run support."""
    if verbose or dry_run:
        print(">>> shutil.move(%s, %s)" % (repr(src), repr(dest)))
    if dry_run:
        return
    shutil.move(src, dest)

def shutil_copyfile(src, dest, verbose, dry_run):
    """call shutil.copyfile with verbose and dry_run support."""
    if verbose or dry_run:
        print(">>> shutil.copyfile(%s, %s)" % (repr(src), repr(dest)))
    if dry_run:
        return
    shutil.copyfile(src, dest)

def changedir(newdir, verbose, dry_run):
    """return the current dir and change to a new dir.

    If newdir is empty, return <None>.
    """
    if not newdir:
        return None
    cwd= os.getcwd()
    if verbose or dry_run:
        print(">>> os.chdir(%s)" % repr(newdir))
    if not dry_run:
        os.chdir(newdir)
    return cwd

program_tests= set()

def test_program(cmd):
    """test if a program exists."""
    if cmd in program_tests:
        # already checked
        return
    try:
        system(cmd+" --version", True, True, None, False, False)
    except IOError as e:
        if "not found" in str(e):
            raise IOError("Error, %s: command not found" % cmd) from e
        raise e from e
    program_tests.add(cmd)

def _test():
    """perform internal tests."""
    import doctest # pylint: disable= import-outside-toplevel
    doctest.testmod()

if __name__ == "__main__":
    _test()
