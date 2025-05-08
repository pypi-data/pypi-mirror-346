import fcntl, os, struct, sys, termios

class ProgInfo():
    """Use an instance of this class to get helpful information about
    your running script.

    Properties:
      * name        - basename of the current script's main file.
      * pid         - numeric PID (program ID) of this script.
      * dir         - full, absolute dirname of this script.
      * real_name   - like name, but with any symlinks resolved.
      * real_dir    - like dir, but with any symlinks resolved.
      * tempdir     - name of this system's main temp directory.
      * temp        - full name of this script's temp file or temp directory.
      * term_height - number of characters high the terminal window is.
      * term_wdith  - number of characters wide the terminal window is.
    """

    def __init__(self):
        """Set up this instance's data."""

        # Name of the current script's main file without the directory.
        self.name = os.path.basename(sys.argv[0])

        # The numeric PID (program ID) of the currently running script.
        self.pid = os.getpid()

        # The full, absolute path to the directory given when the current
        # script was run.
        self.dir = os.path.abspath(os.path.dirname(sys.argv[0]))

        # Like name and dir, but these follow any symlinks to find the real name.
        # Also, real_dir holds the full, absolute path.
        self.real_dir, self.real_name = os.path.split(os.path.realpath(sys.argv[0]))

        # A decent choice of temp file or directory for this program, if
        # needed.
        self.tempdir = self.findMainTempDir()
        self.temp = os.path.join(self.tempdir, "%s.%d" % (self.name, self.pid))

        # Get the terminal width and and height, or default to 25x80.
        self.getTerminalSize()

    def __repr__(self):
        d = self.__dict__
        alist = list(self.__dict__.keys())
        alist.sort()
        return "%s(%s)" % (
            self.__class__.__name__,
            ",".join(
                [
                    "%s=%r" % (a, d[a])
                    for a in alist
                    if not a.startswith("_") and not callable(getattr(self, a))
                ]
            ),
        )

    def getTerminalSize(self):
        """Return a (width,height) tuple for the caracter size of our
        terminal. Also update this instance's term_width and term_height
        properties."""

        # Let the COLUMNS and LINES environment variables override any actual terminal
        # dimensions.
        self.term_width = os.environ.get("COLUMNS")
        if self.term_width:
            self.term_width = int(self.term_width)
        self.term_height = os.environ.get("LINES")
        if self.term_height:
            self.term_height = int(self.term_height)

        # Get terminal dimensions from the terminal device IFF needed.
        for f in sys.stdin, sys.stdout, sys.stderr:
            if f.isatty():
                th, tw, _, _ = struct.unpack(
                    "HHHH",
                    fcntl.ioctl(
                        f.fileno(), termios.TIOCGWINSZ, struct.pack("HHHH", 0, 0, 0, 0)
                    ),
                )
                if not self.term_width:
                    self.term_width = tw
                if not self.term_height:
                    self.term_height = tw
                break
        else:
            # Lame though it is, use 80x25 for terminal dimensions if we can't figure
            # anything else out.
            if not self.term_width:
                self.term_width = 80
            if not self.term_height:
                self.term_height = 25

        return self.term_width, self.term_height

    def findMainTempDir(self, perms=None):
        """Return the full path to a reasonable guess at what might be a
        temp direcory on this system, creating it if necessary using the
        given permissions. If no permissions are given, we'll base the
        perms on the current umask."""

        # Let the environment tell us where our temp directory is, or ought
        # to be, or just use /tmp if the enrionment lets us down.
        d = os.path.abspath(
            os.environ.get(
                "TMPDIR",
                os.environ.get(
                    "TEMP", os.environ.get("TMP", os.path.join(os.sep, "tmp"))
                ),
            )
        )

        # Ensure our temp direcory exists.
        if not os.path.isdir(d):
            # If no permissions were given, then just respect the current umask.
            if perms is None:
                m = os.umask(0)
                os.umask(m)
                perms = m ^ 0o777
            # Set the 'x' bit of each non-zero permission tripplet
            # (e.g. 0640 ==> 0750).
            perms = [p | (p != 0) for p in [((mode >> n) & 7) for n in (6, 3, 0)]]
            os.path.mkdirs(d, perms)

        # If all went well, return the full path of this possibly new directory.
        return d

    def makeTempFile(self, perms=0o600, keep=False):
        """Open (and likely create, but at least truncate) a temp file
        for this program, and return the open (for reading and writing)
        file object. See our "temp" attribute for the name of the file.
        Remove this file at program termination unless the "keep"
        argument is True."""

        fd = os.open(self.temp, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_TRUNC, perms)
        f = os.fdopen(fd, "w+")
        if not keep:
            atexit.register(os.remove, self.temp)
        return f

    def makeTempDir(self, perms=0o700, keep=False):
        """Create a directory for this program's temp files, and
        register a function with the atexit module that will
        automatically removed that whole directory if when this program
        exits (unless keep=True is given as one of the keyword
        arguments)."""

        os.mkdirs(self.temp, perms)
        if not keep:
            atexit.register(rmdirs, self.temp)
        return self.temp
