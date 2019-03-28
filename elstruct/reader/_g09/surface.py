""" gradient and hessian readers
"""
import numpy
import autoparser as apr
import autoparse.pattern as app


def gradient(output_string):
    """ read gradient from the output string
    """
    grad = apr.matrix.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.padded(app.escape('Forces (Hartrees/Bohr)'), app.NONNEWLINE),
            app.LINE, app.LINE, '']),
        line_start_ptt=app.LINESPACES.join([app.UNSIGNED_INTEGER] * 2))
    assert numpy.shape(grad)[1] == 3
    return grad


def hessian(output_string):
    """ read hessian from the output string
    """
    comp_ptt = app.one_of_these(['X', 'Y', 'Z']) + app.UNSIGNED_INTEGER
    mat = apr.matrix.read(
        output_string,
        start_ptt=(app.escape('The second derivative matrix:') +
                   app.lpadded(app.NEWLINE)),
        block_start_ptt=(app.series(comp_ptt, app.LINESPACES) +
                         app.padded(app.NEWLINE)),
        line_start_ptt=comp_ptt,
        tril=True)
    return mat
