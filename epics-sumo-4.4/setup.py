#!/usr/bin/env python
"""
setup.py file for sumo.

See http://docs.python.org/install
on how to use setup.py
"""
# pylint: disable=line-too-long

import os
import os.path
import sys

from setuptools import setup

# pylint: disable=invalid-name

if sys.version_info[0:2] < (3,2):
    sys.exit("error: python 3.2 or newer is required for this application")
# Note: The Python version is checked in:
#     setup.py, sumo, sumo-scan

base_name= 'python'

__version__="4.4" #VERSION#

# utilities -------------------------

def find_dirs(path, dirs_must_have_files):
    """find directories below a given path.

    Note: The distutils may have problems with directories that do not contain
    files but only other directories. For this, parameter dirs_must_have_files
    was added. If this is set, only directories that actually contain files are
    returned.

    here is an example of the returned data structure:
    ['doc/_build/html',
     'doc/_static',
     'doc/_build',
     'doc',
     'doc/_build/html/_sources',
     'doc/_build/doctrees',
     'doc/_build/html/_images',
     'doc/_build/html/_static']
    """
    dirs= set()
    for dirpath, _, filenames in os.walk(path):
        if dirpath==os.curdir:
            continue
        if dirs_must_have_files:
            if not filenames:
                continue
        dirs.add(dirpath)
    return list(dirs)

def find_files(path):
    """find files and directories below a given path.

    here is an example of the returned data structure:
    {'doc/_build/html': ['objects.inv', 'searchindex.js', 'index.html'],
     'doc/_build': [],
     'doc/_build/html/_sources': ['license.txt', 'index.txt']
     'doc/_build/doctrees': ['SDshell.doctree', 'license.doctree']
    }
    """
    paths= {}
    for dirpath, _, filenames in os.walk(path):
        paths[dirpath]= filenames
    return paths

def pathsplit(path):
    """splits a path into pieces.

    Here are some examples:
    >>> pathsplit("A")
    ['A']
    >>> pathsplit("A/B")
    ['A', 'B']
    >>> pathsplit("A/B/C")
    ['A', 'B', 'C']
    >>> pathsplit("A/B.x/C.y")
    ['A', 'B.x', 'C.y']
    """
    l= []
    while True:
        (head,tail)=os.path.split(path)
        l.append(tail)
        if not head:
            break
        path= head
    l.reverse()
    return l

def path_rebase(path, base):
    """rebases a path.

    Here are some examples:
    >>> path_rebase("doc/_build/html/_sources","doc/_build")
    'html/_sources'
    >>> path_rebase("doc/_build/html/_sources","doc/_build/html")
    '_sources'
    >>> path_rebase("doc/_build/html/_sources","doc")
    '_build/html/_sources'
    >>> path_rebase("doc/_build/html/_sources","doc/_bduild")
    'doc/_build/html/_sources'
    """
    path_l= pathsplit(path)
    base_l= pathsplit(base)
    if len(path_l)<len(base_l):
        return path
    for (i, base_elm) in enumerate(base_l):
        if base_elm!=path_l[i]:
            return path
    if len(path_l)==len(base_l):
        return ""
    # a bit complicated in order to make pylint happy:
    lst_= path_l[len(base_l):]
    return os.path.join(lst_[0], *lst_[1:])

def dir_glob_list(module_dir, subdir):
    """add entries for package_data.

    returns something like:
    [ "subdir/*",
      "subdir/d1/*",
      "subdir/d2/*"
    ]
    """
    dirs= find_dirs(os.path.join(module_dir, subdir), True)
    subdirs= [path_rebase(d, module_dir) for d in dirs]
    return [os.path.join(d, "*") for d in subdirs]

def data_files_make_list(install_path, source_path):
    """create data statements for arbitrary files."""
    filedict= find_files(source_path)
    data_dict= {}
    for (path,files) in filedict.items():
        subdir= path_rebase(path, source_path)
        if subdir != "":
            destpath= os.path.join(install_path, subdir)
        else:
            destpath= install_path
        for f in files:
            l= data_dict.get(destpath)
            if l is None:
                l= []
                data_dict[destpath]= l
            l.append(os.path.join(path, f))
    return list(data_dict.items())

# main      -------------------------

doc_install_dir= os.path.join("share", "doc",
                              "sumo-%s" % __version__)

html_install_dir= os.path.join(doc_install_dir, "html")

html_build_dir= os.path.join("doc","_build","html")

## create HTML documentation if it doesn't already exist:
if not os.path.exists(html_build_dir):
    sys.exit("Error, your distribution is incomplete: "
             "HTML documentation missing")

if not os.path.exists(os.path.join("sumolib","data")):
    sys.exit("Error, your distribution is incomplete: "
             "extra data files are missing")

data_files= [(doc_install_dir, ["README.rst", "RELEASES.rst", "LICENSE"])]

# add all generated html documentation to data_files:
data_files.extend(data_files_make_list(html_install_dir, html_build_dir))

name='epics-sumo'

# The following commands could be used to print dependencies:
if "deps-pypi" in sys.argv:
    sys.exit(0)
if "deps-rpm" in sys.argv:
    sys.exit(0)
if "deps-deb" in sys.argv:
    sys.exit(0)

if "bdist_rpm" in sys.argv:
    name= base_name+"-"+name

setup(name=name,
      version= __version__,
      description='Python support tools for EPICS software development',
      author='Goetz Pfeiffer',
      author_email='Goetz.Pfeiffer@helmholtz-berlin.de',
      url='https://epics-sumo.sourceforge.io',
      download_url='https://sourceforge.net/projects/epics-sumo/files',
      classifiers=[
          'Development Status :: 6 - Mature',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Natural Language :: English',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Physics',
          'Topic :: Software Development',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Utilities',
          ],

      packages=['sumolib'],
      package_dir= {'sumolib': "sumolib"},
      package_data={'sumolib': dir_glob_list("sumolib", "data") },
      # the data_files parameter is especially needed for the
      # rpm file generation:
      # NOTE: data_files is deprecated in setuptools !!
      data_files= data_files,
      license= "GPLv3",
      scripts= ['bin/sumo','bin/sumo-scan'],
     )
