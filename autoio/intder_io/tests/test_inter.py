"""
  test an intder writer
"""

import os
import automol
import intder_io.writer
from ioformat import read_text_file
from ioformat import write_text_file
from ioformat import load_numpy_string_file


PATH = os.path.dirname(os.path.realpath(__file__))
GEO = automol.geom.from_string(
    read_text_file(['data'], 'c2h6o.xyz', path=PATH))
ZMA = automol.zmat.from_string(
    read_text_file(['data'], 'c2h6o.zmat', path=PATH))
HESS = load_numpy_string_file(['data'], 'c2h6o.hess', path=PATH)


def test__input():
    """ test intder_io.writer.
    """

    inp_str = intder_io.writer.input(GEO)
    inp2_str = intder_io.writer.input(GEO, zma=ZMA)

    write_text_file(['data'], 'input.dat', inp_str, path=PATH)
    write_text_file(['data'], 'input.dat2', inp2_str, path=PATH)


def test__hess():
    """ test intder_io.writer.
    """

    hess = load_numpy_string_file(['data'], 'c2h6o.hess', path=PATH)
    hess_str = intder_io.writer.cart_hess_file(hess)
    write_text_file(['data'], 'file15', hess_str, path=PATH)


if __name__ == '__main__':
    test__input()
    test__hess()
