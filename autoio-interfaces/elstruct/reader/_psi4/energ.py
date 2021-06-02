""" electronic energy readers
"""

import autoread as ar
import autoparse.pattern as app
import autoparse.find as apf
import elstruct.par


PROG = elstruct.par.Program.PSI4


def _hf_energy(output_str):
    """ Reads the Hartree-Fock energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        start_ptt=app.one_of_these([
            app.escape('@RHF Final Energy:'),
            app.escape('@ROHF Final Energy:'),
            app.escape('@UHF Final Energy:')]))

    return ene


def _df_hf_energy(output_str):
    """ Reads the Hartree-Fock energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        start_ptt=app.one_of_these([
            app.escape('@DF-RHF Final Energy:'),
            app.escape('@DF-ROHF Final Energy:'),
            app.escape('@DF-UHF Final Energy:')]))

    return ene


def _mp2_energy(output_str):
    """ Reads the MP2 energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    start_ptts = (
        (app.LINESPACES.join([
            '', app.escape('MP2 Total Energy (a.u.)'), app.escape(':')])),
        (app.LINESPACES.join([
            '', app.escape('MP2 total energy'), app.escape('=')]))
    )

    for ptt in start_ptts:
        ene = ar.energy.read(output_str, start_ptt=ptt)
        if ene is not None:
            break

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
        start_ptt=app.LINESPACES.join([
            '', app.escape('* CCSD correlation energy'), app.escape('=')]))

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
        start_ptt=app.LINESPACES.join([
            '', app.escape('* CCSD(T) correlation energy'), app.escape('=')]))

    return ene


def _df_mp2_energy(output_str):
    """ Reads the DF-MP2 energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """
    block_ptt = (
        app.escape(
            '==================> DF-MP2 Energies <====================') +
        app.capturing(app.one_or_more(app.WILDCARD, greedy=False)) +
        app.escape(
            '==================> DF-SCS-MP2 Energies <====================')
    )
    block = apf.last_capture(block_ptt, output_str)

    if block is not None:
        start_ptt = 'Total Energy' + app.SPACES + '=' + app.SPACES
        ene = ar.energy.read(block, start_ptt=start_ptt)
        print('ene', ene)
    else:
        ene = None

    return ene


def _dft_energy(output_str):
    """ Reads the energy from most density functional theory methods
        from the output file string. Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        start_ptt=app.one_of_these([
            app.escape('@RKS Final Energy:'),
            app.escape('@UKS Final Energy:')]))

    return ene


def _df_dft_energy(output_str):
    """ Reads the energy from most density functional theory methods
        from the output file string. Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ene = ar.energy.read(
        output_str,
        start_ptt=app.one_of_these([
            app.escape('@DF-RKS Final Energy:'),
            app.escape('@DF-UKS Final Energy:')]))

    return ene


# A dictionary of functions for reading the energy from the output, by method
ENERGY_READER_DCT = {
    elstruct.par.Method.HF[0]: _hf_energy,
    elstruct.par.Method.DF_HF[0]: _df_hf_energy,
    elstruct.par.Method.Corr.MP2[0]: _mp2_energy,
    # elstruct.par.Method.Corr.DF_MP2[0]: _df_mp2_energy,
    elstruct.par.Method.Corr.CCSD[0]: _ccsd_energy,
    elstruct.par.Method.Corr.CCSD_T[0]: _ccsd_t_energy,
}

METHODS = elstruct.par.program_methods(PROG)
for METHOD in METHODS:
    if elstruct.par.Method.is_standard_dft(METHOD):
        if not elstruct.par.Method.is_density_fitting(METHOD):
            ENERGY_READER_DCT[METHOD] = _dft_energy
        else:
            ENERGY_READER_DCT[METHOD] = _df_dft_energy

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

    # Get the appropriate reader and call it
    if elstruct.par.Method.is_nonstandard_dft(method):
        energy_reader = _dft_energy
    else:
        energy_reader = ENERGY_READER_DCT[method]

    return energy_reader(output_str)
