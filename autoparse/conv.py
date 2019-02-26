""" convert string captures to various datatypes
"""


def single(capture, func):
    """ convert a single-capture to another datatype

    :param capture: a single-capture return value
    :type capture: str or None
    :param func: a string converter
    :type func: callable
    """
    ret = capture
    if capture:
        ret = func(capture) if capture else capture
    return ret


def multi(mcapture, funcs):
    """ convert a multi-capture to another datatype

    :param mcapture: a multi-capture return value
    :type mcapture: tuple[str] or None
    :param funcs: a sequence of string converters
    :type funcs: tuple[callable]
    """

    ret = mcapture
    if mcapture:
        assert len(mcapture) == len(funcs)
        ret = tuple(func(capture) for capture, func in zip(mcapture, funcs))
    return ret


def singles(captures, func):
    """ convert a sequence of single-captures to another datatype

    :param captures: a sequence of single-capture return values
    :type captures: tuple[str]
    :param func: a string converter
    :type func: callable
    """
    ret = captures
    if captures:
        ret = tuple(map(func, captures)) if captures else captures
    return ret


def multis(mcaptures, funcs):
    """ convert a sequence of multi-captures to another datatype

    :param mcaptures: a sequence of multi-capture return values
    :type mcaptures: tuple[tuple[str]]
    :param funcs: a sequence of string converters
    :type funcs: tuple[callable]
    """
    ret = mcaptures
    if mcaptures:
        ret = tuple(multi(captures, funcs) for captures in mcaptures)
    return ret
