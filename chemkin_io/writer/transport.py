"""
 writes the string for the chemkin
"""

from chemkin_io.writer import util

# convert wavenumbers to Kelvin (check)
CM2K = 1.438776877


def properties(trans_dct):
    """ Writes the string in containing data from several mechanism species
        used in calculating transport properties during ChemKin simulations.

        :param names: names of each species
        :type names: list(string)
        :param geos: geometries of each species
        :type geos: list
        :param epsilons: Lennard-Jones epsilon param. for each species (K)
        :type epsilons: list(float)
        :param sigmas: Lennard-Jones sigma param. for each species (Angstrom)
        :type sigmas: list(float)
        :param tot_dip_moms: Total dipole moment of each species (Debye)
        :type tot_dip_moms: list(float)
        :param polars: Mean static polarizability of each species (Angstrom^3)
        :type polars: list(float)
        :param z_rots: 298 K rotational relazxation collision number
        :type z_rots: type(float)
        :return: chemkin_str: ChemKin string with data
        :rtype: str
    """

    # Find the length of the longest name string for formatting
    nameslen = util.name_column_length(list(trans_dct.keys()))

    # Initialize string with common header
    chemkin_str = util.HEADER_STR
    chemkin_str += '\n'

    # Add the headers for each of the columns
    chemkin_str += (
        '{0:<'+nameslen+'}'.format('! Species'),
        '{1:>5d}'.format('Shape'),
        '{2:>12.3f}'.format('Epsilon'),
        '{3:>8.3f}'.format('Sigma'),
        '{4:>8.3f}'.format('Mu'),
        '{5:>8.3f}'.format('Alpha'),
        '{6:>8.3f}'.format('Z_Rot'),
    )

    # Add the values to the string
    for name, dct in trans_dct.items():
        shape_idx = dct.get('shape_idx', 2)
        eps = dct.get('epsilon', 0.00) * CM2K
        sigma = dct.get('sigma', 0.00) * BOHR2ANG
        dip_mom = dct.get('dip_mom', 0.00)
        polar = dct.get('polarizability', 0.00) * BOHR32ANG3
        zrot = dct.get('zrot', 1.00) 

        chemkin_str += (
            '{0:<'+nameslen+'}'.format(name),
            '{1:>5d}'.format(shape),
            '{2:>12.3f}'.format(eps),
            '{3:>8.3f}'.format(sig),
            '{4:>8.3f}'.format(dmom),
            '{5:>8.3f}'.format(polar),
            '{6:>8.3f}'.format(zrot)
        )
        chemkin_str += '\n'

    return chemkin_str
