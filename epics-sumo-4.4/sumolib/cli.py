"""Command line interface."""

# pylint: disable=too-many-lines, invalid-name

import sys
import glob
import os
import os.path
import time
import pprint
import sumolib.ModuleSpec
import sumolib.Dependencies
import sumolib.JSON

if __name__ == "__main__":
    # if this module is directly called like a script, we have to add the path
    # ".." to the python search path in order to find modules named
    # "sumolib.[module]".
    sys.path.append("..")

__version__="4.4" #VERSION#

assert __version__==sumolib.ModuleSpec.__version__
assert __version__==sumolib.Dependencies.__version__

HELP_NAME= "help"

HELP_OPTS= {"-h"     : HELP_NAME,
            "--help" : HELP_NAME
           }

# -----------------------------------------------
# completion utilities
# -----------------------------------------------

def complete_list(list_, element, _):
    """complete for a given list."""
    if not element:
        # just return a list of all modules
        return list_
    return [e for e in list_ if e.startswith(element)]

def complete_file(pattern, _):
    """return all files for a pattern for command completion"""
    if pattern is None:
        pattern= "*"
    else:
        if os.path.isfile(pattern):
            # file exists, do not further complete
            return []
        pattern+= "*"
    return [f for f in glob.glob(pattern) if os.path.isfile(f)]

def complete_dir(pattern, _):
    """return all files for a pattern."""
    if pattern is None:
        return [f for f in glob.glob("*") if os.path.isdir(f)]
    extra= None
    if os.path.isdir(pattern):
        extra= pattern
    g= pattern+"*"
    l= [f for f in glob.glob(g) if os.path.isdir(f)]
    if extra:
        l.append(extra)
    if l:
        return l
    # try pattern/* instead of pattern* :
    g= os.path.join(pattern,"*")
    l= [f for f in glob.glob(g) if os.path.isdir(f)]
    if extra:
        l.append(extra)
    return l

# -----------------------------------------------
# container classes
# -----------------------------------------------

class Container():
    """hold all option values."""
    @staticmethod
    def normalize_name(st):
        """remove dashes from a name."""
        if st.startswith("--"):
            st= st.replace("--","",1)
        elif st.startswith("-"):
            st= st.replace("-","",1)
        return st.replace("-","_")
    def __init__(self, initial_dict= None):
        """initialize."""
        if initial_dict is None:
            self._args= set()
        else:
            self._args= set(initial_dict.keys())
            for (k,v) in initial_dict.items():
                setattr(self, self.normalize_name(k), v)
    def declare(self, name, is_array= False):
        """declare a value as empty."""
        name= self.normalize_name(name)
        if not is_array:
            setattr(self, name, None)
        else:
            setattr(self, name, [])
        self._args.add(name)
    def get(self, name, default= None):
        """get a value, return default if it doesn't exist.
        """
        return getattr(self, self.normalize_name(name), default)
    def defined(self, name):
        """return if the attribute is set and not empty."""
        return bool(self.get(name))
    def put(self, name, value, is_array= False):
        """put a value."""
        name= self.normalize_name(name)
        if not is_array:
            # We allow on purpose to overwrite an option that was already given
            # with a new value:
            setattr(self, name, value)
            self._args.add(name)
        else:
            if name not in self._args:
                l= []
                setattr(self, name, l)
                self._args.add(name)
            else:
                l= self.get(name)
                if l is None:
                    l= []
                    setattr(self, name, l)
                elif not isinstance(l, list):
                    raise TypeError("attr %s has wrong type: %s\n" % \
                                    (name,type(l)))
            l.append(value)
    def _restore_dict(self):
        """restore value dict."""
        d= {}
        for k in self._args:
            d[k]= getattr(self, k)
        return d
    def defined_items(self):
        """return all items that are not empty.
        """
        return [k for k in self._args if self.defined(k)]
    def __repr__(self):
        """return python representation."""
        return "%s(%s)" % (self.__class__.__name__,
                           pprint.pformat(self._restore_dict()))
    def __str__(self):
        """print human representation."""
        d= self._restore_dict()
        lines= [self.__class__.__name__]
        for k in sorted(d.keys()):
            lines.append("    %s: %s" % (k, repr(d[k])))
        lines.append("")
        return "\n".join(lines)

class Arguments(Container):
    """class for arguments and commands."""

class Options(Container):
    """class for options."""

# -----------------------------------------------
# class for option specifications:
# -----------------------------------------------

class OptionSpec():
    """Spec for a command line option."""
    # pylint: disable=R0903
    #                          Too few public methods
    # pylint: disable=R0913
    #                          Too many arguments
    def __init__(self, name_str, completion= None,
                 arg_name= None, array= False,
                 arg_is_option= False,
                 value_list= None):
        """initialize the object.

        name_str:
           "--help -h" for example, the first name is the 'real name'
           "--my-opt" becomes "my_opt" as property later on
        """
        self.real_name= None
        self.names= set()
        for n in name_str.split():
            self.names.add(n)
            if self.real_name is None:
                self.real_name= Options.normalize_name(n)
                continue
        self.arg_name= arg_name
        self.arg_is_option= arg_is_option
        self.completion= completion
        self.array= array
        self.value_list= value_list
        # if there is a value_list and no completion function, use the list
        # completion:
        if not completion and value_list:
            self.completion= lambda s,o: complete_list(value_list, s, o)
    def check(self, value):
        """simple check of the options value.
        """
        if not self.value_list:
            return True
        return value in self.value_list
    def __repr__(self):
        """return python representation."""
        st= " ".join(self.names)
        return "%s(%s, %s, %s, %s, %s)" % \
                (self.__class__.__name__,
                 repr(st),
                 repr(self.completion),
                 repr(self.arg_name),
                 repr(self.array),
                 repr(self.value_list))
    def __str__(self):
        """return a human readable representation."""
        lines= [ self.__class__.__name__]
        lines.append("    real_name: %s" % self.real_name)
        lines.append("    names: %s" % (" ".join(self.names)))
        lines.append("    arg_name: %s" % self.arg_name)
        lines.append("    completion: %s" % self.completion)
        lines.append("    array: %s" % self.array)
        lines.append("    value_list: %s" % self.value_list)
        lines.append("")
        return "\n".join(lines)

class OptionSpecs():
    """hold command specfications."""
    def __init__(self, specs= None):
        """Initialize the object."""
        self.names= set()
        self.real_names= set()
        self.speclist= []
        self.specs= {}
        if specs is not None:
            for s in specs:
                self.add_spec(s)
        self.complete_word_option= None
        self.complete_new_option = None
        self.complete_attribute  = None
    def completion_options(self, attribute, word_option, new_option):
        """define the special completion options.

        word_option:
            complete the last argument further
        new_option :
            complete a new argument
        attribute  :
            the name of the attribute in "Options" that is set when completion
            is requested. The flag will have the value "word" or "new" or
            <None>.
        """
        self.complete_new_option = new_option
        self.complete_word_option= word_option
        self.complete_attribute  = attribute
    def add_spec(self, spec):
        """add a single specification."""
        for n in spec.names:
            if n in self.names:
                raise AssertionError("error: optionname %s used twice" % n)
            self.names.add(n)
            self.specs[n]= spec
        self.real_names.add(spec.real_name)
        self.speclist.append(spec)
    def add(self, name_str, completion= None, arg_name= None,
            array= False,
            arg_is_option= False,
            value_list= None):
        """add a single specification."""
        # pylint: disable=R0913
        #                          Too many arguments
        self.add_spec(OptionSpec(name_str, completion, arg_name,
                                 array, arg_is_option, value_list))
    def match(self, name):
        """return a list of matching optionnames."""
        return [n for n in self.names if n.startswith(name)]
    def get(self, name):
        """get OptionSpec object for a name."""
        return self.specs.get(name)
    def __repr__(self):
        """return python representation."""
        return "%s(%s)" % \
                (self.__class__.__name__,
                 ", ".join([repr(s) for s in self.speclist]))
    def __str__(self):
        """return human readable representation."""
        lines= [ self.__class__.__name__]
        for spec in self.speclist:
            l= str(spec).splitlines()
            l.pop(0)
            lines.extend(l)
            lines.append("    ----")
        return "\n".join(lines)

# -----------------------------------------------
# class for command specifications:
# -----------------------------------------------

class CmdSpec():
    """a single command specification."""
    # pylint: disable=R0903
    #                          Too few public methods
    def __init__(self, name, completion=None, array= False, optional= False):
        """initialize the object."""
        self.name= name
        self.completion= completion
        self.array= array
        self.optional= optional

class CmdSpecs():
    """hold command specfications."""
    def __init__(self):
        """Initialize the object."""
        self.names= []
        self.specs= {}
        self.cnt= 0
    def add(self, name, completion= None, array= False, optional= False):
        """add a single specification."""
        self.names.append(name)
        self.specs[name]= CmdSpec(name,completion,array,optional)
    def get(self):
        """get items."""
        if self.cnt>=len(self.names):
            return (None,None)
        name= self.names[self.cnt]
        self.cnt+=1
        return (name, self.specs[name])
    def start_get(self):
        """start getting items."""
        self.cnt= 0
    def more(self):
        """return if there are more items."""
        return self.cnt<len(self.names)

# -----------------------------------------------
# command line processing
# -----------------------------------------------

def is_opt(st):
    """Test if a string "looks" like an option.

    Here are some examples:

    >>> is_opt("")
    False
    >>> is_opt("x")
    False
    >>> is_opt("-")
    False
    >>> is_opt("-$")
    False
    >>> is_opt("-x")
    True
    >>> is_opt("-xx")
    False
    >>> is_opt("--x")
    True
    >>> is_opt("--$")
    False
    >>> is_opt("--")
    False
    >>> is_opt("--x-s")
    True
    """
    if not st:
        return False
    if st[0]!="-":
        return False
    if len(st)==1:
        return False
    if len(st)==2:
        return st[1].isalpha()
    if st[1]!="-":
        return False
    return st[2].isalpha()

class CliError(Exception):
    """Error from command line parsing."""

def assert_options(catch_exceptions, options, *opt_list):
    """check for the presence of options."""
    for opt in opt_list:
        if not getattr(options, opt):
            txt= "Error, --%s is mandatory here" % opt
            if not catch_exceptions:
                raise CliError(txt)
            sys.exit(txt)

def process_opts(args, optionspecs, catch_exceptions, testmode= False):
    """parse incomplete options.

    expects args[0] to be the program's name.

    >>> spcs= OptionSpecs()
    >>> spcs.completion_options("list","--list","--listnew")
    >>> spcs.add("--help -h")
    >>> spcs.add("--flag -F")
    >>> spcs.add("-x", arg_name="VALUE")
    >>> spcs.add("-a", arg_name="ELM", array= True)
    >>> spcs.add("-y", lambda x,r: [x+"a",x+"b"], "YOPT")

    >>> def t(args):
    ...     a= ["dummy"]
    ...     a.extend(args)
    ...     (options,rest)= process_opts(a, spcs, True, True)
    ...     if options is not None:
    ...         print(options)
    ...         print("rest:", repr(rest))



    >>> t([])
    Options
        a: None
        flag: None
        help: None
        list: None
        x: None
        y: None
    <BLANKLINE>
    rest: []
    >>> t(["-h"])
    Options
        a: None
        flag: None
        help: True
        list: None
        x: None
        y: None
    <BLANKLINE>
    rest: []
    >>> t(["--help"])
    Options
        a: None
        flag: None
        help: True
        list: None
        x: None
        y: None
    <BLANKLINE>
    rest: []
    >>> t(["-F"])
    Options
        a: None
        flag: True
        help: None
        list: None
        x: None
        y: None
    <BLANKLINE>
    rest: []
    >>> t(["--flag"])
    Options
        a: None
        flag: True
        help: None
        list: None
        x: None
        y: None
    <BLANKLINE>
    rest: []
    >>> t(["-x"])
    error, argument 'VALUE' missing for option '-x'
    >>> t(["-x", "ab"])
    Options
        a: None
        flag: None
        help: None
        list: None
        x: 'ab'
        y: None
    <BLANKLINE>
    rest: []
    >>> t(["-a", "a"])
    Options
        a: ['a']
        flag: None
        help: None
        list: None
        x: None
        y: None
    <BLANKLINE>
    rest: []
    >>> t(["-a", "a", "-h", "-a", "b"])
    Options
        a: ['a', 'b']
        flag: None
        help: True
        list: None
        x: None
        y: None
    <BLANKLINE>
    rest: []
    >>> t(["-a", "a", "-F", "-a", "b"])
    Options
        a: ['a', 'b']
        flag: True
        help: None
        list: None
        x: None
        y: None
    <BLANKLINE>
    rest: []
    >>> t(["-F", "--", "-x"])
    Options
        a: None
        flag: True
        help: None
        list: None
        x: None
        y: None
    <BLANKLINE>
    rest: ['-x']
    >>> t(["-a", "--", "-x"])
    Options
        a: ['-x']
        flag: None
        help: None
        list: None
        x: None
        y: None
    <BLANKLINE>
    rest: []
    >>> t(["-a", "--", "-x", "a"])
    Options
        a: ['-x']
        flag: None
        help: None
        list: None
        x: None
        y: None
    <BLANKLINE>
    rest: ['a']
    >>> t(["-a", "--", "b"])
    Options
        a: ['b']
        flag: None
        help: None
        list: None
        x: None
        y: None
    <BLANKLINE>
    rest: []
    >>> t(["-a", "ab", "--", "-h"])
    Options
        a: ['ab']
        flag: None
        help: True
        list: None
        x: None
        y: None
    <BLANKLINE>
    rest: []
    >>> t(["-y","a"])
    Options
        a: None
        flag: None
        help: None
        list: None
        x: None
        y: 'a'
    <BLANKLINE>
    rest: []

    >>> t(["-y","a","--list"])
    aa
    ab
    >>> t(["-y","a","--listnew"])
    Options
        a: None
        flag: None
        help: None
        list: 'new'
        x: None
        y: 'a'
    <BLANKLINE>
    rest: []
    >>> t(["-y","a","b","--listnew"])
    Options
        a: None
        flag: None
        help: None
        list: 'new'
        x: None
        y: 'a'
    <BLANKLINE>
    rest: ['b']
    >>> t(["-y","a","b","c","--listnew"])
    Options
        a: None
        flag: None
        help: None
        list: 'new'
        x: None
        y: 'a'
    <BLANKLINE>
    rest: ['b', 'c']
    >>> t(["-y","a","b","--list"])
    Options
        a: None
        flag: None
        help: None
        list: 'word'
        x: None
        y: 'a'
    <BLANKLINE>
    rest: ['b']
    >>> t(["--","--list"])
    --flag
    --help
    >>> t(["-","--list"])
    --flag
    --help
    -F
    -a
    -h
    -x
    -y
    >>> t(["-a","--list"])
    -a
    """
    # pylint: disable=R0914
    #                          Too many local variables
    # pylint: disable=R0912
    #                          Too many branches
    # pylint: disable=R0915
    #                          Too many statements
    # pylint: disable=R0911
    #                          Too many return statements
    def pr_complete(lst):
        """print completion list."""
        print("\n".join(sorted(lst)))
    def display_help(txt):
        """display help on stderr for a second."""
        txt= " "+txt
        sys.stderr.write(txt)
        time.sleep(1)
        bs= "\b" * len(txt)
        sp= " " * len(txt)
        sys.stderr.write("".join((bs,sp,bs)))

    def complete(spec, st, options):
        """print completion.

        May raise:
            any exception from comp_func
        """
        comp_func= None
        comp_func= spec.completion
        if comp_func:
            # may raise any exception:
            print("\n".join(sorted(comp_func(st, options))))
            return
        if spec.arg_name:
            display_help(spec.arg_name)
    def my_exit(msg=None):
        """exit func."""
        if testmode:
            if msg:
                print(msg)
        else:
            if msg is None:
                sys.exit()
            else:
                sys.exit("\n"+msg)
    # extract the program name from args:
    # arg0= args[0]
    args= args[1:]
    # names of options when they are put into the options object:
    option_names= optionspecs.real_names
    if not optionspecs.complete_attribute:
        raise AssertionError("in optionspecs complete_attribute is "
                             "not defined")
    # add the name of the completion option:
    option_names.add(optionspecs.complete_attribute)
    # add the name of the help option:
    option_names.add(HELP_NAME)
    # create an empty Options object:
    options= Options(dict((k, None) for k in optionspecs.real_names))
    if not args:
        # no args at all, return the Options object and a list of remaining
        # arguments which is empty in this case:
        return (options, [])
    completion_mode= ""
    help_mode= False
    new_args= []
    # First extract the help option and the completion_option from the argument
    # list, we parse these options even when a "--" is found in the argument
    # list:
    for a in args:
        if a==optionspecs.complete_word_option:
            completion_mode= "word"
            options.put(optionspecs.complete_attribute, completion_mode)
            continue
        if a==optionspecs.complete_new_option:
            completion_mode= "new"
            options.put(optionspecs.complete_attribute, completion_mode)
            continue
        help_= HELP_OPTS.get(a)
        if help_ is not None:
            help_mode= True
            options.put(help_, True)
            continue
        new_args.append(a)
    if not new_args:
        # no more args, just return what we have so far:
        return (options, [])
    # rest_args are arguments that are neither options nor option arguments:
    rest_args= []
    consumer= None # None or an OptionSpec object
    consumer_name= ""
    options_off= False
    optionspec= None

    i=-1
    while True:
        i+=1
        if i>=len(new_args):
            break
        a= new_args[i]

        if a=="--":
            if i<len(new_args)-1:
                # not at the last argument
                options_off= True
                continue
            # pylint: disable=no-else-return
            # at the last argument from here:
            if not completion_mode:
                if consumer and not help_mode:
                    my_exit(("error, argument '%s' missing for "
                             "option '%s'") % (optionspec.arg_name, a))
                return (options, rest_args)
            elif completion_mode=="new":
                return (options, rest_args)
            elif completion_mode=="word":
                if options_off:
                    my_exit()
                    return (None, None) # never reached
                # find all options starting with "--":
                opts= optionspecs.match(a)
                pr_complete(opts)
                my_exit()
                return (None, None) # never reached

        if consumer:
            if len(a)>1 and \
               a[0]=="-" and \
               not options_off and \
               not consumer.arg_is_option:
                # probably the next option value:
                if help_mode or completion_mode:
                    # skip this error:
                    options.put(consumer.real_name, True)
                    # re-evaluate the argument:
                    consumer= None
                    consumer_name=""
                    i-=1
                    continue
                my_exit(("error, argument '%s' missing for "
                         "option '%s'") % (consumer.arg_name, consumer_name))
                return (None, None) # never reached

            # an option has to get a value:
            if i<len(new_args)-1:
                # not the last argument:
                if not completion_mode:
                    # check the value:
                    if not consumer.check(a):
                        my_exit(("invalid option value '%s' for "
                                 "option '%s'") % (a, consumer_name))
                        return (None, None) # never reached
                options.put(consumer.real_name, a, consumer.array)
                consumer= None
                consumer_name=""
                continue
            # from here: at the end of the argument list:
            if not completion_mode:
                # check the value:
                if not consumer.check(a):
                    my_exit(("invalid option value '%s' for "
                             "option '%s'") % (a, consumer_name))
                    return (None, None) # never reached
                options.put(consumer.real_name, a, consumer.array)
                return (options, rest_args)
            # pylint: disable=no-else-return
            if completion_mode=="new":
                options.put(consumer.real_name, a, consumer.array)
                return (options, rest_args)
            else:
                # completion_mode=="word":
                try:
                    # may raise any exception:
                    complete(consumer, a, options)
                except sumolib.JSON.ParseError as e:
                    if not catch_exceptions:
                        raise
                    my_exit(str(e))
                my_exit()
                return (None, None) # never reached

        if a=="-":
            if i<len(new_args)-1:
                # not at the last argument
                rest_args.append(a)
                continue
            # at the last argument from here:
            if not completion_mode:
                # no completion_mode, we are finished here:
                rest_args.append(a)
                return (options, rest_args)
            if options_off:
                # cannot complete "-" if options are off:
                my_exit()
                return (None, None) # never reached
            # pylint: disable=no-else-return
            if completion_mode=="new":
                rest_args.append(a)
                return (options, rest_args)
            elif completion_mode=="word":
                # find all options starting with "-":
                opts= optionspecs.match(a)
                pr_complete(opts)
                my_exit()
                return (None, None) # never reached

        if (a[0]!='-') or options_off:
            # definitely no option:
            rest_args.append(a)
            continue

        optionspec= optionspecs.get(a)
        if not optionspec:
            # unknown option
            if not completion_mode:
                # this is an error
                my_exit("unknown option '%s'" % a)
                return (None, None) # never reached
            if i<len(new_args)-1:
                # unknown option in the middle, silently skip:
                continue
            # pylint: disable=no-else-return
            # at the last argument from here:
            if completion_mode=="new":
                # silently skip:
                return (options, rest_args)
            else:
                # must be completion_mode=="word"
                # find matching options:
                opts= optionspecs.match(a)
                pr_complete(opts)
                my_exit()
                return (None, None) # never reached

        if i>=len(new_args)-1:
            # at the end of the argument list:
            if not optionspec.arg_name:
                # pylint: disable=no-else-return
                # the option has no option value
                if not completion_mode:
                    options.put(optionspec.real_name, True)
                    return (options, rest_args)
                if completion_mode=="new":
                    options.put(optionspec.real_name, True)
                    return (options, rest_args)
                else:
                    # completion_mode=="word":
                    opts= optionspecs.match(a)
                    pr_complete(opts)
                    my_exit()
                    return (None, None) # never reached
            else:
                # option takes an argument
                if not completion_mode:
                    if help_mode:
                        # continue although argument is missing
                        options.put(optionspec.real_name, True)
                        return (options, rest_args)
                    my_exit(("error, argument '%s' missing for "
                             "option '%s'") % (optionspec.arg_name, a))
                    return (None, None) # never reached
                if completion_mode=="new":
                    try:
                        # may raise any exception:
                        complete(optionspec, "", options)
                    except sumolib.JSON.ParseError as e:
                        if not catch_exceptions:
                            raise
                        my_exit(str(e))
                    my_exit()
                    return (None, None) # never reached
                else:
                    # completion_mode=="word":
                    opts= optionspecs.match(a)
                    pr_complete(opts)
                    my_exit()
                    return (None, None) # never reached

        # from here: not at the end of the argument list:
        if not optionspec.arg_name:
            # the option has no option value
            options.put(optionspec.real_name, True)
            continue
        # option takes a value:
        consumer= optionspec
        consumer_name= a
        continue

    return (options, rest_args)

def process_cmd(cli_args, cmd_list, completion_mode,
                item_name= "command",
                testmode= False):
    """process a single command.

    cmd_list: list of possible commands (cli_args[0])

    returns a tuple (cmd, args)
    """
    # pylint: disable=R0912
    #                          Too many branches
    # pylint: disable= too-many-return-statements
    def complete(st, lst):
        """call completion func if it exists and exit."""
        l= sorted(lst)
        if st:
            l= [s for s in l if s.startswith(st)]
        print("\n".join(l))
    def my_exit(msg=None):
        """exit func."""
        if testmode:
            if msg:
                print(msg)
        else:
            if msg is None:
                sys.exit()
            else:
                sys.exit("\n"+msg)
    if not cli_args:
        # no args given
        if completion_mode:
            complete("", cmd_list)
            my_exit()
            return ("",[])
        # may produce "command missing" message:
        my_exit("%s missing" % item_name)
    if completion_mode:
        if len(cli_args)<=1:
            # pylint: disable=no-else-return
            # only a single command
            if completion_mode=="new":
                if cli_args[0] not in cmd_list:
                    # wrong command, cannot complete further
                    my_exit()
                    return ("",[])
                return(cli_args[0], cli_args[1:])
            else:
                # completion_mode=="word":
                complete(cli_args[0], cmd_list)
                my_exit()
                return ("",[])
        else:
            # more than one argument
            if cli_args[0] not in cmd_list:
                # wrong command, cannot complete further
                my_exit()
                return ("",[])
            # one command decoded, delegate completion to caller by returning
            # here:
            return(cli_args[0], cli_args[1:])
    # not completion_mode from here:
    if cli_args[0] not in cmd_list:
        # may produce "unknown command" message:
        my_exit("unknown %s: %s" % (item_name, cli_args[0]))
        return ("",[])
    return(cli_args[0], cli_args[1:])

def process_args(cli_args, argspec, completion_mode,
                 catch_exceptions, testmode= False):
    """new command argument processing.

    argspec must be None or an CmdSpecs object.

    Note:
    This function contains sys.exit statements !!

    Here is some testcode:

    >>> tspec= CmdSpecs()
    >>> tspec.add("MOD", completion= lambda x,r: [x+"a"+"-mod",x+"b"+"-mod"])
    >>> tspec.add("VER", completion= lambda x,r: [x+"1"+"-ver",x+"2"+"-ver"],
    ...           optional= True)
    >>> tspec.add("ARG", completion= lambda x,r: [x+"a"+"-arg",x+"b"+"-arg"],
    ...           optional= True, array= True)

    >>> import pprint

    >>> def t(cli_args, completion_mode):
    ...     r=process_args(cli_args, tspec, completion_mode, True, True)
    ...     if r:
    ...         pprint.pprint(r)


    >>> t([], None)
    error, mandatory argument MOD missing
    >>> t([], "word")
    a-mod
    b-mod
    >>> t(["a"], "word")
    aa-mod
    ab-mod
    >>> t(["mod"], None)
    Arguments({'ARG': [], 'MOD': 'mod', 'VER': None})
    >>> t(["mod"], "word")
    moda-mod
    modb-mod
    >>> t(["mod"], "new")
    1-ver
    2-ver
    >>> t(["mod","12"], None)
    Arguments({'ARG': [], 'MOD': 'mod', 'VER': '12'})
    >>> t(["mod","12"], "word")
    121-ver
    122-ver
    >>> t(["mod","12"], "new")
    a-arg
    b-arg
    >>> t(["mod","12", "a"], None)
    Arguments({'ARG': ['a'], 'MOD': 'mod', 'VER': '12'})
    >>> t(["mod","12", "a", "b"], None)
    Arguments({'ARG': ['a', 'b'], 'MOD': 'mod', 'VER': '12'})
    >>> t(["mod","12", "a", "b"], "word")
    ba-arg
    bb-arg
    >>> t(["mod","12", "a", "b"], "new")
    a-arg
    b-arg
    """
    # pylint: disable=R0912
    #                          Too many branches
    # pylint: disable=R0911
    #                          Too many return statements
    # pylint: disable=R0915
    #                          Too many statements
    def rcpy(l):
        """create reversed list."""
        n= l[:]
        n.reverse()
        return n
    def display_help(txt):
        """display help on stderr for a second."""
        txt= " "+txt
        sys.stderr.write(txt)
        time.sleep(1)
        bs= "\b" * len(txt)
        sp= " " * len(txt)
        sys.stderr.write("".join((bs,sp,bs)))
    def complete(name, spec, st, result):
        """call completion func if it exists and exit.

        May raise:
            any exception from comp_func
        """
        comp_func= None
        comp_func= spec.completion
        if comp_func:
            # may raise any exception:
            print("\n".join(sorted(comp_func(st, result))))
            return
        display_help(name)
    def my_exit(msg=None):
        """exit func."""
        if testmode:
            if msg:
                print(msg)
        else:
            if msg is None:
                sys.exit()
            else:
                sys.exit("\n"+msg)
    if not argspec:
        # no cli_args expected
        if completion_mode:
            my_exit()
            return None
        if not cli_args:
            return Arguments()
        my_exit("error, unexpected arguments: %s" % (" ".join(cli_args)))
        return None
    if not isinstance(argspec, CmdSpecs):
        raise TypeError("argspec '%s' has wrong type" % repr(argspec))
    argspec.start_get()
    result= Arguments()
    rargs= rcpy(cli_args)
    spec= CmdSpec(name="",array=False)
    arg= ""
    while True:
        if not rargs:
            break
        if not argspec.more() and not spec.array:
            break
        arg= rargs.pop()
        # keep the same spec all the time if it is of "array" type:
        if not spec.array:
            (name, spec)= argspec.get()
        if completion_mode=="word" and not rargs:
            try:
                # may raise any exception:
                complete(name, spec, arg, result)
            except sumolib.JSON.ParseError as e:
                if not catch_exceptions:
                    raise
                my_exit(str(e))
            my_exit()
            return None
        result.put(name, arg, is_array= spec.array)
    if not argspec.more():
        if completion_mode:
            if not rargs:
                if completion_mode=="new":
                    arg=""
                try:
                    # may raise any exception:
                    complete(name, spec, arg, result)
                except sumolib.JSON.ParseError as e:
                    if not catch_exceptions:
                        raise
                    my_exit(str(e))
            # if (rargs) is kind of an error here, just do nothing in
            # completion mode:
            my_exit()
            return None
        if rargs:
            # extra arguments
            my_exit("error, unexpected arguments: %s" % \
                 (" ".join(rcpy(rargs))))
            return None
    else:
        if completion_mode:
            if not spec.name:
                # no spec was loaded
                (name, spec)= argspec.get()
            elif completion_mode=="new":
                if not spec.array:
                    (name, spec)= argspec.get()
            if completion_mode=="new":
                arg=""
            try:
                # may raise any exception:
                complete(name, spec, arg, result)
            except sumolib.JSON.ParseError as e:
                if not catch_exceptions:
                    raise
                my_exit(str(e))
            my_exit()
            return None
        while argspec.more():
            (name, spec)= argspec.get()
            if not spec.optional:
                my_exit("error, mandatory argument %s missing" % name)
                return None
            # define the argument as None in the result object:
            result.declare(name, spec.array)
    # when the command was successfully parsed, clear cache files that may have
    # been created for command line completion:
    return result

def _test():
    """perform internal tests."""
    import doctest # pylint: disable= import-outside-toplevel
    doctest.testmod()

if __name__ == "__main__":
    _test()
