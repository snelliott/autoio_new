""" electronic energy readers
"""

import autoread as ar
import autoparse.pattern as app
import autoparse.find as apf
import elstruct.par


PROG = elstruct.par.Program.MOLPRO2015

BASIS_PATTERN = app.one_or_more(
    app.one_of_these(
        [app.LETTER, app.NUMBER, app.escape('*'), app.escape('-'),
         app.escape('('), app.escape(')')])
    )


def _hf_energy(output_str):
    """ Reads the Hartree-Fock energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        app.one_of_these([
            app.LINESPACES.join([
                app.escape('!RHF STATE'), app.FLOAT, app.escape('Energy')]),
            app.LINESPACES.join([
                app.escape('!UHF STATE'), app.FLOAT, app.escape('Energy')]),
        ]))

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
            app.escape('!MP2 total energy') + app.maybe(':'),
            app.escape('!RMP2 energy'),
        ]))

    return ene


def _ccsd_energy(output_str):
    """ Reads the CCSD/UCCSD energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        app.one_of_these([
            app.escape('!CCSD total energy') + app.maybe(':'),
            app.escape('!RHF-UCCSD energy'),
        ]))

    return ene


def _ccsd_t_energy(output_str):
    """ Reads the CCSD(T)/UCCSD(T) energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        app.one_of_these([
            app.escape('!CCSD(T) total energy') + app.maybe(':'),
            app.escape('!RHF-UCCSD(T) energy'),
            app.LINESPACES.join([
                app.escape('!CCSD(T) STATE'),
                app.FLOAT,
                app.escape('Energy')]),
        ]))

    return ene


def _ccsdt_energy(output_str):
    """ Reads the CCSDT energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        app.one_of_these([
            app.LINESPACES.join([
                app.escape('!CCSDT STATE'),
                app.FLOAT,
                app.escape('Energy')]),
        ]))

    return ene


def _ccsdt_q_energy(output_str):
    """ Reads the CCSDT(Q) energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        app.one_of_these([
            app.LINESPACES.join([
                app.escape('!CCSDT(Q) STATE'),
                app.FLOAT,
                app.escape('Energy')]),
        ]))

    return ene


def _ccsd_t_f12_energy(output_str):
    """ Reads the CCSD(T)-F12/UCCSD(T)-F12 energy from the output file string.
        Currently, the function only reads the energy of the F12b variant.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        app.one_of_these([
            app.escape('!CCSD(T)-F12b total energy') + app.maybe(':'),
            app.escape('!RHF-UCCSD(T)-F12b energy'),
        ]))
    return ene


def _casscf_energy(output_str):
    """ Reads the CASSCF energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        app.LINESPACES.join([
            app.escape('!MCSCF STATE'), app.FLOAT, app.escape('Energy')]),
        )

    return ene


def _caspt2_energy(output_str):
    """ Reads the CASPT2 energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        app.LINESPACES.join([
            app.escape('!RSPT2 STATE'), app.FLOAT, app.escape('Energy')]),
        )

    return ene


def _mrci_energy(output_str):
    """ Reads the MRCISD+Q energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        app.LINESPACES.join([
            app.escape('!MRCI STATE'), app.FLOAT, app.escape('Energy')]),
        )

    return ene


def _end_file_energy(output_str):
    """ Reads a user-defined electronic energy in the output string that has
        be given the variable name is MOLPRO_ENERGY.
        Returns the energy in Hartrees.
    """

    end_file_ptt = (
        'MOLPRO_ENERGY' + app.SPACES +
        app.escape('=') + app.SPACES +
        app.capturing(app.FLOAT) + app.SPACES +
        'AU'
    )
    ene = apf.last_capture(end_file_ptt, output_str)
    ene = float(ene) if ene is not None else ene

    return ene


# A dictionary of functions for reading the energy from the output, by method
ENERGY_READER_DCT = {
    elstruct.par.Method.HF[0]: _hf_energy,
    elstruct.par.Method.Corr.MP2[0]: _mp2_energy,
    elstruct.par.Method.Corr.CCSD[0]: _ccsd_energy,
    elstruct.par.Method.Corr.CCSD_T[0]: _ccsd_t_energy,
    elstruct.par.Method.Corr.CCSDT[0]: _ccsdt_energy,
    elstruct.par.Method.Corr.CCSDT_Q[0]: _ccsdt_q_energy,
    elstruct.par.Method.Corr.CCSD_T_F12[0]: _ccsd_t_f12_energy,
    elstruct.par.Method.MultiRef.CASSCF[0]: _casscf_energy,
    elstruct.par.Method.MultiRef.CASPT2[0]: _caspt2_energy,
    elstruct.par.Method.MultiRef.CASPT2I[0]: _caspt2_energy,
    elstruct.par.Method.MultiRef.CASPT2C[0]: _caspt2_energy,
    elstruct.par.Method.MultiRef.MRCISDQ[0]: _mrci_energy,
}
METHODS = elstruct.par.program_methods(PROG)

assert all(method in ENERGY_READER_DCT for method in METHODS)


def method_list():
    """ Constructs a list of available electronic structure methods.
    """
    return tuple(sorted(ENERGY_READER_DCT.keys()))


def energy(method, output_str):
    """ Reads the the total electronic energy from the output file string.
        Returns the energy in Hartrees.

        :param method: electronic structure method to read
        :type method: str
        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    assert method in method_list()

    # First try and grab the energy printed at the end of the file
    ene = _end_file_energy(output_str)

    # If no energy is found, get the appropriate reader and call it
    if ene is None:
        energy_reader = ENERGY_READER_DCT[method]
        ene = energy_reader(output_str)

    return ene
