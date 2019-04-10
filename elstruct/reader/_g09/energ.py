""" electronic energy readers
"""
import autoread as ar
from autoparse import cast as _cast
import autoparse.pattern as app
import autoparse.find as apf
import elstruct.par

PROG = elstruct.par.Program.G09


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


def _dft_energy_(func_name):

    def _dft_energy(output_string):
        ene = ar.energy.read(
            output_string,
            app.one_of_these([
                app.escape('E(R{}) ='.format(func_name)),
                app.escape('E(U{}) ='.format(func_name))]),
            case=False)  # this is the default, but as a reminder
        return ene

    return _dft_energy


# a dictionary of functions for reading the energy from the output, by method
ENERGY_READER_DCT = {
    elstruct.par.Method.HF[0]: _hf_energy,
    elstruct.par.Method.Corr.MP2[0]: _mp2_energy,
}

METHODS = elstruct.par.program_methods(PROG)
for METHOD in METHODS:
    if elstruct.par.Method.is_dft(METHOD):
        method_name = elstruct.par.program_method_name(PROG, METHOD)
        ENERGY_READER_DCT[METHOD] = _dft_energy_(method_name)

assert all(method in ENERGY_READER_DCT for method in METHODS)


def energy(method, output_string):
    """ get total energy from output
    """
    # get the appropriate reader and call it
    energy_reader = ENERGY_READER_DCT[method]
    return energy_reader(output_string)
