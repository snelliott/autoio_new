""" molecular geometry and structure readers
"""
from autoparse import cast as _cast
import autoparse.pattern as app
import autoparse.find as apf
import phycon.elements as pce
import automol


def opt_geometry(output_string):
    """ get optimized geometry from output
    """
    geom_line_ptt_ = _geometry_line_pattern(
        num_ptt=app.capturing(app.UNSIGNED_INTEGER),
        val_ptt=app.capturing(app.FLOAT))
    geom_line_ptt = _geometry_line_pattern(
        num_ptt=app.UNSIGNED_INTEGER,
        val_ptt=app.FLOAT)
    geom_ptt = app.series(geom_line_ptt, app.padded(app.NEWLINE))

    block_ptt_ = app.padded(app.NEWLINE).join([
        app.escape("Standard orientation:"),
        app.LINE, app.LINE, app.LINE, app.LINE,
        app.capturing(geom_ptt),
    ])
    geo_str = apf.last_capture(block_ptt_, output_string)

    mcaps = apf.all_captures(geom_line_ptt_, geo_str)
    nums, xcomps, ycomps, zcomps = zip(*_cast(mcaps))
    syms = tuple(map(pce.symbol, nums))
    xyzs = tuple(zip(xcomps, ycomps, zcomps))
    geo = automol.constructors.geom.from_data(syms, xyzs, angstrom=True)
    return geo


def opt_zmatrix(output_string):
    """ get optimized z-matrix geometry from output
    """
    # read the matrix from the beginning of the output
    mat_block_ptt_ = app.padded(app.NEWLINE).join([
        app.escape('Symbolic Z-matrix:'),
        app.LINE,
        app.capturing(automol.readers.zmatrix.matrix_block_pattern()),
    ])
    mat_str = apf.first_capture(mat_block_ptt_, output_string)
    syms, key_mat, name_mat = (
        automol.readers.zmatrix.matrix_block_information(mat_str))

    # read the values from the end of the output
    setv_term_ptt = _setval_term_pattern(
        name_ptt=app.VARIABLE_NAME,
        val_ptt=app.FLOAT)
    setv_term_ptt_ = _setval_term_pattern(
        name_ptt=app.capturing(app.VARIABLE_NAME),
        val_ptt=app.capturing(app.FLOAT))
    setv_block_ptt = app.series(setv_term_ptt, app.padded(app.NEWLINE))
    setv_block_ptt_ = app.padded(app.NEWLINE).join([
        app.escape('!   Optimized Parameters   !'),
        app.escape('! (Angstroms and Degrees)  !'),
        app.LINE, app.LINE, app.LINE, app.capturing(setv_block_ptt)])
    setv_str = apf.last_capture(setv_block_ptt_, output_string)
    caps = apf.all_captures(setv_term_ptt_, setv_str)
    val_dct = dict(_cast(caps))

    # call the automol constructor
    zma = automol.constructors.zmatrix.from_data(
        syms, key_mat, name_mat, val_dct,
        one_indexed=True, angstrom=True, degree=True)
    return zma


def _geometry_line_pattern(num_ptt, val_ptt):
    return app.LINESPACES.join([
        app.UNSIGNED_INTEGER, num_ptt, app.UNSIGNED_INTEGER,
        val_ptt, val_ptt, val_ptt])


def _setval_term_pattern(name_ptt, val_ptt):
    return app.LINESPACES.join([
        app.escape('!'), name_ptt, val_ptt, app.escape('-DE/DX ='), app.FLOAT,
        app.escape('!')])
