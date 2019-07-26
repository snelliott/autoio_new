""" irc readers
"""

from qcelemental import periodictable as pt
import autoread as ar
import autoparse.pattern as app
import autoparse.find as apf
import automol
from .surface import gradient
from .surface import hessian


def get_irc(output_string):
    """ get a list of strings for each irc point
    """

    # Lines
    output_lines = output_string.splitlines()

    # Find the lines with point number to get the strings
    section_starts = []
    for i, line in enumerate(output_lines):
        if 'Point Number' in line:
            section_starts.append(i)

    # get list of each string
    pt_str = []
    for i in range(1, len(section_starts)):
        start = section_starts[i-1]
        end = section_starts[i]
        pt_str.append('\n'.join(output_lines[start+1:end]))

    # Obtain the grads and hessians
    geoms = []
    grads = []
    hess = []
    for string in pt_str:
        geoms.append(irc_geometry(string))
        grads.append(gradient(string))
        hess.append(hessian(string))

    return geoms, grads, hess


def irc_geometry(output_string):
    """ get geometry from at a point on the IRC
    """
    nums, xyzs = ar.geom.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.escape('Input orientation:'),
            app.LINE, app.LINE, app.LINE, app.LINE, '']),
        sym_ptt=app.UNSIGNED_INTEGER,
        line_start_ptt=app.UNSIGNED_INTEGER,
        line_sep_ptt=app.UNSIGNED_INTEGER,)
    syms = tuple(map(pt.to_E, nums))
    geo = automol.geom.from_data(syms, xyzs, angstrom=True)
    return geo
