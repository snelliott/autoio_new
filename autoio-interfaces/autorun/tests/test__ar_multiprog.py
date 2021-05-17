""" tests projrot (maybe others)
"""

import os
import tempfile
import automol
from ioformat import read_text_file
import autorun
# from ioformat import load_numpy_string_file


PATH = os.path.dirname(os.path.realpath(__file__))

NAME = 'Methane'
FORMULA = {'C': 1, 'H': 4}
HFORM0 = -123.45
ENTHALPYT = 0.
BREAKT = 1000.
PF_STR = read_text_file(['data'], 'pf.dat', path=PATH)


def test__thermo():
    """ test
    """

    formula_str = automol.formula.string(FORMULA)

    thermp_script_str = autorun.SCRIPT_DCT['thermp']
    pac99_script_str = autorun.SCRIPT_DCT['pac99'].format(formula_str)

    with tempfile.TemporaryDirectory(dir=PATH) as run_dir:
        hform298, nasa_poly = autorun.thermo(
            thermp_script_str, pac99_script_str, run_dir,
            PF_STR, NAME, FORMULA, HFORM0,
            enthalpyt=ENTHALPYT, breakt=BREAKT, convert=True)

    print('THERM')
    print(hform298)
    print(nasa_poly)


# def test__projected_frequencies():
#     """ test
#     """
#
#     mess_script_str = autorun.SCRIPT_DCT['messpf']
#     projrot_script_str = autorun.SCRIPT_DCT['projrot']
#
#     with tempfile.TemporaryDirectory(dir=PATH) as run_dir:
#        proj_freqs, proj_imag_freqs, proj_zpe = autorun.projected_frequencies(
#             mess_script_str, projrot_script_str, run_dir,
#             mess_hr_str, projrot_hr_str,
#             mess_geo, projrot_geo, hess)
#
#     print(proj_freqs, proj_imag_freqs, proj_zpe)


if __name__ == '__main__':
    test__thermo()
    # test__projected_frequencies
