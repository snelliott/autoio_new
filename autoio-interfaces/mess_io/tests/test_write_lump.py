""" test mess_io.writer._lump
"""

import os
from ioformat import read_text_file
import mess_io.writer


PATH = os.path.dirname(os.path.realpath(__file__))

WELL_MERGE_LST = (
    ('W2', 'W1'),
    ('W5', 'W4', 'W3'),
    ('W9', 'W8', 'W7', 'W6')
)


def test__():
    """ test mess_io.writer._lump.well_lump_scheme
    """

    ref_lump1_str = read_text_file(['data', 'inp'], 'well_lump1.inp', PATH)
    ref_lump2_str = read_text_file(['data', 'inp'], 'well_lump2.inp', PATH)

    lump1_str = mess_io.writer.well_lump_scheme(WELL_MERGE_LST)
    lump2_str = mess_io.writer.well_lump_scheme(
        WELL_MERGE_LST, separator='-')

    assert lump1_str == ref_lump1_str.rstrip()
    assert lump2_str == ref_lump2_str.rstrip()
