""" electronic energy readers
"""
import autoread as ar
import autoparse.pattern as app
import elstruct.par

PROG = elstruct.par.Program.NWCHEM6


def _hf_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.escape('Total SCF energy =')
        )
    return ene


def _mp2_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.escape('Total MP2 energy:')
        )
    return ene


def _ccsd_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.escape('Total CCSD energy:')
        )
    return ene


def _ccsd_t_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.escape('Total CCSD(T) energy:')
        )
    return ene


# a dictionary of functions for reading the energy from the output, by method
ENERGY_READER_DCT = {
    elstruct.par.Method.HF[0]: _hf_energy,
    elstruct.par.Method.Corr.MP2[0]: _mp2_energy,
    elstruct.par.Method.Corr.CCSD[0]: _ccsd_energy,
    elstruct.par.Method.Corr.CCSD_T[0]: _ccsd_t_energy,
}

METHODS = elstruct.par.program_methods(PROG)

assert all(method in ENERGY_READER_DCT for method in METHODS)


def energy(method, output_string):
    """ get total energy from output
    """

    # get the appropriate reader and call it
    energy_reader = ENERGY_READER_DCT[method]

    return energy_reader(output_string)
