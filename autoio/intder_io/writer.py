"""
 make an FCMINT
"""

import automol
from intder_io import util


def input(geo, zma=None):
    """ ZMatrix
    """

    if zma is None:
        zma = automol.geom.zmatrix(geo)

    inp_str = (
        util.header_format(geo) + '\n' +
        util.internals_format(zma) + '\n' +
        util.geometry_format(geo) + '\n' +
        util.symbols_format(geo)
    )

    return inp_str


def cart_hess_file(hess):
    """ Write a file with the Cartesian Hessian
    """

    # Put in the dimensions of the Hessian
    natom = len(hess)
    hess_str = '{0:>6d}{1:>6d}\n'.format(natom, natom*3)
    hess_str += util.hessian_format(hess)

    return hess_str
