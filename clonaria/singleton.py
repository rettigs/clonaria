class Singleton(object):
    """
    Taken from https://www.python.org/download/releases/2.2/descrintro/#__new__

    Objects that inherit this class are instantiated the first time they are called.
    Further instantiations return the same object.
    """
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it
    def init(self, *args, **kwds):
        pass
