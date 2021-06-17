""" Utilility functions to format the data into strings appropriate
    for INTDER input files.
"""

import os
from itertools import chain
import automol.geom
import automol.zmat
import automol.util
from ioformat import build_mako_str
from ioformat import indent


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')


def header_format(geo):
    """ format the header
    """

    natom = automol.geom.count(geo)
    if not automol.geom.is_linear(geo):
        nintl = 3 * natom - 6
    else:
        nintl = 3 * natom - 5

    header_keys = {'natom': natom, 'nintl': nintl,
                   'comment': ''}
    return build_mako_str(
        template_file_name='header.mako',
        template_src_path=TEMPLATE_PATH,
        template_keys=header_keys)


def internals_format(zma):
    """ Format the strings with the internal coordinates
    """

    key_mat = automol.zmat.key_matrix(zma)

    # Write the stretch, bend, and torsion coordinates
    intl_str = ''
    for i, row in enumerate(key_mat[1:]):
        intl_str += 'STRE{0:>6d}{1:>6d}\n'.format(
            i+1, row[0])
    for i, row in enumerate(key_mat[2:]):
        intl_str += 'BEND{0:>6d}{1:>6d}{2:>6d}\n'.format(
            i+2, row[0], row[1])
    for i, row in enumerate(key_mat[3:]):
        intl_str += 'TORS{0:>6d}{1:>6d}{2:>6d}{3:>6d}\n'.format(
            i+3, row[0], row[1], row[2])

    # Remove final newline character
    intl_str.rstrip()

    return intl_str


def geometry_format(geo):
    """ Format the geometry string
    """

    # Build geom str
    geo_str = ''
    for (_, xyz) in geo:
        geo_str += '{:>14.5f}{:>14.5f}{:>14.5f}\n'.format(*xyz)

    # Remove final newline character and indent the lines
    geo_str = indent(geo_str.rstrip(), 4)

    return geo_str


def symbols_format(geo):
    """ Format the symbols
    """

    symbs = automol.geom.symbols(geo)
    symb_str = automol.util.vec.string(
        symbs, num_per_row=6, val_format='{0:>6s}')

    symb_str = indent(symb_str, 6)

    return symb_str


def hessian_format(hess):
    """ Format a mass-weighted Hessian into a string for the
        auxiliary input file for INTDER.

        :param hess: mass-weighted Hessian
        :type hess: numpy.ndarray
        :rtype: str
    """

    # Flatten the Hessian out for ease of writing the string
    hess = tuple(chain.from_iterable(hess))
    hess_str = automol.util.vec.string(
        hess, num_per_row=3, val_format='{0:>20.10f}')

    return hess_str
