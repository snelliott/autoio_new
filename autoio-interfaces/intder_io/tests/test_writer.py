""" test intder_io.writer
"""

import os
import automol
from ioformat import pathtools
import intder_io.writer


PATH = os.path.dirname(os.path.realpath(__file__))
DAT_PATH = os.path.join(PATH, 'data')

C2H5OH_GEO = automol.geom.from_string(
    pathtools.read_file(DAT_PATH, 'c2h5oh.xyz'))
C2H5OH_ZMA = automol.zmat.from_string(
    pathtools.read_file(DAT_PATH, 'c2h5oh.zmat'))
C2H5OH_HESS = pathtools.read_numpy_file(DAT_PATH, 'c2h5oh.hess')

HCCH_GEO = automol.geom.from_string(
    pathtools.read_file(DAT_PATH, 'hcch.xyz'))


def test__input():
    """ test intder_io.writer.input_file
    """

    inp_str = intder_io.writer.input_file(C2H5OH_GEO)
    inp2_str = intder_io.writer.input_file(C2H5OH_GEO, zma=C2H5OH_ZMA)
    inp3_str = intder_io.writer.input_file(HCCH_GEO)

    pathtools.write_file(inp_str, DAT_PATH, 'input1.dat')
    pathtools.write_file(inp2_str, DAT_PATH, 'input2.dat')
    pathtools.write_file(inp3_str, DAT_PATH, 'input3.dat')

    assert inp_str == pathtools.read_file(DAT_PATH, 'input1.dat')
    assert inp2_str == pathtools.read_file(DAT_PATH, 'input2.dat')
    assert inp3_str == pathtools.read_file(DAT_PATH, 'input3.dat')


def test__hess():
    """ test intder_io.writer.cart_hess_file
    """

    hess_str = intder_io.writer.cart_hess_file(C2H5OH_HESS)
    pathtools.write_file(hess_str, DAT_PATH, 'file15')

    assert hess_str == pathtools.read_file(DAT_PATH, 'file15')
