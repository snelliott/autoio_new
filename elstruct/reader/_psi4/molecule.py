""" molecular geometry and structure readers
"""
import autoparse.pattern as app
import autoparse.find as apf
import automol


def opt_geometry(output_string):
    """ get optimized cartesian geometry from output
    """
    head_pattern = app.padded(app.escape('Final (previous) structure:'),
                              app.NONNEWLINE)
    pattern = app.NEWLINE.join([
        head_pattern, app.LINE,
        automol.readers.geom.block_pattern()
    ])
    geo_str = apf.last_capture(pattern, output_string)
    geo = automol.readers.geom.from_string(geo_str, strict=False)
    return geo


def opt_zmatrix(output_string):
    """ get optimized z-matrix geometry from output
    """
    head_pattern = app.rpadded(app.escape('Geometry (in Angstrom),'),
                               app.NONNEWLINE)
    pattern = app.NEWLINE.join([
        head_pattern, app.LINE,
        automol.readers.zmatrix.block_pattern()
    ])
    zma_str = apf.last_capture(app.capturing(pattern), output_string)
    zma = automol.readers.zmatrix.from_string(zma_str)
    return zma
