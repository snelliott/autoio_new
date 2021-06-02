""" electronic energy readers
"""

import autoread as ar
import autoparse.pattern as app
import elstruct.par


PROG = elstruct.par.Program.QCHEM5


def _scf_energy(output_str):
    """ Reads the SCF energy (for Hartree-Fock or Density Functional Theory)
        from the output file string. Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ptt1 = (
        'Total energy in the final basis set =' +
        app.SPACES + app.capturing(app.FLOAT)
    )
    ptt2 = (
        'SCF energy' + app.SPACES + '=' +
        app.SPACES + app.capturing(app.FLOAT)
    )

    for _ptt in (ptt1, ptt2):
        ene = ar.energy.read(output_str, _ptt)
        if ene is not None:
            break

    return ene


def _mp2_energy(output_str):
    """ Reads the MP2 energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ptt1 = (
        'MP2' + app.SPACES + 'total energy =' +
        app.SPACES + app.capturing(app.FLOAT) + app.SPACES + 'au'
    )
    ptt2 = (
        'MP2 energy' + app.SPACES + '=' + app.SPACES + app.capturing(app.FLOAT)
    )

    for _ptt in (ptt1, ptt2):
        ene = ar.energy.read(output_str, _ptt)
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

    ptt = (
        'CCSD total energy' + app.SPACES + '=' +
        app.SPACES + app.capturing(app.FLOAT)
    )

    ene = ar.energy.read(output_str, ptt)

    return ene


def _ccsd_t_energy(output_str):
    """ Reads the CCSD(T) energy from the output file string.
        Returns the energy in Hartrees.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: float
    """

    ptt = app.one_of_these([
        'CCSD(T) total energy' + app.SPACES + '='
        + app.SPACES + app.capturing(app.FLOAT)
    ])

    ene = ar.energy.read(output_str, ptt)

    return ene


# A dictionary of functions for reading the energy from the output, by method
ENERGY_READER_DCT = {
    elstruct.par.Method.HF[0]: _scf_energy,
    elstruct.par.Method.Corr.MP2[0]: _mp2_energy,
    elstruct.par.Method.Corr.CCSD[0]: _ccsd_energy,
    elstruct.par.Method.Corr.CCSD_T[0]: _ccsd_t_energy
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
    energy_reader = ENERGY_READER_DCT[method]

    return energy_reader(output_str)
