""" electronic energy readers
"""
import autoread as ar
import autoparse.pattern as app
import elstruct.par

PROG = elstruct.par.Program.MRCC2018


def _hf_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.one_of_these([
            app.escape('***FINAL HARTREE-FOCK ENERGY:'),
            app.escape('***SEMICANONICAL ROHF ENERGY:'),
        ]))
    return ene


def _mp2_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.one_of_these([
            app.escape('Total MP2 energy [au]:'),
            app.escape('MP2 energy [au]:')
        ]))
    return ene


def _ccsd_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.escape('Total CCSD energy [au]:')
        )
    return ene


def _ccsd_t_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.escape('CCSD(T) total energy [au]:')
        )
    return ene


def _ccsdt_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.escape('Total CCSDT energy [au]:')
        )
    return ene


def _ccsdt_q_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.one_of_these([
            app.escape('Total CCSDT(Q) energy [au]:'),
            app.escape('Total CCSDT(Q)/B energy [au]:'),
        ]))
    return ene


# a dictionary of functions for reading the energy from the output, by method
ENERGY_READER_DCT = {
    elstruct.par.Method.HF[0]: _hf_energy,
    elstruct.par.Method.Corr.MP2[0]: _mp2_energy,
    elstruct.par.Method.Corr.CCSD[0]: _ccsd_energy,
    elstruct.par.Method.Corr.CCSD_T[0]: _ccsd_t_energy,
    elstruct.par.Method.Corr.CCSDT[0]: _ccsdt_energy,
    elstruct.par.Method.Corr.CCSDT_Q[0]: _ccsdt_q_energy,
}
METHODS = elstruct.par.program_methods(PROG)
assert all(method in ENERGY_READER_DCT for method in METHODS)


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
