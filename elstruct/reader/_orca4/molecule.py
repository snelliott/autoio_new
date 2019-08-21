""" molecular geometry and structure readers
"""

import autoread as ar
import autoparse.pattern as app
import automol


def opt_geometry(output_string):
    """ get optimized geometry from output
    """
    syms, xyzs = ar.geom.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.padded(
                app.escape('CARTESIAN COORDINATES (ANGSTROEM)'),
                app.NONNEWLINE),
            app.LINE, '']))
    geo = automol.geom.from_data(syms, xyzs, angstrom=True)
    return geo
