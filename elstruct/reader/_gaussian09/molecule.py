""" molecular geometry and structure readers
"""
import numbers
from qcelemental import periodictable as pt
import autoread as ar
import autoparse.pattern as app
import autoparse.find as apf
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
    syms = tuple(map(pt.to_E, nums))
    geo = automol.geom.from_data(syms, xyzs, angstrom=True)
    return geo


def opt_zmatrix(output_string):
    """ get optimized z-matrix geometry from output
    """
    # read the matrix from the beginning of the output
    syms, key_mat, name_mat = ar.zmatrix.matrix.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('Symbolic Z-matrix:'), app.LINE, '']),
        sym_ptt=ar.par.Pattern.ATOM_SYMBOL + app.maybe(app.UNSIGNED_INTEGER),
        key_ptt=app.one_of_these([app.UNSIGNED_INTEGER, app.VARIABLE_NAME]),
        line_end_ptt=app.maybe(app.UNSIGNED_INTEGER),
        last=False)

    # read the values from the end of the output
    if len(syms) == 1:
        val_dct = {}
    else:
        val_dct = ar.zmatrix.setval.read(
            output_string,
            start_ptt=app.padded(app.NEWLINE).join([
                app.padded('Optimized Parameters', app.NONNEWLINE),
                app.LINE, app.LINE, app.LINE, app.LINE, '']),
            entry_sep_ptt='',
            entry_start_ptt=app.escape('!'),
            sep_ptt=app.maybe(app.LINESPACES).join([
                app.escape('-DE/DX ='), app.FLOAT, app.escape('!'),
                app.NEWLINE]),
            last=True)

    # for the case when variable names are used instead of integer keys:
    # (otherwise, does nothing)
    key_dct = dict(map(reversed, enumerate(syms)))
    key_dct[None] = 0
    key_mat = [[key_dct[val]+1 if not isinstance(val, numbers.Real) else val
                for val in row] for row in key_mat]
    sym_ptt = app.STRING_START + app.capturing(ar.par.Pattern.ATOM_SYMBOL)
    syms = [apf.first_capture(sym_ptt, sym) for sym in syms]

    # call the automol constructor
    zma = automol.zmatrix.from_data(
        syms, key_mat, name_mat, val_dct,
        one_indexed=True, angstrom=True, degree=True)
    return zma
