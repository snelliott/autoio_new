""" electronic energy readers
"""
import autoread as ar
import autoparse.pattern as app
import elstruct.par

PROG = elstruct.par.Program.ORCA4


def _scf_energy(output_str):
    """ Reads the SCF energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        app.LINESPACES.join([
            app.escape('Total Energy'), ':'])
        )

    return ene


def _mp2_energy(output_str):
    """ Reads the MP2 energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        app.one_of_these([
            app.escape('MP2 TOTAL ENERGY:'),
            app.LINESPACES.join([
                app.escape('Initial E(tot)'), '...'])
        ]))

    return ene


def _ccsd_energy(output_str):
    """ Reads the CCSD energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        app.LINESPACES.join([
            app.escape('E(CCSD)'), '...'])
        )

    return ene


def _ccsd_t_energy(output_str):
    """ Reads the CCSD(T) energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        app.LINESPACES.join([
            app.escape('E(CCSD(T))'), '...'])
        )

    return ene


# A dictionary of functions for reading the energy from the output, by method
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


def method_list():
    """ Constructs a list of available electronic structure methods.
    """
    return tuple(sorted(ENERGY_READER_DCT.keys()))


def energy(method, output_str):
    """ get total energy from output
    """

    assert method in method_list()

    # Get the appropriate reader and call it
    if elstruct.par.Method.is_nonstandard_dft(method):
        energy_reader = _scf_energy
    else:
        energy_reader = ENERGY_READER_DCT[method]

    return energy_reader(output_str)
