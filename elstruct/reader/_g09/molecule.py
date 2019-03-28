""" molecular geometry and structure readers
"""
import autoparser as apr
import autoparse.pattern as app
import phycon.elements as pce
import automol


def opt_geometry(output_string):
    """ get optimized geometry from output
    """
    nums, xyzs = apr.geom.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('Standard orientation:'),
            app.LINE, app.LINE, app.LINE, app.LINE, '']),
        sym_ptt=app.UNSIGNED_INTEGER,
        line_start_ptt=app.UNSIGNED_INTEGER,
        line_sep_ptt=app.UNSIGNED_INTEGER,)
    syms = tuple(map(pce.symbol, nums))
    geo = automol.constructors.geom.from_data(syms, xyzs, angstrom=True)
    return geo


def opt_zmatrix(output_string):
    """ get optimized z-matrix geometry from output
    """
    # read the matrix from the beginning of the output
    syms, key_mat, name_mat = apr.zmatrix.matrix.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('Symbolic Z-matrix:'), app.LINE, '']),
        last=False)

    # read the values from the end of the output
    val_dct = apr.zmatrix.setval.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('!   Optimized Parameters   !'),
            app.LINE, app.LINE, app.LINE, app.LINE, '']),
        entry_sep_ptt='',
        entry_start_ptt=app.escape('!'),
        sep_ptt=app.maybe(app.LINESPACES).join([
            app.escape('-DE/DX ='), app.FLOAT, app.escape('!'), app.NEWLINE]),
        last=True)

    # call the automol constructor
    zma = automol.constructors.zmatrix.from_data(
        syms, key_mat, name_mat, val_dct,
        one_indexed=True, angstrom=True, degree=True)
    return zma
