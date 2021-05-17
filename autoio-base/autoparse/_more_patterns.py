""" re pattern generators that use _lib constants
"""
from autoparse._pattern import zero_or_more as _zero_or_more
from autoparse._lib import LINESPACE as _LINESPACE


def lpadded(pattern, fill_pattern=_LINESPACE):
    """ a pattern allowing optional linespaces to the left
    """
    return _zero_or_more(fill_pattern) + pattern


def rpadded(pattern, fill_pattern=_LINESPACE):
    """ a pattern allowing optional linespaces to the right
    """
    return pattern + _zero_or_more(fill_pattern)


def padded(pattern, fill_pattern=_LINESPACE):
    """ a pattern allowing optional linespaces to the right
    """
    return _zero_or_more(fill_pattern) + pattern + _zero_or_more(fill_pattern)
