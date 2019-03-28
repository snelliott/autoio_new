""" gradient and hessian readers
"""
import numpy
import autoparser as apr
import autoparse.pattern as app


def gradient(output_string):
    """ get gradient from output
    """
    comp_ptt = app.UNSIGNED_INTEGER
    grad = apr.matrix.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('## Gradient (Symmetry 0) ##'),
            app.LINE, '', app.LINE, '', '']),
        line_start_ptt=comp_ptt)
    assert numpy.shape(grad)[1] == 3
    return grad


def hessian(output_string):
    """ get hessian from output
    """
    comp_ptt = app.UNSIGNED_INTEGER
    hess = apr.matrix.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('## Hessian (Symmetry 0) ##'), app.LINE, '']),
        block_start_ptt=app.padded(app.NEWLINE).join([
            '', app.series(comp_ptt, app.LINESPACES), '', '']),
        line_start_ptt=comp_ptt)
    assert numpy.allclose(hess, numpy.transpose(hess))
    return hess
