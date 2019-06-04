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
            app.escape('ATOMIC COORDINATES'),
            app.LINE, app.LINE, app.LINE, '']),
        line_start_ptt=app.UNSIGNED_INTEGER,
        line_sep_ptt=app.FLOAT,)
    geo = automol.geom.from_data(syms, xyzs, angstrom=True)
    return geo
