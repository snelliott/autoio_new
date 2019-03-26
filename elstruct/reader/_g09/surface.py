""" gradient and hessian readers
"""
import numpy
import autoparse.pattern as app
import autoparse.find as apf

COORD_LABEL_PTT = app.one_of_these(['X', 'Y', 'Z']) + app.UNSIGNED_INTEGER
ARRAY_LINE_PTT = (
    app.LINE_START +
    app.padded(COORD_LABEL_PTT) +
    app.series(app.FLOAT, app.LINESPACES) +
    app.LINE_END
)
ARRAY_BLOCK_HEAD_PTT = (
    app.LINE_START +
    app.padded(app.series(COORD_LABEL_PTT, app.LINESPACES)) +
    app.LINE_END
)
ARRAY_BLOCK_BODY_PTT = app.series(ARRAY_LINE_PTT, app.NEWLINE)
ARRAY_BLOCK_PTT = (
    ARRAY_BLOCK_HEAD_PTT + app.NEWLINE + ARRAY_BLOCK_BODY_PTT
)
ARRAY_BLOCKS_PTT = app.series(ARRAY_BLOCK_PTT, app.NEWLINE)


def gradient(output_string):
    """ read gradient from the output string
    """
    head_ptt = app.padded(app.escape('Forces (Hartrees/Bohr)'), app.NONNEWLINE)
    line_ptt = app.LINE_START + app.padded(
        app.LINESPACES.join(2 * [app.UNSIGNED_INTEGER] + 3 * [app.FLOAT])
    ) + app.LINE_END
    grad_ptt = app.series(line_ptt, app.NEWLINE)
    block_ptt = app.NEWLINE.join(
        [head_ptt] + 2 * [app.LINE] + [grad_ptt])
    block_str = apf.last_capture(app.capturing(block_ptt), output_string)
    assert block_str is not None
    grad_str = apf.first_capture(app.capturing(grad_ptt), block_str)
    grad = tuple(tuple(map(float, line.split()[2:]))
                 for line in grad_str.splitlines())
    return grad


def hessian(output_string):
    """ read hessian from the output string
    """
    head_ptt = app.padded(app.escape('The second derivative matrix:'))
    array_ptt = head_ptt + app.NEWLINE + ARRAY_BLOCKS_PTT
    array_str = apf.last_capture(app.capturing(array_ptt), output_string)
    block_strs = apf.all_captures(app.capturing(ARRAY_BLOCK_BODY_PTT),
                                  array_str)
    tril_rows = _values_from_gaussian_tril_block(block_strs[0])
    ncoords = len(tril_rows)

    for block_str in block_strs[1:]:
        block_tril_rows = _values_from_gaussian_tril_block(block_str)
        nrows = len(block_tril_rows)
        for block_idx, row_idx in enumerate(range(nrows+1, ncoords)):
            tril_rows[row_idx] += block_tril_rows[block_idx]

    hess = numpy.zeros((ncoords, ncoords))

    for row_idx, tril_row in enumerate(tril_rows):
        hess[row_idx, :row_idx+1] = tril_row
        hess[:row_idx+1, row_idx] = tril_row

    # make sure we ended up with a square symmetric matrix
    assert hess.ndim == 2 and hess.shape[0] == hess.shape[1]
    assert numpy.allclose(hess, hess.T)

    return tuple(map(tuple, hess))


def _values_from_gaussian_tril_block(block_str):
    tril_rows = [list(map(float, block_line.split()[1:]))
                 for block_line in block_str.splitlines()]
    return tril_rows
