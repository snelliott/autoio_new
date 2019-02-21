""" convert string captures to various datatypes
"""


def single(capture, dtype):
    """ convert a single-capture to another datatype

    :param capture: a single-capture return value
    :type capture: str or None
    :param dtype: a data type (int, float)
    :type dtype: type
    """
    assert isinstance(dtype, type)

    ret = capture
    if capture:
        ret = dtype(capture) if capture else capture
    return ret


def multi(mcapture, dtypes):
    """ convert a multi-capture to another datatype

    :param mcapture: a multi-capture return value
    :type mcapture: tuple[str] or None
    :param dtypes: a sequence of data types (int, float)
    :type dtypes: tuple[type]
    """
    assert all(isinstance(dtype, type) for dtype in dtypes)

    ret = mcapture
    if mcapture:
        assert len(mcapture) == len(dtypes)
        ret = tuple(dtype(capture) for capture, dtype in
                    zip(mcapture, dtypes))
    return ret


def singles(captures, dtype):
    """ convert a sequence of single-captures to another datatype

    :param captures: a sequence of single-capture return values
    :type captures: tuple[str]
    :param dtype: a data type (int, float)
    :type dtype: type
    """
    assert isinstance(dtype, type)

    ret = captures
    if captures:
        ret = tuple(map(dtype, captures)) if captures else captures
    return ret


def multis(mcaptures, dtypes):
    """ convert a sequence of multi-captures to another datatype

    :param mcaptures: a sequence of multi-capture return values
    :type mcaptures: tuple[tuple[str]]
    :param dtypes: a sequence of data types (int, float)
    :type dtypes: tuple[type]
    """
    assert all(isinstance(dtype, type) for dtype in dtypes)

    ret = mcaptures
    if mcaptures:
        ret = tuple(multi(captures, dtypes) for captures in mcaptures)
    return ret
