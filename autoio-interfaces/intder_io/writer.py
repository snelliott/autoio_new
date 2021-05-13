""" Write the INTDER main and auxiliary input file
"""

import automol.geom
import intder_io._util as intder_util


def input_file(geo, zma=None):
    """ Write the main INTDER input file. Currently
        just supports a basic harmonic frequency and
        total energy distribution calculation.

        :param geo: geometry to build input for
        :type geo: automol geometry data structure
        :param zma: Z-Matrix corresponding to geometry
        :type zma: automol Z-Matrix data structure
        :rtype: str
    """

    if zma is None:
        zma = automol.geom.zmatrix(geo)

    inp_str = (
        intder_util.header_format(geo) + '\n' +
        intder_util.internals_format(zma) + '\n' +
        intder_util.geometry_format(geo) + '\n' +
        intder_util.symbols_format(geo)
    )

    return inp_str


def cart_hess_file(hess):
    """ Write a file with the Cartesian Hessian auxiliary
        input that corresponds to the FCMINT file for CFOUR.

        :param hess: mass-weighted Hessian (in a.u.)
        :type hess: numpy.ndarray
        :rtype: str
    """

    natom = len(hess)
    hess_str = '{0:>6d}{1:>6d}\n'.format(natom, natom*3)
    hess_str += intder_util.hessian_format(hess)

    return hess_str
