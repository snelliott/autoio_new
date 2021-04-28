"""
  test an intder writer
"""

import automol
import intder_io.writer
from _util import read_text_file
from _util import load_numpy_string_file


GEO = automol.geom.from_string(
    read_text_file(['data'], 'c2h6o.xyz'))
ZMA = automol.zmat.from_string(
    read_text_file(['data'], 'c2h6o.zmat'))
HESS = load_numpy_string_file(['data'], 'c2h6o.hess')


def test__input():
    """ test intder_io.writer.
    """

    inp_str = intder_io.writer.input(GEO)
    inp2_str = intder_io.writer.input(GEO, zma=ZMA)

    with open('input.dat', 'w') as fobj:
        fobj.write(inp_str)
    with open('input.dat2', 'w') as fobj:
        fobj.write(inp2_str)


def test__hess():
    """ test intder_io.writer.
    """

    hess = load_numpy_string_file(['data'], 'c2h6o.hess')

    hess_str = intder_io.writer.cart_hess_file(hess)

    with open('file15', 'w') as fobj:
        fobj.write(hess_str)


if __name__ == '__main__':
    test__input()
    test__hess()
