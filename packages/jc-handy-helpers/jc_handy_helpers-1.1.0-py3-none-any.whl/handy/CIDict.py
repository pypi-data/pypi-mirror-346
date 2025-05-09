from .CIString import CIString

class CIDict(dict):
    """Just like dict, but string keys are coerced to CIString values,
    so d['alpha'] and d['AlPhA'] return the same value. (It's also okay
    to have non-string keys, just like regular dictionaries.)"""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        if isinstance(key, str) and not isinstance(key, CIString):
            super().__setitem__(CIString(key), value)
        else:
            super().__setitem__(key, value)

    def __getitem__(self, key):
        if isinstance(key, str) and not isinstance(key, CIString):
            key = CIString(key)
        return super().__getitem__(key)

    def __contains__(self, key):
        if isinstance(key, str) and not isinstance(key, CIString):
            key = CIString(key)
        return super().__contains__(key)

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def update(self, *args, **kwargs):
        if args:
            other = dict(args[0])
            for k, v in other.items():
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def pop(self, key, default=None):
        try:
            if isinstance(key, str) and not isinstance(key, CIString):
                return super().pop(CIString(key))
            return super().pop(key)
        except KeyError:
            if default is not None:
                return default
            raise

    def fromkeys(cls, iterable, value=None):
        new_dict = CIDict()
        for key in iterable:
            new_dict[key] = value
        return new_dict

    def copy(self):
        return CIDict(super().copy())

    def __repr__(self):
        items = []
        for key, value in self.items():
            items.append(f"{repr(key)}: {repr(value)}")
        return f"{self.__class__.__name__}({{{', '.join(items)}}})"
