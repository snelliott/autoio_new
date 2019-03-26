""" functions for working with parameter classes
"""
import inspect
import itertools


def values(cls):
    """ list the values of a parameter class
    """
    assert inspect.isclass(cls)
    vals = tuple(val for val in _public_attributes(cls)
                 if not inspect.isclass(val))
    return vals


def all_values(cls):
    """ recursively list the values of a parameter class tree
    """
    assert inspect.isclass(cls)
    vals = tuple(itertools.chain(*(
        [val] if not inspect.isclass(val) else all_values(val)
        for val in _public_attributes(cls))))
    return vals


def _public_attributes(cls):
    return tuple(val for name, val in
                 inspect.getmembers(cls, lambda x: not inspect.isroutine(x))
                 if not name.startswith('_') and not inspect.isfunction(val))
