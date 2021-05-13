""" utility
"""

from itertools import chain
import automol
import ioformat


HEADER_STR = """# FILES #
intder

Total Energy distribution

# 1       2   3    4    5    6    7    8    9   10   11   12   13   14   15   16 #
  {}     {}    0    2    0 2000    0    0    0    1    3    0    0    0    0    0"""


def header_format(geo):
    """ format the header
    """

    natom = automol.geom.count(geo)
    if not automol.geom.is_linear(geo):
        nintl = 3 * natom - 6
    else:
        nintl = 3 * natom - 5

    header_str = HEADER_STR.format(natom, nintl)

    return header_str


def internals_format(zma):
    """ Format the strings with the internal coordinates
    """

    key_mat = automol.zmat.key_matrix(zma)

    # Write the stretch, bend, and torsion coordinates
    intl_str = ''
    for i, row in enumerate(key_mat[1:]):
        print(row)
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
    geo_str = ioformat.indent(geo_str.rstrip(), 4)

    return geo_str


def symbols_format(geo):
    """ Format the symbols
    """

    symbs = automol.geom.symbols(geo)
    # nsymbs = len(symbs)

    symb_str = automol.util.vec.string(
        symbs, num_per_row=6, val_format='{0:>6s}')
    # for i, symb in enumerate(symbs):
    #     if ((i+1) % 6) == 0 and (i+1) != nsymbs:
    #         symb_str += '{0:>6s}\n'.format(symb)
    #     else:
    #         symb_str += '{0:>6s}'.format(symb)

    symb_str = ioformat.indent(symb_str, 6)

    return symb_str


def hessian_format(hess):
    """ format hessian
    """

    # Flatten the Hessian and print
    # natom = len(hess)
    hess = list(chain.from_iterable(hess))

    hess_str = automol.util.vec.string(
        hess, num_per_row=3, val_format='{0:>20.10f}')
    # hess_str = ''
    # for i, val in enumerate(hess):
    #     hess_str += '{0:>20.10f}'.format(val)
    #     if ((i+1) % 3) == 0 and (i+1) != natom:
    #         hess_str += '\n'

    return hess_str
