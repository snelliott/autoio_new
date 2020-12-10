"""
 tests torsional mode reader
"""

import os
import numpy
import mess_io


PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PATH, 'data')
DATA_NAME = 'mess.log'
with open(os.path.join(DATA_PATH, DATA_NAME), 'r') as datfile:
    OUT_STR = datfile.read()


def test__tors():
    """ test mess_io.reader.tors
    """

    freqs = mess_io.reader.tors.freqs(
        output_string=OUT_STR)
    zpves = mess_io.reader.tors.zpves(
        output_string=OUT_STR)

    ref_freqs = (235.630, 152.547, 227.806)
    ref_zpves = (0.33087, 1.28022, 0.03015)

    assert numpy.allclose(freqs, ref_freqs)
    assert numpy.allclose(zpves, ref_zpves)


if __name__ == '__main__':
    test__tors()
