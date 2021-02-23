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
ZMA = automol.zmat.from_string(
    read_text_file(['data'], 'c2h5oh.zmat'))
GRAD = load_numpy_string_file(['data'], 'c2h5oh.grad')
HESS = load_numpy_string_file(['data'], 'c2h5oh.hess')

GEOS = (GEO,)
GRADS = (GRAD,)
HESSIANS = (HESS,)
PROJROT_ROT_STR = read_text_file(['data'], 'c2h5oh.prot')
MESS_ROT_STR = read_text_file(['data'], 'c2h5oh.mrot')


def test__():
    """ test
    """

    # Run MESS for torsions
    script_str = autorun.SCRIPT_DCT['messpf']
    tors_freqs, tors_zpves = autorun.mess.torsions(
        script_str, RUN_DIR, GEO, MESS_ROT_STR)
    print('MESS')
    print(tors_freqs)
    print(tors_zpves)

    # Run ProjRot for frequencies
    script_str = autorun.SCRIPT_DCT['projrot']
    f1, f2, f3, f4 = autorun.projrot.frequencies(
        script_str, RUN_DIR, GEOS, GRADS, HESSIANS,
        rotors_str=PROJROT_ROT_STR)
    print('PROJROT')
    print(f1)
    print(f2)
    print(f3)
    print(f4)

    # Run thermo
    hform298, nasa_poly = autorun.thermo(
        script_str, run_dir,
        pf_str, formula, hform0, temps,
        enthalpyt=0.0, breakt=1000.0, convert=False)
    print('THERM')
    print(hform298)
    print(nasa_poly)


if __name__ == '__main__':
    test__()
