""" test mess_io.reader._lump
"""

import os
from ioformat import read_text_file
import mess_io.reader


PATH = os.path.dirname(os.path.realpath(__file__))
AUX_STR = read_text_file(['data', 'out'], 'well_lump.aux', PATH)


def test__():
    """ test mess_io.reader._lump.merged_wells
    """

    assert mess_io.reader.merged_wells(AUX_STR, 600) == (
        ('W1', 'W5'), ('W2', 'W6'))
    assert mess_io.reader.merged_wells(AUX_STR, 1200) == (
        ('W1', 'W3', 'W5', 'W6'),)
    assert mess_io.reader.merged_wells(AUX_STR, 2000) == (
        ('W1', 'W2', 'W4', 'W5', 'W3'),)
