""" re finders
"""
import re
from functools import partial
from ._lib import STRING_START as _STRING_START
from ._lib import STRING_END as _STRING_END
from ._lib import LINE_START as _LINE_START
from ._lib import NEWLINE as _NEWLINE
from ._lib import SPACES as _SPACES
from ._lib import LINESPACES as _LINESPACES
from ._lib import NUMBER as _NUMBER
from ._pattern import maybe as _maybe
from ._pattern import capturing as _capturing
from ._more_patterns import block as _block_pattern


def has_match(pattern, string):
    """ does this string have a pattern match?
    """
    match = re.search(pattern, string, flags=re.MULTILINE)
    return match is not None


def full_match(pattern, string):
    """ does this pattern match this *entire* string?
    """
    pattern_ = _STRING_START + pattern + _STRING_END
    return has_match(pattern_, string)


def starts_with(pattern, string):
    """ does the string start with this pattern
    """
    start_pattern = _STRING_START + pattern
    return has_match(start_pattern, string)


def ends_with(pattern, string):
    """ does the string end with this pattern
    """
    end_pattern = pattern + _STRING_END
    return has_match(end_pattern, string)


def matcher(pattern):
    """ return a boolean matching function
    """
    return partial(has_match, pattern)


def all_captures(pattern, string):
    """ capture(s) for all matches of a capturing pattern
    """
    return tuple(re.findall(pattern, string, flags=re.MULTILINE))


def first_capture(pattern, string):
    """ capture(s) from first match for a capturing pattern
    """
    match = re.search(pattern, string, flags=re.MULTILINE)
    return (match.group(1) if match and len(match.groups()) == 1 else
            match.groups() if match else None)


def last_capture(pattern, string):
    """ capture(s) from first match for a capturing pattern
    """
    caps_lst = all_captures(pattern, string)
    return caps_lst[-1] if caps_lst else None


def first_named_capture(pattern, string):
    """ capture dictionary from first match for a pattern with named captures
    """
    match = re.search(pattern, string, flags=re.MULTILINE)
    return match.groupdict() if match and match.groupdict() else None


def split(pattern, string):
    """ split string at matches
    """
    return tuple(re.split(pattern, string, maxsplit=0, flags=re.MULTILINE))


def split_words(string):
    """ split string at whitespaces
    """
    return split(_SPACES, strip_spaces(string))


def split_lines(string):
    """ split string at newlines
    """
    return split(_NEWLINE, string)


def remove(pattern, string):
    """ remove pattern matches
    """
    return replace(pattern, '', string)


def remove_empty_lines(string):
    """ remove empty lines from a string
    """
    pattern = _LINE_START + _maybe(_LINESPACES) + _NEWLINE
    return remove(pattern, string)


def strip_spaces(string):
    """ strip spaces from the string ends
    """
    lspaces = _STRING_START + _SPACES
    rspaces = _SPACES + _STRING_END
    return remove(lspaces, remove(rspaces, string))


def replace(pattern, repl, string):
    """ replace pattern matches
    """
    return re.sub(pattern, repl, string, count=0, flags=re.MULTILINE)


# data type checkers
def is_number(string):
    """ does this string encode a (real) number?
    """
    return full_match(_NUMBER, strip_spaces(string))


# advanced finders
def all_blocks(start_pattern, end_pattern, string):
    """ capture all (non-greedy) blocks bounded by two patterns
    """
    pattern = _capturing(_block_pattern(start_pattern, end_pattern))
    return all_captures(pattern, string)


def first_block(start_pattern, end_pattern, string):
    """ capture the first (non-greedy) block bounded by two patterns
    """
    pattern = _capturing(_block_pattern(start_pattern, end_pattern))
    return first_capture(pattern, string)


def last_block(start_pattern, end_pattern, string):
    """ capture the last (non-greedy) block bounded by two patterns
    """
    pattern = _capturing(_block_pattern(start_pattern, end_pattern))
    return last_capture(pattern, string)


def first_matching_pattern(patterns, string):
    """ from a series of patterns, return the first one matching the string
    """
    pattern = next(filter(partial(has_match, string=string), patterns), None)
    return pattern


def first_matching_pattern_all_captures(patterns, string):
    """ all captures from the first matching pattern
    """
    pattern = first_matching_pattern(patterns, string)
    return all_captures(pattern, string)


def first_matching_pattern_first_capture(patterns, string):
    """ first capture from the first matching pattern
    """
    pattern = first_matching_pattern(patterns, string)
    return first_capture(pattern, string)


def first_matching_pattern_last_capture(patterns, string):
    """ last capture from the first matching pattern
    """
    pattern = first_matching_pattern(patterns, string)
    return last_capture(pattern, string)
