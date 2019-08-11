""" electronic energy readers
"""
import autoread as ar
import autoparse.pattern as app
import elstruct.par

PROG = elstruct.par.Program.ORCA4


def _scf_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.LINESPACES.join([
            app.escape('Total Energy'), ':'])
        )
    return ene


def _mp2_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.one_of_these([
            app.escape('MP2 TOTAL ENERGY:'),
            app.LINESPACES.join([
                app.escape('Initial E(tot)'), '...'])
        ]))
    return ene


def _ccsd_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.LINESPACES.join([
            app.escape('E(CCSD)'), '...'])
        )
    return ene


def _ccsd_t_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.LINESPACES.join([
            app.escape('E(CCSD(T))'), '...'])
        )
    return ene


# a dictionary of functions for reading the energy from the output, by method
ENERGY_READER_DCT = {
    elstruct.par.Method.HF[0]: _scf_energy,
    elstruct.par.Method.Corr.MP2[0]: _mp2_energy,
    elstruct.par.Method.Corr.CCSD[0]: _ccsd_energy,
    elstruct.par.Method.Corr.CCSD_T[0]: _ccsd_t_energy,
}

METHODS = elstruct.par.program_methods(PROG)
for METHOD in METHODS:
    if elstruct.par.Method.is_standard_dft(METHOD):
        ENERGY_READER_DCT[METHOD] = _scf_energy

assert all(method in ENERGY_READER_DCT for method in METHODS)


def energy(method, output_string):
    """ get total energy from output
    """

    # get the appropriate reader and call it
    if elstruct.par.Method.is_nonstandard_dft(method):
        energy_reader = _scf_energy
    else:
        energy_reader = ENERGY_READER_DCT[method]

    return energy_reader(output_string)
