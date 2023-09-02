"""Special sumo command completion functions."""

# pylint: disable=invalid-name

import sys
import os.path
import time
import sumolib.system
import sumolib.ModuleSpec
import sumolib.Dependencies

if __name__ == "__main__":
    # if this module is directly called like a script, we have to add the path
    # ".." to the python search path in order to find modules named
    # "sumolib.[module]".
    sys.path.append("..")

__version__="4.4" #VERSION#

assert __version__==sumolib.system.__version__
assert __version__==sumolib.ModuleSpec.__version__
assert __version__==sumolib.Dependencies.__version__

CACHING_ENABLED= True

DBCACHE=os.path.join(os.environ["HOME"], ".dbcache.sumo")
BUILDCACHE=os.path.join(os.environ["HOME"], ".buildcache.sumo")
MAX_AGE=30

SHELL= os.path.basename(os.environ.get("SHELL",""))
# e.g. "", "zsh" or "bash"

def dummy():
    """callback dummy func."""
    raise AssertionError("callback function not initialized")

# this callback must be set:
db_cache_callback= dummy
build_cache_callback= dummy

# -----------------------------------------------
# module completion utilities
# -----------------------------------------------

def touch(fname, times=None):
    """do "touch" on a file."""
    with open(fname, 'a'): # open/create file
        os.utime(fname, times)

def db_cache():
    """create a module cache in $HOME/.sumo.modulecache if needed.

    returns the cache data.
    """
    if db_cache_callback is None:
        raise AssertionError("Error db_cache_callback is not initialized")

    if CACHING_ENABLED and os.path.exists(DBCACHE):
        # file age in seconds
        age= time.time() - os.path.getmtime(DBCACHE)
        if age<MAX_AGE:
            touch(DBCACHE)
            db= sumolib.Dependencies.DB.from_pickle_file(DBCACHE)
            return db
    # pylint: disable=E1111
    #                        Assigning to function call which doesn't return
    db= db_cache_callback()
    if CACHING_ENABLED:
        db.pickle_save(DBCACHE)
    return db

def build_cache():
    """create a module cache in $HOME/.sumo.modulecache if needed.

    returns the cache data.
    """
    if build_cache_callback is None:
        raise AssertionError("Error build_cache_callback is not initialized")

    if CACHING_ENABLED and os.path.exists(BUILDCACHE):
        # file age in seconds
        age= time.time() - os.path.getmtime(BUILDCACHE)
        if age<MAX_AGE:
            touch(BUILDCACHE)
            db= sumolib.Builds.DB_overlay.from_pickle_file(BUILDCACHE)
            return db
    # pylint: disable=E1111
    #                        Assigning to function call which doesn't return
    builddb= build_cache_callback()
    if CACHING_ENABLED:
        builddb.pickle_save(BUILDCACHE)
    return builddb

def clear_db_cache():
    """remove the db cache."""
    if CACHING_ENABLED and os.path.exists(DBCACHE):
        # file age in seconds
        age= time.time() - os.path.getmtime(DBCACHE)
        if age>=MAX_AGE:
            sumolib.system.os_remove(DBCACHE, verbose= False, dry_run= False)

def clear_build_cache():
    """remove the build cache."""
    if CACHING_ENABLED and os.path.exists(BUILDCACHE):
        # file age in seconds
        age= time.time() - os.path.getmtime(BUILDCACHE)
        if age>=MAX_AGE:
            sumolib.system.os_remove(BUILDCACHE,
                                     verbose= False, dry_run= False)

def clear_caches():
    """clear all caches."""
    clear_db_cache()
    clear_build_cache()

# -----------------------------------------------
# completion functions
# -----------------------------------------------

def module(module_, _):
    """complete a module name."""
    db= db_cache()
    if not module_:
        # just return a list of all modules
        return db.iter_modulenames()
    return [m for m in db.iter_modulenames() if m.startswith(module_)]

def version(module_par_name, ver, result):
    """complete a module version name."""
    db= db_cache()
    try:
        vers= list(db.iter_versions(result.get(module_par_name)))
    except AttributeError as _:
        return []
    except KeyError as _:
        return []
    if not ver:
        return vers
    return [v for v in vers if v.startswith(ver)]

def moduleversion(module_, _):
    """try to give a sensible completion list to a module.
    """
    # pylint: disable=R0911
    #                          Too many return statements
    db= db_cache()
    if not module_:
        # just return a list of all modules
        return db.iter_modulenames()
    if ":" not in module_:
        modules= [m for m in db.iter_modulenames() if m.startswith(module_)]
        if not modules:
            return []
        if len(modules)>1:
            return modules
        # exactly one module_ remains
        module_= modules[0]
        l= ["%s:%s" % (module_,v) for v in db.iter_versions(module_)]
        return l
    (module_,version_)= module_.split(":", 1)
    try:
        db.assert_module(module_,None)
    except KeyError:
        # module_ does not exist
        return []
    versions= [ver for ver in db.iter_versions(module_) \
                   if ver.startswith(version_)]
    if not versions:
        # no version_ matches
        return []

    # for zsh we have to return complete modulespecs,
    # for bash the versions are sufficient:
    if SHELL=="zsh":
        rversions= ["%s:%s" % (module_,v) for v in versions]
    else:
        rversions= versions

    if len(versions)==1:
        if versions[0]!=version_:
            # must still complete
            return rversions
        # exact match, nothing more to do unless the user enters a space which
        # we would here see as a "." parameter:
        return []
    return rversions

def dependency(module_par_name, dep, result):
    """try to complete a dependency for a given module.
    """
    db= db_cache()
    try:
        m= sumolib.ModuleSpec.Spec.from_string(result.get(module_par_name))
    except AttributeError as _:
        return []
    except ValueError as _:
        return []
    if not m.is_exact_spec():
        return []
    deps= list(db.iter_dependencies(m.modulename, m.versionname))
    if not dep:
        return deps
    return [d for d in deps if d.startswith(dep)]

def builds(build, _):
    """complete a build name."""
    builddb= build_cache()
    builds_= list(builddb.iter_builds())
    if not build:
        # just return a list of all builds_
        return builds_
    return [b for b in builds_ if b.startswith(build)]
