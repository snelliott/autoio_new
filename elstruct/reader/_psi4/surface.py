""" gradient and hessian readers
"""

import numpy
import automol
import autoread as ar
import autoparse.pattern as app
import autoparse.find as apf


def gradient(output_string):
    """ get gradient from output
    """
    comp_ptt = app.UNSIGNED_INTEGER
    grad = ar.matrix.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('## Gradient (Symmetry 0) ##'),
            app.LINE, '', app.LINE, '', '']),
        line_start_ptt=comp_ptt)
    assert numpy.shape(grad)[1] == 3
    return grad


def hessian(output_string):
    """ get hessian from output
    """
    comp_ptt = app.UNSIGNED_INTEGER
    hess = ar.matrix.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('## Hessian (Symmetry 0) ##'), app.LINE, '']),
        block_start_ptt=app.padded(app.NEWLINE).join([
            '', app.series(comp_ptt, app.LINESPACES), '', '']),
        line_start_ptt=comp_ptt)
    assert numpy.allclose(hess, numpy.transpose(hess))
    return hess


def irc_points(output_string):
    """ obtain the geometry, gradient, and hessian at each point along the irc
    """

    # Set pattern to find the end of each IRC optimization
    pattern = app.escape(
        '@IRC  **** Point ' +
        app.INTEGER +
        ' on IRC path is optimized ****'
    )
    block = apf.last_capture(
        (pattern +
         app.capturing(app.one_or_more(app.WILDCARD, greedy=False)) +
         app.escape('    Back-transformation to cartesian coordinates...')),
        output_string)

    # Set pattern for grabbing the geometry from the block
    geo_head_ptt = (
        app.escape('@IRC    Cartesian Geometry (in Angstrom)') +
        app.LINE_FILL +
        '\n'
    )

    # Grab all of the optimized geometries
    captures = apf.all_captures(pattern, block)
    if captures is not None:
        geoms = []
        for string in captures:
            syms, xyzs = ar.geom.read(
                string,
                start_ptt=geo_head_ptt,
                line_start_ptt=app.escape('@IRC')
            )
            geoms.append(automol.geom.from_data(syms, xyzs, angstrom=True))
    else:
        geoms = []

    # Set the gradients and hessians to empty lists since they MAY not be run
    grads, hessians = [], []

    return geoms, grads, hessians


def irc_path(output_string):
    """ get the coordinates and energies relative to the saddle point
    """

    # coordinates 
    block = apf.last_capture(
        (app.escape('@IRC              ****     IRC Steps     ****') +
         app.capturing(app.one_or_more(app.WILDCARD, greedy=False)) +
         app.escape('---Fragment 1 Intrafragment Coordinates---')),
        output_string)

    pattern = (
        app.escape('@IRC') + app.SPACES + app.INTEGER + app.SPACES +
        app.FLOAT + app.SPACES +
        app.capturing(app.FLOAT) + app.SPACES +
        app.FLOAT + app.SPACES +
        app.LINE_FILL
    )

    captures = apf.all_captures(pattern, block)
    if captures is not None:
        # Remove duplicates that may appear because of Psi4 output printing
        unique_coords = []
        for coord in captures:
            if coord not in unique_coords:
                unique_coords.append(coord)
        coords = [float(coord) for coord in unique_coords]
    else:
        coords = None

    # energies
    block = apf.last_capture(
        (app.escape('@IRC            ****      IRC Report      ****') +
         app.capturing(app.one_or_more(app.WILDCARD, greedy=False)) +
         app.escape('@IRC              ****     IRC Steps     ****')),
        output_string)

    pattern = (
        app.escape('@IRC') + app.SPACES + app.INTEGER + app.SPACES +
        app.capturing(app.FLOAT) + app.SPACES +
        app.FLOAT
    )

    captures = apf.all_captures(pattern, block)
    if captures is not None:
        energies = [float(capture) for capture in captures]
    else:
        energies = None

    return (coords, energies)
