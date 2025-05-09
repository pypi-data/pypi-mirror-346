class AsciiString(str):
    """This is just like str, but any non-ASCII characters are converted
    (if possible) to ASCII.

    Caveat: Regardless of the impropriety of this rule, AsciiString
    permits translations of each non-ASCII character to only one ASCII
    character. If no such translation can be made, the non-ASCII
    character remains in the AsciiString instance. The caller can check
    for this, using the isascii() method.
    """

    # Our Unicode-to-ASCII translator map will be computed the first time an
    # AsciiStr object is instantiated.
    utoa = None

    def __new__(cls, val):
        if cls.utoa is None:
            # Create our string translator based on the ASCII-to-Unicode
            # character map below. We could run str.maketrans() against the
            # consequent string literals, but this seems more edit-friendly,
            # and we only build this translator the first time AsciiString is
            # instantiated. It is expected this map will grow over time, but
            # it must ALWAYS map a single ASCII character to a single Unicode
            # character, regardles of what might be actually "correct."
            conv = {
                "'": {"´"},
                "A": {"Æ", "Á", "Å", "À", "Â", "ă", "Ä", "Ã"},
                "B": {"Þ"},
                "C": {"Ç"},
                "E": {"Ë", "É", "Ê", "È"},
                "I": {"Ï", "Í", "Î", "Ì"},
                "J": {"Ð"},
                "N": {"ń", "Ñ"},
                "O": {"Ø", "Ó", "Ö", "Ò", "Õ", "Ô"},
                "S": {"ș", "š"},
                "T": {"ț"},
                "U": {"Ù", "Ü", "Û", "Ú"},
                "Y": {"Ý"},
                "Z": {"ž"},
                "a": {"â", "ã", "á", "æ", "Ń", "å", "ä", "à"},
                "b": {"þ"},
                "c": {"ç"},
                "e": {"é", "ê", "è", "ë"},
                "f": {"Ș"},
                "i": {"ì", "î", "ï", "í"},
                "n": {"ñ", "Š"},
                "o": {"õ", "ó", "ò", "ð", "ö", "ø", "ô"},
                "s": {"Ț", "ū", "ß"},
                "u": {"û", "Ž", "ü", "ù", "ú"},
                "y": {"Ă", "ý"},
                "z": {"ƒ"},
            }

            u = a = ""
            for ach in conv:
                for uch in conv[ach]:
                    a += ach
                    u += uch
            cls.utoa = str.maketrans(u, a)

        return str.__new__(cls, val.translate(cls.utoa))
