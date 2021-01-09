""" molecular geometry and structure readers
"""
import autoread as ar
import autoparse.pattern as app
import automol


def opt_geometry(output_str):
    """ Reads the optimized molecular geometry (in Cartesian coordinates) from
        the output file string. Returns the geometry in Bohr.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: automol molecular geometry data structure
    """

    syms, xyzs = ar.geom.read(
        output_str,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('Final (previous) structure:'), app.LINE, '']))

    geo = automol.geom.from_data(syms, xyzs, angstrom=True)

    return geo


def opt_zmatrix(output_str):
    """ Reads the optimized Z-Matrix from the output file string.
        Returns the Z-Matrix in Bohr and Radians.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: automol molecular geometry data structure
    """

    # Read the matrix and the values from the output
    syms, key_mat, name_mat, val_dct = ar.zmatrix.read(
        output_str,
        start_ptt=(
            app.padded(app.escape('Geometry (in Angstrom),'), app.NONNEWLINE) +
            2 * app.padded(app.NEWLINE)))

    # Call the automol constructor
    if all(x is not None for x in (syms, key_mat, name_mat, val_dct)):
        zma = automol.zmatrix.from_data(
            syms, key_mat, name_mat, val_dct,
            one_indexed=True, angstrom=True, degree=True)
    else:
        zma = None

    return zma
