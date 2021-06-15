""" Library of functions for writing and formatting strings
    that are used by all of the interface modules
"""

from ioformat._format import build_mako_str
from ioformat._format import indent
from ioformat._format import addchar
from ioformat._format import headlined_sections
from ioformat._format import remove_whitespace_from_string
from ioformat._format import remove_trail_whitespace
from ioformat._format import remove_comment_lines
from ioformat import pathtools
from ioformat import phycon
from ioformat import ptt
from ioformat._util import read_text_file
from ioformat._util import write_text_file
from ioformat._util import load_numpy_string_file


__all__ = [
    'build_mako_str',
    'indent',
    'addchar',
    'headlined_sections',
    'remove_whitespace_from_string',
    'remove_trail_whitespace',
    'remove_comment_lines',
    'addchar',
    'pathtools',
    'phycon',
    'ptt',
    'read_text_file',
    'write_text_file',
    'load_numpy_string_file',

]
