""" electronic energy readers
"""
import autoparse.pattern as app
import autoparse.find as apf
import autoparse.conv as apc
from elstruct import par


def _hf_energy(orb_restricted, output_string):
    assert isinstance(orb_restricted, bool)
    if orb_restricted:
        pattern = app.LINESPACES.join([
            app.one_of_these([
                app.escape('@RHF Final Energy:'),
                app.escape('@ROHF Final Energy:'),
            ]),
            app.capturing(app.FLOAT)
        ])
    else:
        pattern = app.LINESPACES.join([
            app.escape('@UHF Final Energy:'),
            app.capturing(app.FLOAT)
        ])
    cap = apf.last_capture(pattern, output_string)
    val = apc.single(cap, func=float)
    return val


def _dft_energy(orb_restricted, output_string):
    assert isinstance(orb_restricted, bool)
    if orb_restricted:
        pattern = app.LINESPACES.join([
            app.escape('@RKS Final Energy:'),
            app.capturing(app.FLOAT)
        ])
    else:
        pattern = app.LINESPACES.join([
            app.escape('@UKS Final Energy:'),
            app.capturing(app.FLOAT)
        ])
    cap = apf.last_capture(pattern, output_string)
    val = apc.single(cap, func=float)
    return val


def _mp2_energy(orb_restricted, output_string):
    assert isinstance(orb_restricted, bool)
    pattern = app.LINESPACES.join([
        app.escape('MP2 Total Energy (a.u.)'),
        app.escape(':'),
        app.capturing(app.FLOAT)
    ])
    cap = apf.last_capture(pattern, output_string)
    val = apc.single(cap, func=float)
    return val


# a dictionary of functions for reading the energy from the output, by method
ENERGY_READER_DCT = {
    par.Method.HF: _hf_energy,
    par.Method.Dft.B3LYP: _dft_energy,
    par.Method.Corr.MP2: _mp2_energy,
}


def method_list():
    """ list of available electronic structure methods
    """
    return tuple(sorted(ENERGY_READER_DCT.keys()))


def energy(method, orb_restricted, output_string):
    """ get total energy from output
    """
    assert method in method_list()
    # get the appropriate reader and call it
    energy_reader = ENERGY_READER_DCT[method]
    return energy_reader(orb_restricted, output_string)
