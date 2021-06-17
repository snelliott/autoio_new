""" test intder_io.writer
"""

import os
import automol
from ioformat import read_text_file
from ioformat import write_text_file
from ioformat import load_numpy_string_file
import intder_io.writer


PATH = os.path.dirname(os.path.realpath(__file__))

C2H5OH_GEO = automol.geom.from_string(
    read_text_file(['data'], 'c2h5oh.xyz', path=PATH))
C2H5OH_ZMA = automol.zmat.from_string(
    read_text_file(['data'], 'c2h5oh.zmat', path=PATH))
C2H5OH_HESS = load_numpy_string_file(['data'], 'c2h5oh.hess', path=PATH)

HCCH_GEO = automol.geom.from_string(
    read_text_file(['data'], 'hcch.xyz', path=PATH))


def test__input():
    """ test intder_io.writer.input_file
    """

    inp_str = intder_io.writer.input_file(C2H5OH_GEO)
    inp2_str = intder_io.writer.input_file(C2H5OH_GEO, zma=C2H5OH_ZMA)
    inp3_str = intder_io.writer.input_file(HCCH_GEO)

    write_text_file(['data'], 'input1.dat', inp_str, path=PATH)
    write_text_file(['data'], 'input2.dat', inp2_str, path=PATH)
    write_text_file(['data'], 'input3.dat', inp3_str, path=PATH)

    assert inp_str == read_text_file(['data'], 'input1.dat', path=PATH)
    assert inp2_str == read_text_file(['data'], 'input2.dat', path=PATH)
    assert inp3_str == read_text_file(['data'], 'input3.dat', path=PATH)


def test__hess():
    """ test intder_io.writer.cart_hess_file
    """

    hess_str = intder_io.writer.cart_hess_file(C2H5OH_HESS)
    write_text_file(['data'], 'file15', hess_str, path=PATH)

    assert hess_str == read_text_file(['data'], 'file15', path=PATH)


if __name__ == "__main__":
    test__input()
