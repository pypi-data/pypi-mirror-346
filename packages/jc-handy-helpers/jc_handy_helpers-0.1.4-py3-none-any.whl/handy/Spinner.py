class Spinner:
    """Instantiate this class with any sequence, the elements of which
    will be returned iteratively every time that instance is called.

    Example:
    >>> spinner=Spinner('abc')
    >>> spinner=Spinner('abc')
    >>> spinner()
    'a'
    >>> spinner()
    'b'
    >>> spinner()
    'c'
    >>> spinner()
    'a'

    Each next element of the given sequence is returned every time the
    instance is called, which repeats forever. The default sequence is
    '-\\|/', which are the traditional ASCII spinner characters. Try
    this:

      import sys,time
      from handy import Spinner
      spinner=Spinner()
      while True:
        sys.stderr.write(" It won't stop! (%s) \\r"%spinner())
        time.sleep(0.1)

    It's a cheap trick, but it's fun. (Use ^C to stop it.)

    By the way, ANY indexable sequence can be used. A Spinner object
    instantiated with a tuple of strings will return the "next" string
    every time that instance is called, which can be used to produce
    multi-character animations. The code below demonstrates this and
    uses yoyo=True to show how that works as well.

      import sys,time
      from handy import Spinner
      spinner=Spinner(Spinner.cylon,True)
      while True:
        sys.stderr.write(" The robots [%s] are coming. \\r"%spinner())
        time.sleep(0.1)

    Bear in mind instantiating Spinner with a mutable sequence (like a
    list) means you can modify that last after the fact. This raises
    some powerful, though not necessarily intended, possibilities.
    """

    cylon = tuple(
        """
-
 -
  =
  =+=
   <*>
    =+=
      =
       -
        -
""".strip().split(
            "\n"
        )
    )

    def __init__(self, seq=r"-\|/", yoyo=False):
        """Set the sequence for this Spinner instance. If yoyo is True,
        the sequence items are returned in ascending order than then in
        descending order, and so on. Otherwise, which is the default,
        the items are returned only in ascending order."""

        self.seq = seq
        self.ndx = -1
        self.delta = 1
        self.yoyo = yoyo

    def __call__(self):
        """Return the "next" item from the sequence this object was
        instantiated with. If yoyo was True when this objecect was
        created, items will be returned in ascending and then descending
        order."""

        self.ndx += self.delta
        if not 0 <= self.ndx < len(self.seq):
            if self.ndx > len(self.seq):
                self.ndx = len(self.seq)  # In case this sequence has shrunk.
            if self.yoyo:
                self.delta *= -1
                self.ndx += self.delta * 2
            else:
                self.ndx = 0
        return self.seq[self.ndx]
