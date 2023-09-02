# -*- coding: UTF-8 -*-
"""JSON utilities.
"""

# pylint: disable=invalid-name, wrong-import-position

import sys
import json

if __name__ == "__main__":
    # if this module is directly called like a script, we have to add the path
    # ".." to the python search path in order to find modules named
    # "sumolib.[module]".
    sys.path.append("..")

import pprint
import os
import os.path
import shutil
import time
import pickle
import tempfile
import sumolib.lock
import sumolib.utils

__version__="4.4" #VERSION#

assert __version__==sumolib.lock.__version__
#assert __version__==sumolib.utils.__version__

_pyver= (sys.version_info[0], sys.version_info[1])

# -----------------------------------------------
# exceptions
# -----------------------------------------------

class ParseError(Exception):
    """This is raised when the JSON data is invalid."""

class InconsistentError(Exception):
    """This is raised when we cannot get consistent JSON data."""

# -----------------------------------------------
# JSON functions
# -----------------------------------------------

def dump_file(filename, var, mode_file):
    """Dump a variable to a file in JSON format.

    This function uses a technique to write the file atomically. It assumes
    that we have a lock on the file so the temporary filename does not yet
    exist.

    mode_file is the file we copy the file permissions from.
    """
    (f_dir, f_name)= os.path.split(filename)
    if not f_dir:
        f_dir= os.getcwd()
    (fd, tmp_filename)= tempfile.mkstemp(prefix=f_name,
                                         dir= f_dir,
                                         text= True)
    fh= os.fdopen(fd, "wt")
    # modern python JSON modules add a trailing space at lines that end with a
    # comma. It seems that this is only fixed in python 3.4. So for now we
    # remove the spaces manually here, which is done by json_str().
    fh.write(json_str(var))
    fh.flush()
    os.fsync(fh.fileno())
    fh.close()
    # copy file permissions from mode_file to tmp_filename. We have to do this
    # since mkstemp creates a file with minimal permissions, like "-rw-------":
    if not os.path.exists(mode_file):
        # No mode file exists, create one. We assume that is a portable way to
        # get the standard file permissions on any operating system:
        # pylint: disable=consider-using-with
        fh= open(mode_file, "w")
        fh.close()
        shutil.copymode(mode_file, tmp_filename)
        sumolib.system.os_remove(mode_file, verbose= False, dry_run= False)
    else:
        shutil.copymode(mode_file, tmp_filename)
    # Set modification date to [now] since shutil.copymode copied the
    # modification date from mode_file:
    os.utime(tmp_filename, None)
    sumolib.system.os_rename(tmp_filename, filename,
                             verbose= False, dry_run= False)

# pylint: disable=C0303
#                          Trailing whitespace

def json_str(var):
    """convert a variable to JSON format.

    Here is an example:

    >>> var= {"key":[1,2,3], "key2":"val", "key3":{"A":1,"B":2}}
    >>> print(json_str(var))
    {
        "key": [
            1,
            2,
            3
        ],
        "key2": "val",
        "key3": {
            "A": 1,
            "B": 2
        }
    }
    <BLANKLINE>
    """
    raw_str= json.dumps(var, sort_keys= True, indent= 4)

    # modern python JSON modules add a trailing space at lines that end
    # with a comma. It seems that this is only fixed in python 3.4. So for
    # now we remove the spaces manually here:

    lines= [x.rstrip() for x in raw_str.splitlines()]
    # effectively add a single newline at the end:
    lines.append("")
    return "\n".join(lines)

def dump(var):
    """Dump a variable in JSON format.

    Here is an example:

    >>> var= {"key":[1,2,3], "key2":"val", "key3":{"A":1,"B":2}}
    >>> dump(var)
    {
        "key": [
            1,
            2,
            3
        ],
        "key2": "val",
        "key3": {
            "A": 1,
            "B": 2
        }
    }
    <BLANKLINE>
    """
    print(json_str(var))

# pylint: enable=C0303
#                          Trailing whitespace

def json_load(data):
    """decode a JSON string.
    """
    return json.loads(data)

def anytxt2scalar(txt):
    """convert a simple text or JSON string to scalar.

    (python 3 version)

    Here are some examples:
    >>> anytxt2scalar('1')
    1
    >>> anytxt2scalar('true')
    True
    >>> anytxt2scalar('1.2')
    1.2
    >>> anytxt2scalar('abc')
    'abc'
    >>> anytxt2scalar('1')
    1
    >>> anytxt2scalar('Ä')
    'Ä'
    >>> anytxt2scalar('')
    ''
    """
    if not isinstance(txt, str):
        raise TypeError("error, argument must be of type str, not %s" % \
                        type(txt))
    ret= None
    try:
        ret= json.loads(txt)
    except ValueError as _:
        pass
    if ret is None:
        try:
            ret= json.loads('"'+txt+'"')
        except ValueError as e:
            raise ValueError("error, invalid string: %s" % repr(txt)) from e
    return ret

def loadfile(filename):
    """load a JSON file.

    If filename is "-" read from stdin.
    """
    # pylint: disable=consider-using-with
    if filename != "-":
        fh= open(filename)
    else:
        fh= sys.stdin

    try:
        results= json.load(fh)
    except ValueError as e:
        if filename != "-":
            msg= "file %s: %s" % (filename, str(e))
            fh.close()
        else:
            msg= "<stdin>: %s" % str(e)
        # always re-raise as a value error:
        raise ParseError(msg) from e
    except IOError as e:
        if filename != "-":
            msg= "file %s: %s" % (filename, str(e))
            fh.close()
        else:
            msg= "<stdin>: %s" % str(e)
        raise e.__class__(msg)
    if filename != "-":
        fh.close()
    return results

class Container():
    """an object that is a python structure.

    This is a dict that contains other dicts or lists or strings or floats or
    integers.
    """
    def selfcheck(self, msg):
        """raise an exception if the object is not valid."""
        # pylint: disable=W0613
        #                          Unused argument
        # pylint: disable=R0201
        #                          Method could be a function
        return
    def __init__(self, dict_= None, use_lock= True, timeout= None):
        """create the object."""
        if dict_ is None:
            self.dict_= {}
        else:
            self.dict_= dict_
        self.lock= None
        self._use_lock= use_lock
        self._filename= None
        self.timeout= timeout
    def filename(self, new_name= None):
        """return or set the internal filename."""
        if new_name is None:
            return self._filename
        if new_name==self._filename:
            return None
        # remove old locks that may exist:
        self.unlock_file()
        self._filename= new_name
        return None
    def dirname(self):
        """return the directory part of the internal filename."""
        return os.path.dirname(self._filename)
    def lock_file(self):
        """lock a file and store filename and lock in the object."""
        if not self._use_lock:
            return
        if not self._filename:
            raise ValueError("cannot lock JSON object: filename is not set")
        if self.lock:
            # already locked
            return
        lk= sumolib.lock.MyLock(self._filename, self.timeout)
        # may raise lock.LockedError, lock.AccessError or OSError:
        lk.lock()
        self.lock= lk
    def unlock_file(self):
        """remove a filelock if there is one."""
        if not self._use_lock:
            return
        if self.lock:
            self.lock.unlock()
            self.lock= None
    def __del__(self):
        """object destructor."""
        # When a derived class raises an exception *before* __init__ of *this*
        # class is called, the object is not properly constructed. Nevertheless
        # python will call the __del__() method. self.unlock_file() will then
        # fail. We handle this by testing first if the attribute "dict_"
        # exists. Only if this exists, self.unlock_file() is called.
        if getattr(self, "dict_", None) is None:
            return
        self.unlock_file()
    def datadict(self):
        """return the internal dict."""
        return self.dict_
    def to_dict(self):
        """return the object as a dict."""
        return self.dict_
    def __repr__(self):
        """return a repr string."""
        return "%s(%s)" % (self.__class__.__name__,
                           pprint.pformat(self.to_dict()))
    def __str__(self):
        """return a human readable string."""
        txt= ["%s:" % self.__class__.__name__]
        txt.append(pprint.pformat(self.to_dict(), indent=2))
        return "\n".join(txt)
    @classmethod
    def from_json(cls, json_data):
        """create an object from a json string."""
        obj= cls(json_load(json_data))
        obj.selfcheck("(created from JSON string)")
        return obj
    @classmethod
    def from_json_file(cls, filename,
                       use_lock,
                       keep_lock,
                       timeout= None):
        """create an object from a json file.

        """
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        if not isinstance(keep_lock, bool):
            raise TypeError("wrong type of keep_lock")
        if filename=="-":
            result= cls(loadfile(filename))
            result.selfcheck("(created from JSON string on stdin)")
            return result
        if not os.path.exists(filename):
            raise IOError("file \"%s\" not found" % filename)
        l= None
        if not use_lock:
            # load the file the simple way:
            data= loadfile(filename)
        else:
            # use locking
            l= sumolib.lock.MyLock(filename, timeout)
            # may raise lock.LockedError, lock.AccessError or OSError:
            try:
                l.lock()
            except sumolib.lock.AccessError as _:
                if keep_lock:
                    # we cannot keep the lock since we cannot create it, this
                    # is an error:
                    raise
                # we cannot create a lock but try to continue anyway:
                l= None

            if l is not None:
                # regular locking
                try:
                    data= loadfile(filename)
                finally:
                    if not keep_lock:
                        l.unlock()
                        l= None
            else:
                # We cannot create a file lock but be we try to read
                # consistently: it must be valid JSON and the file modification
                # date must not change.
                tmo= timeout
                while True:
                    t1= os.path.getmtime(filename)
                    try:
                        data= loadfile(filename)
                    except ParseError as _:
                        if tmo<=0:
                            raise
                        # if there is a timeout specified, try again:
                        tmo-=1
                        time.sleep(1)
                        continue
                    t2= os.path.getmtime(filename)
                    if t2!=t1:
                        # file modification time changed, we have to read again
                        # unless the time is expired:
                        if tmo<=0:
                            raise InconsistentError("File %s: cannot lock "
                                                    "and cannot read "
                                                    "consistently" % filename)
                        tmo-=1
                        time.sleep(1)
                        continue
                    break

        result= cls(data, use_lock, timeout)
        result.lock= l
        result.filename(filename)
        result.selfcheck("(created from JSON file %s)" % filename)
        return result
    def json_string(self):
        """return a JSON representation of the object."""
        return json_str(self.to_dict())
    def json_print(self):
        """print a JSON representation of the object."""
        print(self.json_string())
    def json_save(self, filename, verbose, dry_run):
        """save as a JSON file.

        If filename is empty, use the default filename.

        Always remove a file lock if it existed before.
        """
        # pylint: disable=R0912
        #                          Too many branches
        if filename=="-":
            raise ValueError("filename must not be \"-\"")
        if filename:
            if (self._filename!=filename) and not dry_run:
                # remove a lock that may still exist:
                # unlocks only of self._use_lock==True:
                self.unlock_file()
            self._filename= filename
        try:
            if not dry_run:
                # locks only of self._use_lock==True:
                self.lock_file()
            backup= sumolib.utils.backup_file(self._filename,
                                              verbose, dry_run)
            if dry_run:
                print("# create JSON file %s" % repr(self._filename))
            else:
                dump_file(self._filename, self.to_dict(), backup)
        finally:
            # unlocks only of self._use_lock==True:
            if not dry_run:
                self.unlock_file()
    def pickle_save(self, filename):
        """save using cPickle, don't use lockfiles or anything."""
        # Note: in python3, a pickle file must be opened in binary mode:
        with open(filename, "wb") as fh:
            pickle.dump(self.to_dict(), fh)
    @classmethod
    def from_pickle_file(cls, filename):
        """load from a cPickle file, don't use lockfiles or anything."""
        # Note: in python3, a pickle file must be opened in binary mode:
        with open(filename, "rb") as fh:
            data= pickle.load(fh)
        return cls(data)

def _test():
    """perform internal tests."""
    import doctest # pylint: disable= import-outside-toplevel
    doctest.testmod()

if __name__ == "__main__":
    _test()
