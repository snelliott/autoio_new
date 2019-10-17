""" gradient and hessian readers
"""
import numpy
from qcelemental import periodictable as pt
import automol
import autoread as ar
from autoparse import cast as _cast
import autoparse.pattern as app
import autoparse.find as apf


# def gradient(output_string):
#     """ read gradient from the output string
#     """
#     grad = ar.matrix.read(
#         output_string,
#         start_ptt=app.padded(app.NEWLINE).join([
#             app.padded(app.escape('Forces (Hartrees/Bohr)'), app.NONNEWLINE),
#             app.LINE, app.LINE, '']),
#         line_start_ptt=app.LINESPACES.join([app.UNSIGNED_INTEGER] * 2))
#     grad = numpy.multiply(grad, -1.0)
#     assert numpy.shape(grad)[1] == 3
#     return grad


def hessian(output_string):
    """ read hessian from the output string
    """
    comp_ptt = (
        app.one_or_more(app.LETTER) +
        app.one_of_these(['X', 'Y', 'Z']) +
        app.UNSIGNED_INTEGER
    )
    mat = ar.matrix.read(
        output_string,
        start_ptt=(app.escape('Mass weighted Second Derivative Matrix') +
                   app.lpadded(app.NEWLINE)),
        block_start_ptt=(app.series(comp_ptt, app.LINESPACES) +
                         app.padded(app.NEWLINE)),
        line_start_ptt=comp_ptt,
        tril=True)

    mat = tuple(map(tuple, mat))
    return mat


if __name__ == '__main__':
    with open('output.dat', 'r') as f:
        OUTPUT_STRING = f.read()
    # print(gradient(OUTPUT_STRING))
    print(hessian(OUTPUT_STRING))
