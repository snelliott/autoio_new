""" tests projrot (maybe others)
"""

import os
import tempfile
import numpy
import automol
from ioformat import read_text_file
import autorun


PATH = os.path.dirname(os.path.realpath(__file__))

GEO = automol.geom.from_string(
    read_text_file(['data'], 'c2h5oh.xyz', path=PATH))
MESS_ROT_STR = read_text_file(['data'], 'c2h5oh.mrot', path=PATH)


def test__():
    """ test
    """

    ref_tors_freqs = (263.39, 320.923)
    ref_tors_zpves = (0.0005850015264154265, 0.0006727675639040085)

    with tempfile.TemporaryDirectory(dir=PATH) as run_dir:
        script_str = autorun.SCRIPT_DCT['messpf']

        tors_freqs, tors_zpves = autorun.mess.torsions(
            script_str, run_dir, GEO, MESS_ROT_STR)

        assert numpy.allclose(tors_freqs, ref_tors_freqs)
        assert numpy.allclose(tors_zpves, ref_tors_zpves)


if __name__ == '__main__':
    test__()
