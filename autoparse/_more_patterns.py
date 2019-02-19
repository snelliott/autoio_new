""" re pattern generators that use _lib constants
"""
from ._pattern import zero_or_more as _zero_or_more
from ._lib import WILDCARD as _WILDCARD


def block(start_pattern, end_pattern):
    """ generate a pattern for a (non-greedy) block bounded by two patterns

    :param start_pattern: an `re` pattern for the start
    :type start_pattern: str
    :param end_pattern: an `re` pattern for the end
    :type end_pattern: str
    """
    pattern = (start_pattern + _zero_or_more(_WILDCARD, greedy=False) +
               end_pattern)
    return pattern
