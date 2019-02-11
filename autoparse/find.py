""" re finders
"""
import re
from functools import partial
from ._lib import STRING_START as _STRING_START
from ._lib import STRING_END as _STRING_END
from ._lib import NEWLINE as _NEWLINE
from ._lib import SPACES as _SPACES


def has_match(pattern, string):
    """ does this string have a pattern match?
    """
    match = re.search(pattern, string, flags=re.MULTILINE)
    return bool(match)


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
