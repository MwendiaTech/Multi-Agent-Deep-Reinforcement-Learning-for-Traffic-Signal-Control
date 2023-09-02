"""patch file support."""

# pylint: disable=invalid-name

import os
import subprocess
import sumolib.system
import sumolib.fileurl

__version__="4.4" #VERSION#

assert __version__==sumolib.system.__version__
assert __version__==sumolib.fileurl.__version__

def assert_patch():
    """ensure that patch exists."""
    sumolib.system.test_program("patch")

def call_patch(patch_file, target_dir, verbose, dry_run):
    """call the patch utility.

    This function does:
      cd target_dir && patch -p1 < patch_file
    """
    assert_patch()
    cmd= "patch -p1"
    if dry_run or verbose:
        print("> cd %s && %s < %s" % (target_dir, cmd, patch_file))
    if dry_run:
        return
    old_dir= sumolib.system.changedir(target_dir,
                                      verbose= False, dry_run= False)
    try:
        # pylint: disable=consider-using-with
        inp= open(patch_file, "r")
        p= subprocess.Popen(cmd, shell=True,
                            stdin= inp,
                            close_fds=True)
        p.wait()
    finally:
        sumolib.system.changedir(old_dir, verbose= False, dry_run= False)
        inp.close()
    if p.returncode != 0:
        raise IOError("patch %s could not be fully applied" % patch_file)

def apply_patches(destdir, patchlist, verbose, dry_run):
    """apply a list of patches to a directory."""
    ap_destdir= os.path.abspath(destdir)
    for p in patchlist:
        filename= os.path.basename(p)
        dest_path= os.path.join(ap_destdir, filename)
        sumolib.fileurl.get(p, dest_path, verbose, dry_run)
        call_patch(dest_path, destdir, verbose, dry_run)
