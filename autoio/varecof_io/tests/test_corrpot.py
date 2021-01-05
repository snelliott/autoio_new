"""
  Tests the varecof_io.writer functions
"""

import os
import tempfile
import shutil
import varecof_io
from _util import read_text_file


# Set paths for building files
TMP_PATH = tempfile.mkdtemp()

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

    with open('data/mol_corr1.f', 'w') as f:
        f.write(spc_corr1_str)
    with open('data/mol_corr2.f', 'w') as f:
        f.write(spc_corr2_str)
    assert spc_corr1_str == read_text_file(['data'], 'mol_corr1.f')
    assert spc_corr2_str == read_text_file(['data'], 'mol_corr.f')


def test__dummy_writer():
    """ tests varecof_io.writer.corr_potentials.dummy
    """

    dummy_corr_str = varecof_io.writer.corr_potentials.dummy()

    with open('data/dummy_corr.f', 'w') as f:
        f.write(dummy_corr_str)
    assert dummy_corr_str == read_text_file(['data'], 'dummy_corr.f')


def test__auxiliary_writer():
    """ tests varecof_io.writer.corr_potentials.auxiliary
    """
    pot_aux_str = varecof_io.writer.corr_potentials.auxiliary()

    with open('data/pot_aux.f', 'w') as f:
        f.write(pot_aux_str)
    assert pot_aux_str == read_text_file(['data'], 'pot_aux.f')


def test__makefile_writer():
    """ tests varecof_io.writer.corr_potentials.makefile
    """

    makefile1_str = varecof_io.writer.corr_potentials.makefile(
        FORTRAN_COMPILER)

    makefile2_str = varecof_io.writer.corr_potentials.makefile(
        FORTRAN_COMPILER,
        pot_file_names=SPECIES_CORR_POTENTIALS)

    with open('data/makefile1', 'w') as f:
        f.write(makefile1_str)
    with open('data/makefile', 'w') as f:
        f.write(makefile2_str)
    assert makefile1_str == read_text_file(['data'], 'makefile1')
    assert makefile2_str == read_text_file(['data'], 'makefile')


def test__compile_correction_potential():
    """ test varecof_io.writer.corr_potentials.compile_correction_pot
    """

    os.makdir(TMP_DIR)

    varecof_io.writer.corr_potentials.compile_corr_pot(TMP_DIR)


if __name__ == '__main__':
    test__species_writer()
    test__dummy_writer()
    test__auxiliary_writer()
    test__makefile_writer()
    test__compile_correction_potential()
