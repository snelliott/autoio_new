""" electronic energy readers
"""
import autoread as ar
import autoparse.pattern as app
import elstruct.par

PROG = elstruct.par.Program.MOLPRO


def _hf_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.one_of_these([
            app.LINESPACES.join([
                app.escape('!RHF STATE'), app.FLOAT, app.escape('Energy')]),
            app.LINESPACES.join([
                app.escape('!UHF STATE'), app.FLOAT, app.escape('Energy')]),
        ]))
    return ene


def _ccsd_energy(output_string):
    ene = ar.energy.read(
        output_string,
        app.one_of_these([
            app.escape('!CCSD total energy') + app.maybe(':'),
            app.escape('!RHF-UCCSD energy'),
        ]))
    return ene


# a dictionary of functions for reading the energy from the output, by method
ENERGY_READER_DCT = {
    elstruct.par.Method.HF[0]: _hf_energy,
    elstruct.par.Method.Corr.CCSD[0]: _ccsd_energy,
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
