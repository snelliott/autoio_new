""" molecular geometry and structure readers
"""

import numbers
from qcelemental import periodictable as pt
import autoread as ar
import autoparse.pattern as app
import autoparse.find as apf
import automol


def opt_geometry(output_str):
    """ Reads the optimized molecular geometry (in Cartesian coordinates) from
        the output file string. Returns the geometry in Bohr.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: automol molecular geometry data structure
    """

    nums, xyzs = ar.geom.read(
        output_str,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('Standard orientation:'),
            app.LINE, app.LINE, app.LINE, app.LINE, '']),
        symb_ptt=app.UNSIGNED_INTEGER,
        line_start_ptt=app.UNSIGNED_INTEGER,
        line_sep_ptt=app.UNSIGNED_INTEGER,)
    syms = tuple(map(pt.to_E, nums))
    geo = automol.geom.from_data(syms, xyzs, angstrom=True)

    return geo


def opt_zmatrix(output_str):
    """ Reads the optimized Z-Matrix (in Cartesian coordinates) from
        the output file string. Returns the Z-Matrix in Bohr and Radians.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: automol molecular geometry data structure
    """

    # Reads the matrix from the beginning of the output
    syms, key_mat, name_mat = ar.zmatrix.matrix.read(
        output_str,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('Symbolic Z-matrix:'), app.LINE, '']),
        symb_ptt=ar.par.Pattern.ATOM_SYMBOL + app.maybe(app.UNSIGNED_INTEGER),
        key_ptt=app.one_of_these([app.UNSIGNED_INTEGER, app.VARIABLE_NAME]),
        line_end_ptt=app.maybe(app.UNSIGNED_INTEGER),
        last=False)

    # Reads the values from the end of the output
    grad_val = app.one_of_these([app.FLOAT, 'nan', '-nan'])
    if len(syms) == 1:
        val_dct = {}
    else:
        val_dct = ar.zmatrix.setval.read(
            output_str,
            start_ptt=app.padded(app.NEWLINE).join([
                app.padded('Optimized Parameters', app.NONNEWLINE),
                app.LINE, app.LINE, app.LINE, app.LINE, '']),
            entry_sep_ptt='',
            entry_start_ptt=app.escape('!'),
            sep_ptt=app.maybe(app.LINESPACES).join([
                app.escape('-DE/DX ='), grad_val, app.escape('!'),
                app.NEWLINE]),
            last=True)

    # Check for the pattern
    err_ptt = app.LINESPACES.join([
        app.escape('-DE/DX ='), app.one_of_these(['nan', '-nan'])])
    if 'Optimized Parameters' in output_str:
        test_str = output_str.split('Optimized Parameters')[1]
        if apf.has_match(err_ptt, test_str):
            print('Warning: Bad gradient value (nan)',
                  'in "Optimized Parameters" list.')

    # For the case when variable names are used instead of integer keys:
    # (otherwise, does nothing)
    key_dct = dict(map(reversed, enumerate(syms)))
    key_dct[None] = 0
    key_mat = [[key_dct[val]+1 if not isinstance(val, numbers.Real) else val
                for val in row] for row in key_mat]
    sym_ptt = app.STRING_START + app.capturing(ar.par.Pattern.ATOM_SYMBOL)
    syms = [apf.first_capture(sym_ptt, sym) for sym in syms]

    # Call the automol constructor
    zma = automol.zmatrix.from_data(
        syms, key_mat, name_mat, val_dct,
        one_indexed=True, angstrom=True, degree=True)

    return zma
