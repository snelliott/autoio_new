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
        start_ptt=app.padded(app.NEWLINE).join([
            app.padded(app.escape('ENERGY GRADIENTS'), app.NONNEWLINE),
            app.LINE, app.LINE, app.LINE, '']),
        line_start_ptt=app.LINESPACES.join([
            app.UNSIGNED_INTEGER,
            app.one_or_more(app.LETTER),
            app.FLOAT,
            app.FLOAT,
            app.FLOAT])
        )
    assert numpy.shape(grad)[1] == 3
    return grad
# def hessian(output_string):
#     """ read hessian from the output string
#     """
#
#     comp_ptt = app.UNSIGNED_INTEGER
#     mat = ar.matrix.read(
#         output_string,
#         start_ptt=app.padded(app.NEWLINE).join([
#             app.padded(app.escape(
#                 'MASS-WEIGHTED PROJECTED HESSIAN (Hartree/Bohr/Bohr/Kamu)'),
#                 app.NONNEWLINE),
#             app.LINE, app.LINE, app.LINE, '']),
#         block_start_ptt=(
#            app.series(comp_ptt, app.LINESPACES) +
#                       app.padded(app.NEWLINE) +
#            app.padded('----- ----- ----- ----- -----', app.LINESPACES) +
#                       app.padded(app.NEWLINE)),
#         line_start_ptt=comp_ptt,
#         val_ptt=app.EXPONENTIAL_FLOAT_D,
#         tril=True)
#
#     mat = [[_cast(apf.replace('d', 'e', dst, case=False)) for dst in row]
#             for row in mat]
#
#     mat = tuple(map(tuple, mat))
#     return mat
