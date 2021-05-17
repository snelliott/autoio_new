""" tests projrot (maybe others)
"""

import os
import tempfile
import automol
from ioformat import read_text_file
from ioformat import load_numpy_string_file
import autorun


PATH = os.path.dirname(os.path.realpath(__file__))

GEO = automol.geom.from_string(
    read_text_file(['data'], 'c2h5oh.xyz', path=PATH))
GRAD = load_numpy_string_file(['data'], 'c2h5oh.grad', path=PATH)
HESS = load_numpy_string_file(['data'], 'c2h5oh.hess', path=PATH)

GEOS = (GEO,)
GRADS = (GRAD,)
HESSIANS = (HESS,)
PROJROT_ROT_STR = read_text_file(['data'], 'c2h5oh.prot', path=PATH)


def test__():
    """ test
    """

    # Run ProjRot for frequencies
    script_str = autorun.SCRIPT_DCT['projrot']
    with tempfile.TemporaryDirectory(dir=PATH) as run_dir:
        fa1, fa2, fa3, fa4 = autorun.projrot.frequencies(
            script_str, run_dir, GEOS, GRADS, HESSIANS,
            rotors_str=PROJROT_ROT_STR)
    print('PROJROT')
    print(fa1)
    print(fa2)
    print(fa3)
    print(fa4)


if __name__ == '__main__':
    test__()
