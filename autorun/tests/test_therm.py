""" tests projrot (maybe others)
"""

import tempfile
import automol
import autorun
from _util import read_text_file
from _util import load_numpy_string_file


RUN_DIR = tempfile.mkdtemp()
print(RUN_DIR)

NAME = 'Methane'
FORMULA = {'C': 1, 'H': 4}
HFORM0 = -123.45
ENTHALPYT = 0.
BREAKT = 1000.
PF_STR = read_text_file(['data'], 'pf.dat')


def test__():
    """ test
    """

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
    test__()
