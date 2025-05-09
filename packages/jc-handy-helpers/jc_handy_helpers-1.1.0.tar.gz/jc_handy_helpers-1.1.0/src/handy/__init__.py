import fnmatch, os, re, shlex, sys, termios, typing
from dataclasses import dataclass
from importlib.metadata import packages_distributions, version, PackageNotFoundError
from importlib.util import find_spec
from pprint import pprint

from .AsciiString import AsciiString
from .CIString import CIString
from .CIDict import CIDict
from .ProgInfo import ProgInfo
from .Spinner import Spinner

# Define some handy package-level instances.
prog = ProgInfo()
cylon_spinner = Spinner(Spinner.cylon, yoyo=True)
wheel_spinner = Spinner() # Traditional text character spinner.

# To support legacy code ...
CaselessString=CIString
CaselessDict=CIDict

__all__=[
    'AsciiString',
    'CIDict','CaselessDict',
    'CIString','CaselessString',
    'ModuleVersion','get_module_versions',
    'ProgInfo','prog',
    'Spinner','cylon_spinner','wheel_spinner',
    'compile_filename_patterns',
    'die',
    'file_walker',
    'first_match',
    'getch',
    'gripe',
    'non_negative_int',
    'positive_int',
    'rmdirs',
    'shellify',
]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   Generally useful stuff.


def first_match(s, patterns):
    """Find the first matching pattern. If found, return the (pattern,
    match) tuple. If not, return (None,None). The "patterns" arugment is
    an itterable of compiled regular expressions, but see the
    compile_filename_patterns() function also in this module for a way
    to make this far more general."""

    for p in patterns:
        m = p.match(s)
        if m:
            return p, m
    return None, None


def non_negative_int(s):
    "Return the non-negative integer value of s, or raise ValueError."

    try:
        n = int(s)
        if n >= 0:
            return n
    except:
        pass
    raise ValueError(f"{s!r} is not a non-negative integer.")


def positive_int(s):
    "Return the positive integer value of s, or raise ValueError."

    try:
        n = int(s)
        if n > 0:
            return n
    except:
        pass
    raise ValueError(f"{s!r} is not a positive integer.")


def shellify(val):
    """Return the given value quotted and escaped as necessary for a
    Unix shell to interpret it as a single value.

    >>> print(shellify(None))
    ''
    >>> print(shellify(123))
    123
    >>> print(shellify(123.456))
    123.456
    >>> print(shellify("This 'is' a test of a (messy) string."))
    'This '"'"'is'"'"' a test of a (messy) string.'
    >>> print(shellify('This "is" another messy test.'))
    'This "is" another messy test.'
    """

    if val is None:
        s = ""
    elif not isinstance(val, str):
        s = str(val)
    else:
        return shlex.quote(val)
    return shlex.quote(s)

def die(msg, output=sys.stderr, progname=prog.name, rc=1):
    """Write '<progname>: <msg>' to output, and terminate with code rc.

    Defaults:
      output:   sys.stderr
      progname: basename of the current program (from sys.argv[0])
      rc:       1

    If rc is None the program is not actually terminated, in which case
    this function simply returns."""

    output.write("%s: %s\n" % (progname, msg))
    if rc is not None:
        sys.exit(rc)


def gripe(msg, output=sys.stderr, progname=prog.name):
    "Same as die(...,rc=None), so the program doesn't terminate."

    die(msg, output, progname, rc=None)

def getch(prompt=None, echo=False):
    """Read a single keystroke from stdin. The user needn't press Enter.
    This function returns the character as soon has it is typed. The
    character is not echoed to the screen unless the "echo" argument is
    True.

    If "prompt" is some true value, write that string to standard output
    before getting the input character, and then after the input, write
    a newline character to standard output."""

    import termios
    import sys, tty

    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    if prompt:
        sys.stdout.write(prompt)
        sys.stdout.flush()
    ch = _getch()
    if echo:
        sys.stdout.write(ch)
    if prompt:
        sys.stdout.write("\n")
    sys.stdout.flush()
    return ch

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   Filename and file system helpers.

def compile_filename_patterns(pattern_list):
    """Given a sequence of filespecs, regular expressions (prefixed with
    're:'), and compiled regular expressions, convert them all to
    compiled RE instances. The original pattern_list is not modified.
    The compiled REs are returned in a new list."""

    pats = list(pattern_list)
    for i in range(len(pats)):
        if isinstance(pats[i], str):
            if pats[i].startswith("re:"):
                pats[i] = pats[i][3:]
            else:
                pats[i] = fnmatch.translate(pats[i])
            pats[i] = re.compile(pats[i])
    return pats

def file_walker(root, **kwargs):
    """This is a recursive iterator over the files in a given directory
    (the root), in all subdirectories beneath it, and so forth. The
    order is an alphabetical and depth-first traversal of the whole
    directory tree.

    If anyone cares: While the effect of this function is to recurse
    into subdirectories, the function itself is not recursive.

    Keyword Arguments:
     *depth        (default: None) The number of directories this
                   iterator will decend below the given root path when
                   traversing the directory structure. Use 0 for only
                   top-level files, 1 to add the next level of
                   directories' files, and so forth.
     *follow_links (default: True) True if symlinks are to be followed.
                   This iterator guards against processing the same
                   directory twice, even if there's a symlink loop, so
                   it's always safe to leave this set to True.
     *prune        (default: []) A list of filespecs, regular
                   expressions (prefixed by 're:'), or pre-compiled RE
                   objects. If any of these matches the name of an
                   encountered directory, that directory is ignored.
     *ignore       (default: []) This works just like prune, but it
                   excludes files rather than directories.
     *report_dirs  (default: False) If True or 'first', each directory
                   encountered will be included in this iterator's
                   values immediately before the filenames found in that
                   directory. If 'last', they will be included
                   immediatly after the the last entry in that
                   directory. In any case, directory names end with the
                   path separator appropriate to the host operating
                   system in order to distinguish them from filenames.
                   If the directory is not descended into because of
                   depth-limiting or pruning, that directory will not
                   appear in this iterator's values at all. The default
                   is False, meaning only non-directory entries are
                   reported.
    """

    # Get our keyword argunents, and do some initialization.
    max_depth = kwargs.get("depth", None)
    if max_depth is None:
        max_depth = sys.maxsize  # I don't think we'll hit this limit in practice.
    follow_links = kwargs.get("follow_links", True)
    prune = compile_filename_patterns(kwargs.get("prune", []))
    ignore = compile_filename_patterns(kwargs.get("ignore", []))
    report_dirs = kwargs.get("report_dirs", False)
    if report_dirs not in (False, True, "first", "last"):
        raise ValueError(
            "report_dirs=%r is not one of False, True, 'first', or 'last'."
            % (report_dirs,)
        )
    stack = [(0, root)]  # Prime our stack with root (at depth 0).
    been_there = set([os.path.abspath(os.path.realpath(root))])
    dir_stack = []  # Stack of paths we're yielding after exhausting those directories.

    while stack:
        depth, path = stack.pop()
        if report_dirs in (True, "first"):
            yield path + os.sep
        elif report_dirs == "last":
            dir_stack.append(path + os.sep)
        flist = os.listdir(path)
        flist.sort()
        dlist = []
        # First, let the caller iterate over these filenames.
        for fn in flist:
            p = os.path.join(path, fn)
            if os.path.isdir(p):
                # Just add this to this path's list of directories for now.
                dlist.insert(0, fn)
                continue
            pat, mat = first_match(fn, ignore)
            if not pat:
                yield p
        # Don't dig deeper than we've been told to.
        if depth < max_depth:
            # Now, let's deal with the directories we found.
            for fn in dlist:
                p = os.path.join(path, fn)
                # We might need to stack this path for our fake recursion.
                if os.path.islink(p) and not follow_links:
                    # Nope. We're not following symlinks.
                    continue
                rp = os.path.abspath(os.path.realpath(p))
                if rp in been_there:
                    # Nope. We've already seen this path (and possibly processed it).
                    continue
                m = None
                pat, mat = first_match(fn, prune)
                if pat:
                    # Nope. This directory matches one of the prune patterns.
                    continue
                # We have a keeper! Record the path and push it onto the stack.
                been_there.add(rp)
                stack.append((depth + 1, p))
    while dir_stack:
        yield dir_stack.pop()

def rmdirs(path):
    """Just like os.rmdir(), but this fuction takes care of recursively
    removing the contents under path for you.

    WARNING: Don't use this function. It's only here to support lagacy
    code until I can replace calls to rmdirs() with calls to
    os.removedirs(). This is a misbegotten function and should not be
    used."""

    for f in file_walker(path, follow_links=False, report_dirs="last"):
        if f[-1] == os.sep:
            if f != os.sep:
                # print "os.rmdir(%r)"%(f[:-1],)
                os.rmdir(f[:-1])
        else:
            # print "os.remove(%r)"%(f,)
            os.remove(f)

@dataclass
class ModuleVersion:
    """
    Instances of this dataclass have three attributes:

      name:    The name of the imported module.
      dist:    The name of the package installed via pip.
      version: The version string from the module's metadata.

    You shouldn't need to instantiate this dataclass yourself, but it
    would look like this:

        module=ModuleVersion(
            'module_name',
            'distributed_package_name_if_different',
            'version_string_of_this_module
        )

    The `dist` attrubute will be `None` if the module is distrubuted
    under the same name as the imported module.

    This dataclass also contains two format strings:

      fmt:      Format string for just `name` and `version` values.
      fmt_dist: Also includes formatting for the `dist` value.

    Update these format strings at both your pleasure and peril.

    See the get_module_versions() function for more information.
    """

    fmt: typing.ClassVar[str]="{name}: {version}"
    fmt_dest: typing.ClassVar[str]="{name} (from {dist}): {version}"

    name: str
    dist: str
    version: str

    def __str__(self):
        if self.dist:
            return ModuleVersion.fmt_dest.format(**self.__dict__)
        else:
            return ModuleVersion.fmt.format(**self.__dict__)

def get_module_versions():
    """
    Return a list of ModuleVersion instances starting with the main
    program module, followed by the sorted-by-name imported modules that
    are not part of Python's standard library.

    The main module can print its own version like this:

        print(get_module_versions()[0])

    Or it can include the versions of its non-standard dependencies like
    this:

        mv=get_module_versions()
        print(mv.pop(0))
        while mv:
            print(' ',mv.pop(0))

    See the ModuleVersion dataclass for more information.
    """

    # Get a dictionary of imported, non-standard modules.
    std_mod_path=os.path.dirname(os.__file__)
    imported={}
    for m in sorted(sys.modules.keys()):
        if m=='__main__' or '.' in m or m[0]=='_':
            continue
        spec=find_spec(m)
        if spec.origin is None or spec.origin=='built-in' or std_mod_path in spec.origin:
            continue
        imported[m]=ModuleVersion(m,None,None)

    # Get version strings for these modules.
    pd=packages_distributions()
    # Iterate on a distinct list of keys because we modify the dictionary
    # we're iterating through.
    for m in list(imported.keys()):
        try:
            imported[m].version=version(m)
        except PackageNotFoundError as e:
            if m in pd:
                dist=pd[m][0]
                try:
                    imported[m].dist=dist
                    imported[m].version=version(dist)
                except PackageNotFoundError as e:
                    del imported[m]
            else:
                del imported[m]

    # Return a list of ModuleVersion instances beginning with our main program
    # module and continuing with a sorted list of imported, non-standard
    # modules.
    if prog.name in imported:
        response=[imported.pop(prog.name)]
    else:
        response=[ModuleVersion(prog.name,None,'UNKNOWN')]
    response.extend(sorted(imported.values(),key=lambda m:m.name))
    return response
