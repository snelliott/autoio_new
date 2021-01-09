""" gradient and hessian readers
"""

import autoread as ar
import autoparse.pattern as app


def gradient(output_str):
    """ Reads the molecular gradient (in Cartesian coordinates) from
        the output file string. Returns the gradient in atomic units.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: tuple(tuple(float))
    """

    head_ptt = ('Atom' + app.SPACES +
                app.escape('dE/dx') + app.SPACES +
                app.escape('dE/dy') + app.SPACES +
                app.escape('dE/dz'))
    grad = ar.matrix.read(
        output_str,
        start_ptt=app.padded(app.NEWLINE).join([
            app.padded(head_ptt, app.NONNEWLINE),
            app.LINE, '']),
        line_start_ptt=app.UNSIGNED_INTEGER)

    return grad


def hessian(output_str):
    """ Reads the molecular Hessian (in Cartesian coordinates) from
        the output file string. Returns the Hessian in atomic units.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: tuple(tuple(float))
    """

    comp_ptt = (
        app.one_or_more(app.LETTER) +
        app.one_of_these(['X', 'Y', 'Z']) +
        app.UNSIGNED_INTEGER
    )
    mat = ar.matrix.read(
        output_str,
        start_ptt=(
            app.escape('Force Constants (Second Derivatives of the Energy) ') +
            app.escape('in [a.u.]') +
            app.lpadded(app.NEWLINE)),
        block_start_ptt=(app.series(comp_ptt, app.LINESPACES) +
                         app.padded(app.NEWLINE)),
        line_start_ptt=comp_ptt,
        tril=True)

    if mat is not None:
        mat = tuple(map(tuple, mat))

    return mat
