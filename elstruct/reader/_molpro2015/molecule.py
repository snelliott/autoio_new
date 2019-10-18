""" molecular geometry and structure readers
"""
import numpy
import autoread as ar
import autoparse.pattern as app
import automol


def opt_geometry(output_string):
    """ get optimized geometry from output
    """
    syms, xyzs = ar.geom.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('ATOMIC COORDINATES'),
            app.LINE, app.LINE, app.LINE, '']),
        line_start_ptt=app.UNSIGNED_INTEGER,
        line_sep_ptt=app.FLOAT,)
    geo = automol.geom.from_data(syms, xyzs, angstrom=False)
    return geo


def opt_zmatrix(output_string):
    """ get optimized z-matrix geometry from output
    """
    # read the matrix from the beginning of the output
    syms, key_mat, name_mat = ar.zmatrix.matrix.read(
        output_string,
        start_ptt=app.maybe(app.SPACES).join([
            'geometry', app.escape('='), app.escape('{'), '']),
        entry_start_ptt=app.maybe(','),
        entry_sep_ptt=',',
        last=False,
        case=False)

    # read the initial z-matrix values from the beginning out the output
    if len(syms) == 1:
        val_dct = {}
    else:
        val_dct = ar.zmatrix.setval.read(
            output_string,
            entry_start_ptt='SETTING',
            val_ptt=app.one_of_these([app.EXPONENTIAL_FLOAT_D, app.NUMBER]),
            last=False,
            case=False)

    names = sorted(set(numpy.ravel(name_mat)) - {None})
    caps_names = list(map(str.upper, names))
    name_dct = dict(zip(caps_names, names))
    assert set(caps_names) <= set(val_dct)
    val_dct = {name_dct[caps_name]: val_dct[caps_name]
               for caps_name in caps_names}

    # read optimized z-matrix values from the end of the output
    opt_val_dct = ar.zmatrix.setval.read(
        output_string,
        start_ptt=app.padded('Optimized variables') + app.NEWLINE,
        entry_end_ptt=app.one_of_these(['ANGSTROM', 'DEGREE']),
        last=True,
        case=False)
    opt_val_dct = {name_dct[caps_name]: opt_val_dct[caps_name]
                   for caps_name in opt_val_dct.keys()}
    assert set(opt_val_dct) <= set(val_dct)
    val_dct.update(opt_val_dct)

    # call the automol constructor
    zma = automol.zmatrix.from_data(
        syms, key_mat, name_mat, val_dct,
        one_indexed=True, angstrom=True, degree=True)
    return zma
