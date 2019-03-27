""" electronic energy readers
"""
from autoparse import cast as _cast
import autoparse.pattern as app
import autoparse.find as apf
import elstruct.par


def _hf_energy(output_string):
    pattern = app.LINESPACES.join([
        app.one_of_these([
            app.escape('@RHF Final Energy:'),
            app.escape('@ROHF Final Energy:'),
            app.escape('@UHF Final Energy:'),
        ]),
        app.capturing(app.FLOAT)
    ])
    cap = apf.last_capture(pattern, output_string, case=False)
    val = _cast(cap)
    return val


def _dft_energy(output_string):
    pattern = app.LINESPACES.join([
        app.one_of_these([
            app.escape('@RKS Final Energy:'),
            app.escape('@UKS Final Energy:'),
        ]),
        app.capturing(app.FLOAT)
    ])
    cap = apf.last_capture(pattern, output_string, case=False)
    val = _cast(cap)
    return val


def _mp2_energy(output_string):
    pattern = app.LINESPACES.join([
        app.escape('MP2 Total Energy (a.u.)'),
        app.escape(':'),
        app.capturing(app.FLOAT)
    ])
    cap = apf.last_capture(pattern, output_string, case=False)
    val = _cast(cap)
    return val


# a dictionary of functions for reading the energy from the output, by method
ENERGY_READER_DCT = {
    elstruct.par.Method.HF: _hf_energy,
    elstruct.par.Method.Dft.B3LYP: _dft_energy,
    elstruct.par.Method.Corr.MP2: _mp2_energy,
}


def method_list():
    """ list of available electronic structure methods
    """
    return tuple(sorted(ENERGY_READER_DCT.keys()))


def energy(method, output_string):
    """ get total energy from output
    """
    assert method in method_list()
    # get the appropriate reader and call it
    energy_reader = ENERGY_READER_DCT[method]
    return energy_reader(output_string)
