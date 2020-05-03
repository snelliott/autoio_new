""" property readers
"""

from autoparse import pattern as app
from autoparse import find as apf


def dipole_moment(output_string):
    """
    Reads the dipole moment
    """
    pattern = app.LINESPACES.join([
        'Total Dipole Moment',
        ':',
        app.capturing(app.FLOAT),
        app.capturing(app.FLOAT),
        app.capturing(app.FLOAT)])
    captures = apf.last_capture(pattern, output_string)
    vals = captures if captures is not None else []
    if vals:
        vals = [float(val) for val in vals]
    else:
        vals = None
    return vals
#
#
# def polarizability(output_string):
#     """
#     Reads the static polarizability
#     """
#     tensor = ar.matrix.read(
#         output_string,
#         start_ptt=app.padded(
#                 'The raw cartesian tensor (atomic units)') +
#                 app.NEWLINE)
#     return tensor
