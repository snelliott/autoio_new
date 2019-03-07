""" hessian readers
"""
import numpy
import autoparse.pattern as app
import autoparse.find as apf

ARRAY_BLOCK_HEAD_PATTERN = (
    app.PADDED_NEWLINE +
    app.series(app.UNSIGNED_INTEGER, app.LINESPACES) +
    app.PADDED_NEWLINE
)
ARRAY_LINE_PATTERN = (
    app.PADDED_LINE_START + app.UNSIGNED_INTEGER + app.LINESPACES +
    app.series(app.FLOAT, app.LINESPACES)
)
ARRAY_BLOCK_PATTERN = app.series(ARRAY_LINE_PATTERN, app.PADDED_NEWLINE)


def gradient(output_string):
    """ get gradient from output
    """
    start_pattern = app.one_of_these([
        app.escape('Total Gradient:'),
        app.escape('## F-D gradient'),
        app.escape('## Gradient')])
    end_pattern = app.escape('***')
    block_capturing_pattern = app.capturing(ARRAY_BLOCK_PATTERN)

    wide_block_str = apf.last_block(start_pattern, end_pattern, output_string,
                                    case=False)
    grad_str = apf.first_capture(block_capturing_pattern, wide_block_str)
    grad = _array_from_psi4_array_string(grad_str)
    assert grad.ndim == 2 and grad.shape[1] == 3

    return tuple(map(tuple, grad))


def hessian(output_string):
    """ get hessian from output
    """
    start_pattern = app.one_of_these([
        app.escape('## Total Hessian'),
        app.escape('## Hessian')])
    end_pattern = app.escape('***')
    block_capturing_pattern = (ARRAY_BLOCK_HEAD_PATTERN + app.PADDED_NEWLINE +
                               app.capturing(ARRAY_BLOCK_PATTERN))

    wide_block_str = apf.last_block(start_pattern, end_pattern, output_string,
                                    case=False)
    hess_block_strs = apf.all_captures(block_capturing_pattern, wide_block_str)

    hess_blocks = []
    for hess_block_str in hess_block_strs:
        hess_block = _array_from_psi4_array_string(hess_block_str)
        hess_blocks.append(hess_block)

    hess = numpy.concatenate(hess_blocks, axis=1)

    assert hess.ndim == 2 and hess.shape[0] == hess.shape[1]

    return tuple(map(tuple, hess))


def _array_from_psi4_array_string(arr_str):
    return numpy.array([list(map(float, apf.split_words(arr_line)))[1:]
                        for arr_line in apf.split_lines(arr_str)])
