""" cartesian geometry writers
"""


def write(syms, xyzs):
    """ write a geometry to a string
    """
    natms = len(syms)
    assert len(xyzs) == natms

    geo_str = '\n'.join('{:2s} {:10.6f} {:10.6f} {:10.6f}'.format(sym, *xyz)
                        for sym, xyz in zip(syms, xyzs))
    return geo_str


def write_xyz(syms, xyzs, comment=''):
    """ write a geometry to a .xyz string
    """
    natms = len(syms)
    assert len(xyzs) == natms

    geo_str = write(syms=syms, xyzs=xyzs)
    xyz_str = '{:d}\n{:s}\n{:s}'.format(natms, comment, geo_str)
    return xyz_str
