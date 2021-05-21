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

    ref_well_merge_lst = (
        ('W2', 'W1'),
        ('W5', 'W4', 'W3'),
        ('W9', 'W8', 'W7', 'W6')
    )

    well_merge_lst = mess_io.reader.merged_wells(AUX_STR)

    assert well_merge_lst == ref_well_merge_lst
