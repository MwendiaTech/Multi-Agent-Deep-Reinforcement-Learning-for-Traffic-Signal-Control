"""Database file handling.
"""

# pylint: disable= invalid-name

import sys
import os.path
import sumolib.utils

if __name__ == "__main__":
    # if this module is directly called like a script, we have to add the path
    # ".." to the python search path in order to find modules named
    # "sumolib.[module]".
    sys.path.append("..")

# pylint: disable=wrong-import-position
import sumolib.ModuleSpec
import sumolib.JSON

__version__="4.4" #VERSION#

assert __version__==sumolib.ModuleSpec.__version__
assert __version__==sumolib.JSON.__version__

# -----------------------------------------------
# class definitions
# -----------------------------------------------

class DB(sumolib.JSON.Container):
    """the buildtree database."""
    # pylint: disable=R0904
    #                          Too many public methods
    states= set(("stable","testing","unstable",
                 "incomplete","disabled","broken"))
    @classmethod
    def check_state(cls, state, new_build):
        """checks if a state is allowed."""
        if not state in cls.states:
            raise ValueError("unknown state: %s" % repr(state))
        if new_build:
            if state=="disabled":
                raise ValueError("state 'disabled' not allowed for a "
                                 "new build")
    def selfcheck(self, msg):
        """raise exception if obj doesn't look like a builddb.

        This does not do a *complete* check of the datastructure, it only
        ensures that the JSON datastructure isn't something completely
        different.
        """
        def _somevalue(d):
            """return kind of arbitrary value of a dict."""
            keys= list(d.keys())
            key= keys[len(keys)//2]
            return d[key]
        while True:
            d= self.datadict()
            if not isinstance(d, dict):
                break
            if not d:
                # empty directory
                # this may be OK:
                return
            build= _somevalue(d)
            if not isinstance(build, dict):
                break
            modules= build.get("modules")
            if not modules:
                break
            if not isinstance(modules, dict):
                break
            module= _somevalue(modules)
            if not isinstance(module, str):
                break
            return
        raise ValueError("error: builddb data is invalid %s" % msg)
    def generate_buildtag(self, buildtag_stem):
        """generate a new buildtag.

        A new buildtag in the form "STEM-nnn" is generated.
        """
        # determine which number to append:
        no= -1
        buildtag_stem= buildtag_stem + "-"
        for b in self.iter_builds():
            if b.startswith(buildtag_stem):
                b= b.replace(buildtag_stem,"")
                try:
                    n= int(b)
                except ValueError as _:
                    continue
                if n>no:
                    no= n
        if no<=-1:
            no= 0
        no+= 1
        return "%s%03d" % (buildtag_stem, no)
    @staticmethod
    def is_generated_buildtag(buildtag):
        """return True of the buildtag was generated."""
        return buildtag.startswith("AUTO-")
    def __init__(self, dict_= None, use_lock= True, lock_timeout= None):
        """create the object."""
        super().__init__(dict_, use_lock, lock_timeout)
    def merge(self, other):
        """merge with another builddb.

        Returns the list of new added builds.
        """
        if not isinstance(other, DB):
            raise AssertionError("error, <other> must be of type %s" % \
                                 DB)
        d= self.datadict()
        od= other.datadict()
        new_builds= set()
        ignored_builds= set()
        for b in other.iter_builds():
            if self.has_build_tag(b):
                ignored_builds.add(b)
                continue
            # note: this is *NOT* a deepcopy, just the reference is copied:
            d[b]= od[b]
            new_builds.add(b)
        return (new_builds, ignored_builds)
    def is_empty(self):
        """shows of the object is empty."""
        return not bool(self.datadict())
    def delete(self, build_tag):
        """delete a build."""
        d= self.datadict()
        del d[build_tag]
    def has_build_tag(self, build_tag):
        """returns if build_tag is contained."""
        return build_tag in self.datadict()
    def new_build(self, build_tag, state):
        """create a new build with the given state.
        """
        # may raise ValueError:
        self.__class__.check_state(state, new_build= True)
        d= self.datadict()
        if build_tag in d:
            raise ValueError("cannot create, build %s already exists" % \
                               build_tag)
        d[build_tag]= { "state": state }
    def is_incomplete(self, build_tag):
        """returns True if the build is marked incomplete.
        """
        d= self.datadict()
        return d[build_tag]["state"] == "incomplete"
    def is_disabled(self, build_tag):
        """returns True if the build is marked disabled.
        """
        d= self.datadict()
        return d[build_tag]["state"] == "disabled"
    def is_stable(self, build_tag):
        """returns True if the build is marked stable.
        """
        d= self.datadict()
        return d[build_tag]["state"] == "stable"
    def is_testing_or_stable(self, build_tag):
        """returns True if the build is marked testing or stable.
        """
        d= self.datadict()
        s= d[build_tag]["state"]
        # pylint: disable=consider-using-in
        return (s=="testing") or (s=="stable")
    def is_unstable(self, build_tag):
        """returns True if the build is marked testing or stable.
        """
        d= self.datadict()
        s= d[build_tag]["state"]
        return s=="unstable"
    def state(self, build_tag):
        """return the state of the build."""
        d= self.datadict()
        return d[build_tag]["state"]
    def change_state(self, build_tag, new_state):
        """sets the state to a new value."""
        # may raise ValueError:
        self.__class__.check_state(new_state, new_build= False)
        d= self.datadict()
        d[build_tag]["state"]= new_state
    def is_fully_linked(self, build_tag):
        """returns True if the build consists *only* of links."""
        build_= self.datadict()[build_tag]
        modules_= build_["modules"]
        linked_ = build_.get("linked")
        if not linked_:
            return False
        if len(modules_)>len(linked_):
            return False
        return True
    def add_build(self, other, build_tag):
        """add build data from another Builddb to this one.

        Note: this does NOT do a deep copy, it copies just references.
        """
        d= self.datadict()
        if build_tag in d:
            raise ValueError("cannot add, build %s already exists" % build_tag)
        d[build_tag]= other.datadict()[build_tag]
    def add_module(self, build_tag,
                   module_build_tag,
                   modulename, versionname):
        """add a module definition."""
        build_= self.datadict().setdefault(build_tag, {})
        modules_= build_.setdefault("modules", {})
        modules_[modulename]= versionname
        if build_tag!= module_build_tag:
            linked_ = build_.setdefault("linked", {})
            linked_[modulename]= module_build_tag
    def has_module(self, build_tag, modulename):
        """returns if the module is contained here."""
        build_= self.datadict()[build_tag]
        module_dict= build_["modules"]
        return modulename in module_dict
    def module_version(self, build_tag, modulename):
        """returns the version of the module or None."""
        build_= self.datadict()[build_tag]
        module_dict= build_["modules"]
        return module_dict.get(modulename)

    def module_link(self, build_tag,
                    modulename):
        """return linked build_tag if the module is linked or None."""
        build_= self.datadict()[build_tag]
        linked_ = build_.get("linked")
        if linked_ is None:
            return None
        return linked_.get(modulename)
    def sortby_linkage(self, build_tags, reverse):
        """sort build so that dependencies of a build always come first."""
        taglist= sorted(build_tags)
        keys= { t: 1 for t in taglist }
        links= { t: self.linked_to(t) for t in taglist }
        loopcount=0
        changes= True
        while changes:
            loopcount+=1
            if loopcount > 100:
                sumolib.utils.errmessage(\
                    "warning: internal error, sortby_linkage failed")
                break
            changes= False
            for t in taglist:
                for d in links[t]:
                    if keys.setdefault(d, 1) >= keys[t]:
                        keys[t]= keys[d]+1
                        changes= True
        if not reverse:
            l= sorted(taglist, key= lambda tag: (keys[tag],tag))
        else:
            l= sorted(taglist, key= lambda tag: (-keys[tag],tag))
        return l
    def linked_to(self, build_tag):
        """returns all builds this build is linked to."""
        build_= self.datadict()[build_tag]
        linked_ = build_.get("linked")
        s= set()
        if linked_ is None:
            return s
        for v in linked_.values():
            s.add(v)
        return s
    def is_linked_to(self, build_tag, other_build_tag):
        """returns True if there are links to other_build_tag."""
        build_= self.datadict()[build_tag]
        linked_ = build_.get("linked")
        if linked_ is None:
            return False
        for v in linked_.values():
            if v== other_build_tag:
                return True
        return False
    def linked_builds(self, build_tag):
        """return a set of tags of all builds that depend on this.
        """
        dependends= set()
        for b in self.iter_builds():
            if self.is_linked_to(b, build_tag):
                dependends.add(b)
        return dependends
    def rec_linked_builds(self, build_tag):
        """return a set of tags of all builds that recursively depend on this.
        """
        all_= set((build_tag,))
        checked= set()
        while len(checked)!=len(all_):
            for b in all_.difference(checked):
                checked.add(b)
                all_.update(self.linked_builds(b))
        all_.remove(build_tag)
        return all_
    def check_by_modulespecs(self, modulespecs):
        """checks which builds match or partially match the modulespecs.

        returns: a dict
          { buildtag : { "matched": matched_modules,
                         "wrongversion": wrong_version_modules,
                         "missing": missing_modules,
                         "modules": {
                                      modulename: (flag, modulespec)
                                      ...
                                    }
                         ...
                       }
          }
        """
        # pylint: disable=too-many-locals
        result= {}

        if not isinstance(modulespecs, sumolib.ModuleSpec.Specs):
            raise TypeError("wrong type: '%s'" % repr(modulespecs))
        modulespecs= modulespecs.sorted()
        for build_tag in self.iter_builds():
            this_build_result= {}
            missing_cnt=0
            wrong_version_cnt=0
            match_version_cnt=0
            m= self.modules(build_tag)
            for modulespec in modulespecs:
                modulename= modulespec.modulename
                v= m.get(modulename)
                if v is None:
                    # module is not part of build:
                    res= ("-", modulename)
                    missing_cnt+= 1
                else:
                    spec_st= sumolib.ModuleSpec.Spec(modulename, v,
                                                     "eq").to_string()
                    if not modulespec.test(v):
                        res= ("!=", spec_st)
                        wrong_version_cnt+= 1
                    elif modulespec.equal(v):
                        res= ("==", spec_st)
                        match_version_cnt+= 1
                    else:
                        res= ("=~", spec_st)
                        match_version_cnt+= 1
                this_build_result[modulename]= res
            if wrong_version_cnt!=0 or match_version_cnt!=0:
                result[build_tag]= { "matched": match_version_cnt,
                                     "wrongversion": wrong_version_cnt,
                                     "missing": missing_cnt,
                                     "modules": this_build_result
                                   }
        return result

    def filter_by_modulespecs(self, modulespecs):
        """return a new Builddb that satisfies the given list of specs.

        Note that this function treats versions like "R1-3" and "1-3" to be
        different.
        """
        if not isinstance(modulespecs, sumolib.ModuleSpec.Specs):
            raise TypeError("wrong type: '%s'" % repr(modulespecs))
        new= self.__class__()
        for build_tag in self.iter_builds():
            found= True
            m= self.modules(build_tag)
            for modulespec in modulespecs:
                modulename= modulespec.modulename
                v= m.get(modulename)
                if v is None:
                    found= False
                    break
                if not modulespec.test(v):
                    found= False
                    break
            if found:
                new.add_build(self, build_tag)
        return new
    def iter_builds(self):
        """return a build iterator.
        """
        for t in sorted(self.datadict().keys()):
            yield t
    def iter_modules(self, build_tag):
        """return an iterator on the modules."""
        build_= self.datadict()[build_tag]
        module_dict= build_["modules"]
        for module in sorted(module_dict.keys()):
            yield (module, module_dict[module])
    def modules(self, build_tag):
        """return all modules of a build.

        The returned structure is a dictionary mapping modulenames to
        versionnames.
        """
        build_ = self.datadict()[build_tag]
        return build_["modules"]
    def module_specs(self, build_tag):
        """return the modules of a build in form module spec strings.

        This function returns a list of strings that ccan be parsed by
        sumolib.ModuleSpec.Spec.from_string().
        """
        lst= []
        build_dict= self.modules(build_tag)
        for modulename in sorted(build_dict.keys()):
            versionname= build_dict[modulename]
            m= sumolib.ModuleSpec.Spec(modulename, versionname, "eq")
            lst.append(m.to_string())
        return lst

class DB_overlay(DB):
    """Implement a builddb with overlays.

    Overlays are other build databases that are added to the local build
    database but cannot be modified and whose build specifications are not
    saved when the object is saved.
    """
    # pylint: disable=R0904
    #                          Too many public methods
    def __init__(self, dict_= None, use_lock= True, lock_timeout= None):
        """create the object."""
        super().__init__(dict_, use_lock, lock_timeout)
        self.overlay_keys= {}
        self.overlay_files= []
        self.overlay_mode= True
        self.ignored_keys= set()
    def overlaymode(self, new_mode= None):
        """get or set the overlay mode.

        overlay_mode True:
            All JSON representations of the object do not contain builds that
            were added with overlay().
            Builds added with overlay() cannot be modified.
        overlay_mode False:
            All JSON representations of the object contain all the builds.
            Builds added with overlay() can be modified.
        """
        if new_mode is None:
            return self.overlay_mode
        self.overlay_mode= new_mode
        return None
    def overlay(self, filename, use_lock= True):
        """merge with another builddb from a file."""
        other= DB.from_json_file(filename, use_lock= use_lock,
                                 keep_lock= False)
        (new_keys, ignored_keys)= self.merge(other)
        if ignored_keys:
            sumolib.utils.errmessage(\
                ("Warning: The following build tags in %s were ignored "
                 "since they already exist in %s:") % \
                 (filename, self._filename))
            sumolib.utils.errmessage(" ".join(sorted(ignored_keys)))
            # list of builds:
            # (sumo build list 2>&1 >/dev/null) | tail -n +1

        self.overlay_files.append(filename)
        idx= len(self.overlay_files)-1
        for k in new_keys:
            self.overlay_keys[k]= idx
    def tag_is_overlayed(self, build_tag):
        """return True if build_tag is from overlayed builddb."""
        return build_tag in self.overlay_keys
    def filename_from_tag(self, build_tag):
        """return the name of the builddb file from a tag."""
        if not self.tag_is_overlayed(build_tag):
            return self.filename() # from class JSON.Container
        return self.overlay_files[self.overlay_keys[build_tag]]
    def dirname_from_tag(self, build_tag):
        """return the name of the builddb directory from a tag."""
        return os.path.dirname(self.filename_from_tag(build_tag))
    def delete(self, build_tag):
        """delete a build."""
        if self.overlay_mode and (self.tag_is_overlayed(build_tag)):
            raise ValueError(("error, build '%s' is not in local build "
                              "directory due to your 'sumo config local' "
                              "configuration") % build_tag)
        super().delete(build_tag)
    def change_state(self, build_tag, new_state):
        """sets the state to a new value."""
        if self.overlay_mode and (self.tag_is_overlayed(build_tag)):
            raise ValueError(("error, build '%s' is not in local build "
                              "directory due to your 'sumo config local' "
                              "configuration") % build_tag)
        super().change_state(build_tag, new_state)
    def to_dict(self):
        """return the object as a dict.

        By overriding this method, we change all JSON representations of the
        object.
        """
        if not self.overlay_mode:
            return super().to_dict()
        return { k:v for (k,v) in \
                           super().to_dict().items() \
                           if k not in self.overlay_keys }

class BuildCache(sumolib.JSON.Container):
    """Detailed dependency information.

    Taken from sumo-scan and from the build database.
    Datastructure::

      { "modulename": { "versionname": { "depmodule" :
                                         {
                                           "depvers1": state,
                                           "depvers2": state
                                         }
                                       }
                      }
      }

    Note: "depvers" is the version of "depmodule", "state" is the state of the
    build that depmodule:depvers is part of.
    """
    def __init__(self, dict_= None, use_lock= True, lock_timeout= None):
        """create the object."""
        super().__init__(dict_, use_lock, lock_timeout)
    def add_dependency(self, modulename, versionname,
                       dep_name, dep_version, state):
        """add a single dependency with a state."""
        # pylint: disable=R0913
        #                          Too many arguments
        d= self.datadict()
        versiondict   = d.setdefault(modulename, {})
        depmoduledict = versiondict.setdefault(versionname, {})
        depversiondict= depmoduledict.setdefault(dep_name, {})
        depversiondict[dep_version]= state
    def update_from_builddb(self, builddb, db):
        """update data from a builddb.

        Note: Builds that are disabled, incomplete or unstable are
              ignored !
        """
        # pylint: disable=R0914
        #                          Too many local variables
        d= self.datadict()
        for buildtag in builddb.iter_builds():
            state= builddb.state(buildtag)
            # skip builds marked "disabled":
            if builddb.is_disabled(buildtag):
                continue
            # skip builds marked "incomplete":
            if builddb.is_incomplete(buildtag):
                continue
            # skip builds marked "unstable":
            if builddb.is_unstable(buildtag):
                continue
            # set per build, contains (modulename,versionname)
            build_dict= {}
            for modulename, versionname in builddb.iter_modules(buildtag):
                build_dict[modulename]= versionname
            for (modulename, versionname) in build_dict.items():
                versiondict   = d.setdefault(modulename, {})
                depmoduledict = versiondict.setdefault(versionname, {})
                try:
                    dep_names= list(db.iter_dependencies(modulename,
                                                         versionname))
                except KeyError as _:
                    sumolib.utils.errmessage(\
                        ("WARNING: build '%s', module '%s:%s' not "
                         "in dependency db!" % \
                         (buildtag,modulename,versionname)))
                    continue
                for dep_name in dep_names:
                    v= build_dict.get(dep_name)
                    if v is not None:
                        depversiondict= depmoduledict.setdefault(dep_name, {})
                        depversiondict[v]= state

    def was_built(self, modulename, versionname):
        """return True when the module was built sometime.
        """
        d= self.datadict()
        versiondict   = d.get(modulename)
        if not versiondict:
            return False
        return versionname in versiondict
    def relation(self, modulename, versionname, dep_name, dep_version):
        """return the relation between two modules.

        None: unrelated
        <state>: built together in a build with state <state>.
        """
        d= self.datadict()
        versiondict   = d.get(modulename)
        if not versiondict:
            return None
        depmoduledict = versiondict.get(versionname)
        if not depmoduledict:
            return None
        depversiondict= depmoduledict.get(dep_name)
        if not depversiondict:
            return None
        return depversiondict.get(dep_version)

def _test():
    """perform internal tests."""
    import doctest # pylint: disable= import-outside-toplevel
    doctest.testmod()

if __name__ == "__main__":
    _test()
