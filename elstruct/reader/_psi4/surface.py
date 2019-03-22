""" gradient and hessian readers
"""
import numpy
import autoparse.pattern as app
import autoparse.find as apf

ARRAY_LINE_PATTERN = (
    app.LINE_START + app.padded(app.UNSIGNED_INTEGER) +
    app.series(app.FLOAT, app.LINESPACES)
)
ARRAY_BLOCK_HEAD_PATTERN = (
    app.padded(app.NEWLINE) +
    app.series(app.UNSIGNED_INTEGER, app.LINESPACES) +
    app.padded(app.NEWLINE)
)
ARRAY_BLOCK_BODY_PATTERN = app.series(ARRAY_LINE_PATTERN, app.NEWLINE)
ARRAY_BLOCK_PATTERN = (
    ARRAY_BLOCK_HEAD_PATTERN + app.NEWLINE + ARRAY_BLOCK_BODY_PATTERN
)
ARRAY_BLOCKS_PATTERN = app.series(ARRAY_BLOCK_PATTERN, app.NEWLINE)


def gradient(output_string):
    """ get gradient from output
    """
    head_pattern = app.rpadded(app.escape('## Gradient'), app.NONNEWLINE)
    grad_pattern = app.NEWLINE.join([
        head_pattern,
        app.zero_or_more(app.NONNEWLINE),
        ARRAY_BLOCKS_PATTERN
    ])
    grad_str = apf.last_capture(app.capturing(grad_pattern), output_string)
    grad_str = apf.last_capture(app.capturing(ARRAY_BLOCK_BODY_PATTERN),
                                grad_str)
    grad = _array_from_block_string(grad_str)
    assert grad.ndim == 2 and grad.shape[1] == 3

    return tuple(map(tuple, grad))


def hessian(output_string):
    """ get hessian from output
    """
    head_pattern = app.rpadded(app.escape('## Hessian'), app.NONNEWLINE)
    hess_pattern = app.NEWLINE.join([
        head_pattern,
        app.zero_or_more(app.NONNEWLINE),
        ARRAY_BLOCKS_PATTERN
    ])
    hess_str = apf.last_capture(app.capturing(hess_pattern), output_string)
    hess_block_strs = apf.all_captures(app.capturing(ARRAY_BLOCK_BODY_PATTERN),
                                       hess_str)

    hess_blocks = []
    for hess_block_str in hess_block_strs:
        hess_block = _array_from_block_string(hess_block_str)
        hess_blocks.append(hess_block)

    hess = numpy.concatenate(hess_blocks, axis=1)

    # make sure we ended up with a square symmetric matrix
    assert hess.ndim == 2 and hess.shape[0] == hess.shape[1]
    assert numpy.allclose(hess, hess.T)

    return tuple(map(tuple, hess))


def _array_from_block_string(arr_str):
    return numpy.array([list(map(float, apf.split_words(arr_line)))[1:]
                        for arr_line in apf.split_lines(arr_str)])
