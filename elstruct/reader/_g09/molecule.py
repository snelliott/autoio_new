""" molecular geometry and structure readers
"""
import autoread as ar
import autoparse.pattern as app
import phycon.elements as pce
import automol


def opt_geometry(output_string):
    """ get optimized geometry from output
    """
    nums, xyzs = ar.geom.read(
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
    syms, key_mat, name_mat = ar.zmatrix.matrix.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('Symbolic Z-matrix:'), app.LINE, '']),
        line_end_ptt=app.maybe(app.UNSIGNED_INTEGER),
        last=False)

    # read the values from the end of the output
    val_dct = ar.zmatrix.setval.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.padded('Optimized Parameters', app.NONNEWLINE),
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


if __name__ == '__main__':
    ZMA = opt_zmatrix(open('run.out').read())
    print(automol.zmatrix.string(ZMA))
