""" Library of functions for writing and formatting strings
    that are used by all of the interface modules
"""

from ioformat._format import build_mako_str
from ioformat._format import indent
from ioformat._format import addchar
from ioformat._format import headlined_sections
from ioformat._format import remove_whitespace
from ioformat._format import remove_trail_whitespace
from ioformat._format import remove_comment_lines
from ioformat._run import from_input_string
from ioformat._run import run_script
from ioformat import pathtools
from ioformat import phycon
from ioformat import ptt

__all__ = [
    'build_mako_str',
    'indent',
    'addchar',
    'headlined_sections',
    'remove_whitespace',
    'remove_trail_whitespace',
    'remove_comment_lines',
    'from_input_string',
    'run_script',
    'pathtools',
    'phycon',
    'ptt'
]
