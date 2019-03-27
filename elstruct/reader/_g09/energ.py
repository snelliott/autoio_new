""" electronic energy readers
"""
from autoparse import cast as _cast
import autoparse.pattern as app
import autoparse.find as apf
import elstruct.par


def _hf_energy(output_string):
    pattern = app.LINESPACES.join([
        app.one_of_these([
            app.escape('E(RHF)'),
            app.escape('E(UHF)'),
            app.escape('E(ROHF)'),
        ]),
        app.escape('='),
        app.capturing(app.FLOAT)
    ])
    cap = apf.last_capture(pattern, output_string, case=False)
    val = _cast(cap)
    return val


def _mp2_energy(output_string):
    pattern = app.LINESPACES.join([
        app.escape('EUMP2'),
        app.escape('='),
        app.capturing(app.EXPONENTIAL_FLOAT_D),
    ])
    cap = apf.last_capture(pattern, output_string, case=False)
    cap = apf.replace('d', 'e', cap, case=False)
    val = _cast(cap)
    return val


def _dft_energy_(func_name):

    def _dft_energy(output_string):
        pattern = app.LINESPACES.join([
            app.one_of_these([
                app.escape('E(R{})'.format(func_name)),
                app.escape('E(U{})'.format(func_name)),
            ]),
            app.escape('='),
            app.capturing(app.FLOAT)
        ])
        cap = apf.last_capture(pattern, output_string, case=False)
        val = _cast(cap)
        return val

    return _dft_energy


# a dictionary of functions for reading the energy from the output, by method
ENERGY_READER_DCT = {
    elstruct.par.Method.HF: _hf_energy,
    elstruct.par.Method.Dft.B3LYP: _dft_energy_('b3lyp'),
    elstruct.par.Method.Corr.MP2: _mp2_energy,
}


def method_list():
    """ list of available electronic structure methods
    """
    return tuple(sorted(ENERGY_READER_DCT.keys()))


def energy(method, output_string):
    """ get total energy from output
    """
    method = method.lower()
    assert method in method_list()
    # get the appropriate reader and call it
    energy_reader = ENERGY_READER_DCT[method]
    return energy_reader(output_string)
