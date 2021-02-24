""" tests projrot (maybe others)
"""

import tempfile
import automol
import autorun
from _util import read_text_file
from _util import load_numpy_string_file


RUN_DIR = tempfile.mkdtemp()
print(RUN_DIR)

GEO = automol.geom.from_string(
    read_text_file(['data'], 'c2h5oh.xyz'))
MESS_ROT_STR = read_text_file(['data'], 'c2h5oh.mrot')


def test__():
    """ test
    """

    script_str = autorun.SCRIPT_DCT['messpf']

    tors_freqs, tors_zpves = autorun.mess.torsions(
        script_str, RUN_DIR, GEO, MESS_ROT_STR)

    print('MESS')
    print(tors_freqs)
    print(tors_zpves)


if __name__ == '__main__':
    test__()
