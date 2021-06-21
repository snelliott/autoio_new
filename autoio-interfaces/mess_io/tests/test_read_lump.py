""" test mess_io.reader._lump
"""

import os
from ioformat import pathtools
import mess_io.reader


PATH = os.path.dirname(os.path.realpath(__file__))
AUX_PATH = os.path.join(PATH, 'data', 'out')

AUX_STR = pathtools.read_file(AUX_PATH, 'well_lump.aux')

TEMP1 = 600
TEMP2 = 1200
TEMP3 = 2000
PRESSURE = 1.0


def test__():
    """ test mess_io.reader._lump.merged_wells
    """

    assert mess_io.reader.merged_wells(AUX_STR, PRESSURE, TEMP1) == (
        ('W1', 'W5'), ('W2', 'W6'))
    assert mess_io.reader.merged_wells(AUX_STR, PRESSURE, TEMP2) == (
        ('W1', 'W3', 'W5', 'W6'),)
    assert mess_io.reader.merged_wells(AUX_STR, PRESSURE, TEMP3) == (
        ('W1', 'W2', 'W4', 'W5', 'W3'),)
