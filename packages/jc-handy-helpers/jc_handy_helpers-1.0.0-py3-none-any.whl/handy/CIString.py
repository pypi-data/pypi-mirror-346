class CIString(str):
    """This is kind of a lawyerly class for strings. They have no case!
    :) This is just like str, but hashing and comparison operations
    ignore case. This goes for comparing CIStrings with themselves or
    with ordinary str values.

    Sadly, just using CIStrings as dictionary keys is insufficient to
    make dictionary lookups of string values case-insensitive. See the
    handy.CIDict class for that."""

    def __new__(cls, value):
        str_value = str(value)
        instance = super().__new__(cls, str_value)
        instance._folded_hash = hash(str_value.casefold())
        return instance

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __eq__(self, other):
        folded_self = self.casefold()
        if isinstance(other, str):
            return folded_self == other.casefold()
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    def __lt__(self, other):
        folded_self = self.casefold()
        if isinstance(other, str):
            return folded_self < other.casefold()
        return NotImplemented

    def __le__(self, other):
        folded_self = self.casefold()
        if isinstance(other, str):
            return folded_self <= other.casefold()
        return NotImplemented

    def __gt__(self, other):
        folded_self = self.casefold()
        if isinstance(other, str):
            return folded_self > other.casefold()
        return NotImplemented

    def __ge__(self, other):
        folded_self = self.casefold()
        if isinstance(other, str):
            return folded_self >= other.casefold()
        return NotImplemented

    def __hash__(self):
        return self._folded_hash
