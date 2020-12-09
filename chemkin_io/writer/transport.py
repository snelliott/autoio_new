"""
 writes the string for the chemkin
"""

from chemkin_io.writer import _util as util

# conversion factors
CM2K = 1.438776877
BOHR2ANG = 0.529177
BOHR2ANG_3 = BOHR2ANG**3


def properties(trans_dct):
    """ Writes the string in containing data from several mechanism species
        used in calculating transport properties during ChemKin simulations.

        :param trans_dct:
        :type dict: {name:
            geos (bohr),
            epsilons (K)
            sigmas (Angstrom)
            tot_dip_moms (Debye)
            polars (Angstrom^3)
            z_rots}
        :return: chemkin_str: ChemKin string with data
        :rtype: str
    """

    # Find the length of the longest name string for formatting
    # nameslen = util.name_column_length(list(trans_dct.keys()))

    # Initialize string with common header
    chemkin_str = util.CKIN_TRANS_HEADER_STR
    chemkin_str += '\n'

    # Add the headers for each of the columns
    # '{0:<'+nameslen+'}'.format('! Species'),
    chemkin_str += (
        '{0:20s}'.format('! Species') +
        '{0:>5s}'.format('Shape') +
        '{0:>12s}'.format('Epsilon') +
        '{0:>8s}'.format('Sigma') +
        '{0:>8s}'.format('Mu') +
        '{0:>8s}'.format('Alpha') +
        '{0:>8s}'.format('Z_Rot')
    )
    chemkin_str += '\n'

    # Add the values to the string
    for name, dct in trans_dct.items():
        shape_idx = dct.get('shape_idx', 2)
        eps = dct.get('epsilon', 0.00) * CM2K
        sig = dct.get('sigma', 0.00) * BOHR2ANG
        dmom = dct.get('dipole_moment', 0.00)
        polar = dct.get('polarizability', 0.00) * BOHR2ANG_3
        zrot = dct.get('zrot', 1.00)

        # '{0:<'+nameslen+'}'.format(name),
        chemkin_str += (
            '{0:20s}'.format(name) +
            '{0:>5d}'.format(shape_idx) +
            '{0:>12.3f}'.format(eps) +
            '{0:>8.3f}'.format(sig) +
            '{0:>8.3f}'.format(dmom) +
            '{0:>8.3f}'.format(polar) +
            '{0:>8.3f}'.format(zrot)
        )
        chemkin_str += '\n'

    return chemkin_str
