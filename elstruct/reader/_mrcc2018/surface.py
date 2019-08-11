""" gradient and hessian readers
"""
import numpy
import autoread as ar
import autoparse.pattern as app


def gradient(output_string):
    """ read gradient from the output string
    """
    grad = ar.matrix.read(
        output_string,
        start_ptt=(
            app.padded(app.escape('Cartesian gradient [au]:')) +
            app.NEWLINE),
        line_start_ptt=app.LINESPACES.join([
            app.UNSIGNED_INTEGER, app.one_or_more(app.LETTER)])
        )
    assert numpy.shape(grad)[1] == 3
    return grad
