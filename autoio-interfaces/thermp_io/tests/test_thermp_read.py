""" Test reading files for ThermP
"""

import os
import numpy
from ioformat import pathtools
import thermp_io


PATH = os.path.dirname(os.path.realpath(__file__))
DAT_PATH = os.path.join(PATH, 'data')

OUT_STR1 = pathtools.read_file(DAT_PATH, 'thermp.out', PATH)
OUT_STR2 = ''


def test__hf298k():
    """ test thermp_io.readar.hf298k
    """

    # All values from file, but reader only returning first
    ref_hf298k = (0.1146914955191809, 0.08766401512449826,
                  0.07924181529799032, 0.0810591889970729)

    hf298k_1 = thermp_io.reader.hf298k(OUT_STR1)
    assert numpy.allclose(hf298k_1, ref_hf298k[0])

    hf298k_2 = thermp_io.reader.hf298k(OUT_STR2)
    assert hf298k_2 is None
