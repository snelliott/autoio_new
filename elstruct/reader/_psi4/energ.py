""" electronic energy readers
"""
import autoread as ar
import autoparse.pattern as app
import elstruct.par

PROG = elstruct.par.Program.PSI4


def _hf_energy(output_string):
    ene = ar.energy.read(
        output_string,
        start_ptt=app.one_of_these([
            app.escape('@RHF Final Energy:'),
            app.escape('@ROHF Final Energy:'),
            app.escape('@UHF Final Energy:')]))
    return ene


def _dft_energy(output_string):
    ene = ar.energy.read(
        output_string,
        start_ptt=app.one_of_these([
            app.escape('@RKS Final Energy:'),
            app.escape('@UKS Final Energy:')]))
    return ene


def _mp2_energy(output_string):
    ene = ar.energy.read(
        output_string,
        start_ptt=app.LINESPACES.join([
            '', app.escape('MP2 Total Energy (a.u.)'), app.escape(':')]))
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
