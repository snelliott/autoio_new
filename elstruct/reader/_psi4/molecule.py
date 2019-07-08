""" molecular geometry and structure readers
"""
import autoread as ar
import autoparse.pattern as app
import automol


def opt_geometry(output_string):
    """ get optimized cartesian geometry from output
    """
    syms, xyzs = ar.geom.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('Final (previous) structure:'), app.LINE, '']))

    geo = automol.geom.from_data(syms, xyzs, angstrom=True)
    return geo


def opt_zmatrix(output_string):
    """ get optimized z-matrix geometry from output
    """
    # read the matrix and the values from the output
    syms, key_mat, name_mat, val_dct = ar.zmatrix.read(
        output_string,
        start_ptt=(
            app.padded(app.escape('Geometry (in Angstrom),'), app.NONNEWLINE) +
            2 * app.padded(app.NEWLINE)))

    # call the automol constructor
    zma = automol.zmatrix.from_data(
        syms, key_mat, name_mat, val_dct,
        one_indexed=True, angstrom=True, degree=True)
    return zma


if __name__ == '__main__':
    OUT_STR = open('run.out').read()
    print(opt_zmatrix(OUT_STR))
