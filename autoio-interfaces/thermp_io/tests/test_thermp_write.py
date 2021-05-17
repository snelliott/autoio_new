""" Test writing files for ThermP
"""
import os

from ioformat import read_text_file
import thermp_io


PATH = os.path.dirname(os.path.realpath(__file__))
TEMPS = (100.0, 200.0, 300.0, 400.0, 500.0,
         600.0, 700.0, 800.0, 900.0, 1000.0)
NTEMPS = len(TEMPS)
FORMULA = 'CH4'
H0FORM = -123.45
ENTHALPYT = 0.
BREAKT = 1000.


def test__input_file():
    """ test thermp_io.writer.input_file
    """

    inp_str = thermp_io.writer.input_file(
        NTEMPS,
        formula=FORMULA,
        delta_h=H0FORM,
        enthalpy_temp=ENTHALPYT,
        break_temp=BREAKT)
    assert inp_str == read_text_file(['data'], 'thermp.inp', PATH)


if __name__ == '__main__':
    test__input_file()
