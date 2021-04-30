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
GRAD = load_numpy_string_file(['data'], 'c2h5oh.grad')
HESS = load_numpy_string_file(['data'], 'c2h5oh.hess')

GEOS = (GEO,)
GRADS = (GRAD,)
HESSIANS = (HESS,)
PROJROT_ROT_STR = read_text_file(['data'], 'c2h5oh.prot')


def test__():
    """ test
    """

    # Run ProjRot for frequencies
    script_str = autorun.SCRIPT_DCT['projrot']
    fa1, fa2, fa3, fa4 = autorun.projrot.frequencies(
        script_str, RUN_DIR, GEOS, GRADS, HESSIANS,
        rotors_str=PROJROT_ROT_STR)
    print('PROJROT')
    print(fa1)
    print(fa2)
    print(fa3)
    print(fa4)


if __name__ == '__main__':
    test__()
