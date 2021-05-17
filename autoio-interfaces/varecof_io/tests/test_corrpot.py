"""
  Tests the varecof_io.writer functions
"""

import os
import tempfile
from ioformat import read_text_file
from ioformat import write_text_file
import varecof_io


# Set paths for building files
TMP_PATH = tempfile.mkdtemp()
PATH = os.path.dirname(os.path.realpath(__file__))

# Set variables
NPOT = 5
BND_IDXS = [1, 3]
RVALS = [1.5958, 1.6958, 1.7958, 1.8958, 1.9958,
         2.0958, 2.1958, 2.2958, 2.3958, 2.4958]

POTENTIALS = [
    [0.052, 0.175, 0.430, 0.724, 0.996,
     1.199, 1.308, 1.317, 1.243, 1.113],
    [-0.722, -0.517, -0.372, -0.277, -0.218,
     -0.181, -0.153, -0.126, -0.096, -0.064],
    [0.224, 0.329, 0.556, 0.823, 1.071,
     1.255, 1.348, 1.346, 1.263, 1.127]
]
SPECIES_NAME = 'mol'
POT_LABELS = ['basis+relaxed', 'basis', 'relaxed']
FORTRAN_COMPILER = 'x86_64-conda_cos6-linux-gnu-gfortran'  # from conda-forge
SPECIES_CORR_POTENTIALS = ['mol']
DIST_RESTRICT_IDXS = [[1, 5]]


def test__species_writer():
    """ tests varecof_io.writer.corr_potentials.species
    """

    spc_corr1_str = varecof_io.writer.corr_potentials.species(
        RVALS, POTENTIALS, BND_IDXS)

    spc_corr2_str = varecof_io.writer.corr_potentials.species(
        RVALS, POTENTIALS, BND_IDXS,
        species_name=SPECIES_NAME,
        pot_labels=POT_LABELS,
        dist_restrict_idxs=DIST_RESTRICT_IDXS)

    assert spc_corr1_str == read_text_file(['data'], 'mol_corr2.f', PATH)
    assert spc_corr2_str == read_text_file(['data'], 'mol_corr.f', PATH)


def test__dummy_writer():
    """ tests varecof_io.writer.corr_potentials.dummy
    """

    dummy_corr_str = varecof_io.writer.corr_potentials.dummy()

    assert dummy_corr_str == read_text_file(['data'], 'dummy_corr.f', PATH)


def test__auxiliary_writer():
    """ tests varecof_io.writer.corr_potentials.auxiliary
    """
    pot_aux_str = varecof_io.writer.corr_potentials.auxiliary()

    assert pot_aux_str == read_text_file(['data'], 'pot_aux.f', PATH)


def test__makefile_writer():
    """ tests varecof_io.writer.corr_potentials.makefile
    """

    makefile1_str = varecof_io.writer.corr_potentials.makefile(
        FORTRAN_COMPILER)

    makefile2_str = varecof_io.writer.corr_potentials.makefile(
        FORTRAN_COMPILER,
        pot_file_names=SPECIES_CORR_POTENTIALS)

    assert makefile1_str == read_text_file(['data'], 'makefile1', PATH)
    assert makefile2_str == read_text_file(['data'], 'makefile', PATH)


def test__compile_correction_potential():
    """ test varecof_io.writer.corr_potentials.compile_correction_pot
    """

    write_text_file([TMP_PATH], 'mol_corr.f',
                    read_text_file(['data'], 'mol_corr.f', PATH), PATH)
    write_text_file([TMP_PATH], 'pot_aux.f',
                    read_text_file(['data'], 'pot_aux.f', PATH), PATH)
    write_text_file([TMP_PATH], 'dummy_corr.f',
                    read_text_file(['data'], 'dummy_corr.f', PATH), PATH)
    write_text_file([TMP_PATH], 'makefile',
                    read_text_file(['data'], 'makefile', PATH), PATH)
    varecof_io.writer.corr_potentials.compile_corr_pot(TMP_PATH)

    assert os.path.exists(os.path.join(TMP_PATH, 'libcorrpot.so'))


if __name__ == '__main__':
    test__species_writer()
    test__dummy_writer()
    test__auxiliary_writer()
    test__makefile_writer()
    test__compile_correction_potential()
