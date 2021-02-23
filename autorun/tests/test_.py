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

NAME = 'Methane'
FORMULA = {'C': 1, 'H': 4}
HFORM0 = -123.45
ENTHALPYT = 0.
BREAKT = 1000.
PF_STR = read_text_file(['data'], 'pf.dat')


def test__1():
    """ test
    """

    # Run MESS for torsions
    script_str = autorun.SCRIPT_DCT['messpf']
    tors_freqs, tors_zpves = autorun.mess.torsions(
        script_str, RUN_DIR, GEO, MESS_ROT_STR)
    print('MESS')
    print(tors_freqs)
    print(tors_zpves)


def test__2():
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


def test__3():
    """ test
    """

    # Run thermo
    formula_str = automol.formula.string(FORMULA)
    thermp_script_str = autorun.SCRIPT_DCT['thermp']
    pac99_script_str = autorun.SCRIPT_DCT['pac99'].format(formula_str)
    hform298, nasa_poly = autorun.thermo.direct(
        thermp_script_str, pac99_script_str, RUN_DIR,
        PF_STR, NAME, FORMULA, HFORM0,
        enthalpyt=ENTHALPYT, breakt=BREAKT, convert=True)
    print('THERM')
    print(hform298)
    print(nasa_poly)


if __name__ == '__main__':
    # test__1()
    # test__2()
    test__3()
