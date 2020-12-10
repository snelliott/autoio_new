""" property readers
"""

import numpy as np
from autoparse import pattern as app
from autoparse import find as apf


def dipole_moment(output_string):
    """
    Reads the dipole moment
    """
    pattern = (app.escape('Dipole moment (field-independent basis, Debye):') +
               app.NEWLINE +
               app.padded('X=') + app.capturing(app.FLOAT) +
               app.padded('Y=') + app.capturing(app.FLOAT) +
               app.padded('Z=') + app.capturing(app.FLOAT))
    captures = apf.last_capture(pattern, output_string)
    vals = captures if captures is not None else []
    if vals:
        vals = [float(val) for val in vals]
    else:
        vals = None

    return vals


def polarizability(output_string):
    """
    Reads the static polarizability
    """
    pattern = ('Exact polarizability:' +
               app.SPACES + app.capturing(app.FLOAT) +
               app.SPACES + app.capturing(app.FLOAT) +
               app.SPACES + app.capturing(app.FLOAT) +
               app.SPACES + app.capturing(app.FLOAT) +
               app.SPACES + app.capturing(app.FLOAT) +
               app.SPACES + app.capturing(app.FLOAT))
    captures = apf.last_capture(pattern, output_string)
    vals = captures if captures is not None else []
    if vals:
        vals = [float(val) for val in vals]
        tensor = np.array([[vals[0], vals[1], vals[3]],
                           [vals[1], vals[2], vals[4]],
                           [vals[3], vals[4], vals[5]]])
    else:
        tensor = None

    return tensor
