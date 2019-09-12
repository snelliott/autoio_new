""" electronic energy readers
"""
import autoread as ar
from autoparse import cast as _cast
import autoparse.pattern as app
import autoparse.find as apf
import elstruct.par

PROG = elstruct.par.Program.GAUSSIAN09


def _hf_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.one_of_these([
            app.escape('E(RHF) ='),
            app.escape('E(UHF) ='),
            app.escape('E(ROHF) =')]))
    return ene


def _mp2_energy(output_string):
    ene_d_str = ar.energy.read(
        output_string,
        app.escape('EUMP2 = '),
        val_ptt=app.EXPONENTIAL_FLOAT_D)
    ene = _cast(apf.replace('d', 'e', ene_d_str, case=False))
    return ene


def _dft_energy(output_string):
    e_pattern = app.escape('E(') + app.VARIABLE_NAME + app.escape(')')
    ene = ar.energy.read(
        output_string,
        start_ptt=app.LINESPACES.join([
            'SCF Done:', e_pattern, '=']))
    return ene


# a dictionary of functions for reading the energy from the output, by method
ENERGY_READER_DCT = {
    elstruct.par.Method.HF[0]: _hf_energy,
    elstruct.par.Method.Corr.MP2[0]: _mp2_energy,
}

METHODS = elstruct.par.program_methods(PROG)
for METHOD in METHODS:
    if elstruct.par.Method.is_standard_dft(METHOD):
        ENERGY_READER_DCT[METHOD] = _dft_energy

assert all(method in ENERGY_READER_DCT for method in METHODS)


def energy(method, output_string):
    """ get total energy from output
    """

    # get the appropriate reader and call it
    if elstruct.par.Method.is_nonstandard_dft(method):
        energy_reader = _dft_energy
    else:
        energy_reader = ENERGY_READER_DCT[method]

    return energy_reader(output_string)
