""" gradient and hessian readers
"""
import numpy
from qcelemental import periodictable as pt
import automol
import autoread as ar
from autoparse import cast as _cast
import autoparse.pattern as app
import autoparse.find as apf


def gradient(output_string):
    """ read gradient from the output string
    """
    grad = ar.matrix.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.padded(app.escape('Forces (Hartrees/Bohr)'), app.NONNEWLINE),
            app.LINE, app.LINE, '']),
        line_start_ptt=app.LINESPACES.join([app.UNSIGNED_INTEGER] * 2))
    grad = numpy.multiply(grad, -1.0)
    assert numpy.shape(grad)[1] == 3
    return grad


def hessian(output_string):
    """ read hessian from the output string
    """
    try:
        comp_ptt = app.one_of_these(['X', 'Y', 'Z']) + app.UNSIGNED_INTEGER
        mat = ar.matrix.read(
            output_string,
            start_ptt=(app.escape('The second derivative matrix:') +
                       app.lpadded(app.NEWLINE)),
            block_start_ptt=(app.series(comp_ptt, app.LINESPACES) +
                             app.padded(app.NEWLINE)),
            line_start_ptt=comp_ptt,
            tril=True)
    except TypeError:
        comp_ptt = app.UNSIGNED_INTEGER
        mat = ar.matrix.read(
            output_string,
            val_ptt=app.EXPONENTIAL_FLOAT_D,
            start_ptt=(
                app.escape('Force constants in Cartesian coordinates:') +
                app.lpadded(app.NEWLINE)),
            block_start_ptt=(app.series(comp_ptt, app.LINESPACES) +
                             app.padded(app.NEWLINE)),
            line_start_ptt=comp_ptt,
            tril=True)

        mat = [[_cast(apf.replace('d', 'e', dst, case=False)) for dst in row]
               for row in mat]

    mat = tuple(map(tuple, mat))
    return mat


def harmonic_frequencies(output_string):
    """ read harmonic frequencies from the output string
    """
    pattern = 'Frequencies --' + app.capturing(app.LINE_FILL)
    captures = apf.all_captures(pattern, output_string)
    if captures is not None:
        freqs = []
        for capture in captures:
            vals = capture.split()
            for val in vals:
                freqs.append(float(val))
    else:
        freqs = None
    return freqs


def irc_points(output_string):
    """ obtain the geometry, gradient, and hessian at each point along the irc
    """

    # Lines
    output_lines = output_string.splitlines()

    # Obtain all of the info for the points off the saddle point
    # Find the lines with point number to get the strings
    section_starts = []
    for i, line in enumerate(output_lines):
        if 'Point Number  1 in' in line:
            section_starts.append(i)
            break
    for i, line in enumerate(output_lines):
        if 'OF POINTS ALONG THE PATH' in line:
            section_starts.append(i)

    # Get the TS info first
    sadpt_str = '\n'.join(output_lines[0:section_starts[0]])
    sadpt_geom = sadpt_geometry(sadpt_str)
    sadpt_grad = gradient(sadpt_str)
    sadpt_hess = hessian(sadpt_str)

    # Now start getting other points by getting a list of each string with point info
    pt_strs = []
    for i in range(1, len(section_starts)):
        start_line = section_starts[i-1]
        end_line = section_starts[i]
        pt_strs.append('\n'.join(output_lines[start_line+1:end_line]))

    # Obtain the grads and hessians
    geoms = []
    grads = []
    hessians = []
    for string in pt_strs:
        geoms.append(irc_geometry(string))
        grads.append(gradient(string))
        hessians.append(hessian(string))

    # Combine with the 0 index info
    geoms = [sadpt_geom] + geoms
    grads = [sadpt_grad] + grads
    hessians = [sadpt_hess] + hessians

    return geoms, grads, hessians


def sadpt_geometry(sadpt_string):
    """ get the geometry of the saddle point of IRC
    """
    nums, xyzs = ar.geom.read(
        sadpt_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('Input orientation:'),
            app.LINE, app.LINE, app.LINE, app.LINE, '']),
        sym_ptt=app.UNSIGNED_INTEGER,
        line_start_ptt=app.UNSIGNED_INTEGER,
        line_sep_ptt=app.UNSIGNED_INTEGER)
    syms = tuple(map(pt.to_E, nums))
    geo = automol.geom.from_data(syms, xyzs, angstrom=True)
    return geo


def irc_geometry(output_string):
    """ get geometry at a point on the IRC
    """
    nums, xyzs = ar.geom.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('CURRENT STRUCTURE'),
            app.LINE, app.LINE, app.LINE, app.LINE, app.LINE, '']),
        sym_ptt=app.UNSIGNED_INTEGER,
        line_start_ptt=app.UNSIGNED_INTEGER)
    syms = tuple(map(pt.to_E, nums))
    geo = automol.geom.from_data(syms, xyzs, angstrom=True)
    return geo


def irc_energies(output_string):
    """ get the energies relative to the saddle point
    """
    # Read the reference energy (the ts/sadpt)
    ptt = (
        'Energies reported relative to the TS energy of' +
        app.SPACES +
        app.capturing(app.FLOAT)
    )
    ts_energy = apf.last_capture(ptt, output_string)
    pt_energies = _read_irc_reacion_path_summary(output_string, 'energy')
    if ts_energy and pt_energies:
        energies = [float(ts_energy) + ene for ene in pt_energies]

    # See if the enes need to be flipped so the ts ene is first
    if pt_energies[0] != 0.0:
        energies = energies[::-1]
    return energies


def irc_coordinates(output_string):
    """ get the coordinates relative to the saddle point
    """
    coordinates = _read_irc_reacion_path_summary(output_string, 'coord')
    return coordinates


def _read_irc_reacion_path_summary(output_string, read_val):
    """ get the desired values from the reaction path summary block
    """
    assert read_val in ('energy', 'coord')

    block = apf.last_capture(
        (app.escape('Summary of reaction path following') +
         app.capturing(app.one_or_more(app.WILDCARD, greedy=False)) +
         app.escape('Total number of points:') + app.SPACES + app.INTEGER),
        output_string)

    if read_val == 'energy':
        pattern = (
            app.INTEGER + app.SPACES +
            app.capturing(app.FLOAT) +
            app.SPACES +
            app.FLOAT
        )
    elif read_val == 'coord':
        pattern = (
            app.INTEGER + app.SPACES +
            app.FLOAT +
            app.SPACES +
            app.capturing(app.FLOAT)
        )

    captures = apf.all_captures(pattern, block)
    if captures is not None:
        values = [float(capture) for capture in captures]
    else:
        values = None

    return values


if __name__ == '__main__':
    with open('run.out', 'r') as f:
        RF = f.read()
    print(harmonic_frequencies(RF))

