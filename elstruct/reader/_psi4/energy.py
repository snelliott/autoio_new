""" electronic energy readers
"""
import autoparse.pattern as app
import autoparse.find as apf
import autoparse.conv as apc
from ... import params as par


def _rhf_energy(output_string):
    pattern = app.LINESPACES.join([
        app.escape('@RHF Final Energy:'),
        app.capturing(app.FLOAT)
    ])
    cap = apf.last_capture(pattern, output_string)
    val = apc.single(cap, dtype=float)
    return val


def _uhf_energy(output_string):
    pattern = app.LINESPACES.join([
        app.escape('@UHF Final Energy:'),
        app.capturing(app.FLOAT)
    ])
    cap = apf.last_capture(pattern, output_string)
    val = apc.single(cap, dtype=float)
    return val


def _rohf_energy(output_string):
    pattern = app.LINESPACES.join([
        app.escape('@ROHF Final Energy:'),
        app.capturing(app.FLOAT)
    ])
    cap = apf.last_capture(pattern, output_string)
    val = apc.single(cap, dtype=float)
    return val


def _mp2_energy(output_string):
    pattern = app.LINESPACES.join([
        app.escape('MP2 Total Energy (a.u.)'),
        app.escape(':'),
        app.capturing(app.FLOAT)
    ])
    cap = apf.last_capture(pattern, output_string)
    val = apc.single(cap, dtype=float)
    return val


# a dictionary of functions for reading the energy from the output, by method
ENERGY_FINDERS = {
    par.METHOD.RHF: _rhf_energy,
    par.METHOD.UHF: _uhf_energy,
    par.METHOD.ROHF: _rohf_energy,
    par.METHOD.RHF_MP2: _mp2_energy,
    par.METHOD.UHF_MP2: _mp2_energy,
    par.METHOD.ROHF_MP2: _mp2_energy,
}


def method_list():
    """ list of available electronic structure methods
    """
    return tuple(sorted(ENERGY_FINDERS.keys()))


def energy(method, output_string):
    """ get total energy from output
    """
    assert method in method_list()
    # get the appropriate finder and call it
    energy_finder = ENERGY_FINDERS[method]
    return energy_finder(output_string)
