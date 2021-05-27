""" Tests the writing of the energy transfer section
"""

import os
from ioformat import read_text_file
import onedmin_io.writer


PATH = os.path.dirname(os.path.realpath(__file__))

# Input parameters
RANSEED = 28384920
NSAMP = 10
TARGET_XYZ_NAME = 'target.xyz'
BATH_XYZ_NAME = 'bath.xyz'
SMIN = 3.77945
SMAX = 9.44863

# Submission script parameters
NJOBS = 20
RUN_DIR = 'job'
EXE_PATH = 'onedmin.x'


def test__input_file():
    """ test onedmin_io.writer.input_file
    """

    onedmin_inp1_str = onedmin_io.writer.input_file(
        NSAMP, SMIN, SMAX, ranseed=RANSEED)

    onedmin_inp2_str = onedmin_io.writer.input_file(
        NSAMP, SMIN, SMAX, ranseed=RANSEED,
        target_xyz_name=TARGET_XYZ_NAME, bath_xyz_name=BATH_XYZ_NAME,
        spin_method=1)

    assert onedmin_inp1_str == read_text_file(['data'], 'onedmin1.inp', PATH)
    assert onedmin_inp2_str == read_text_file(['data'], 'onedmin2.inp', PATH)


def test__submission_script():
    """ test onedmin_io.writer.submission_script
    """

    subscript_str = onedmin_io.writer.submission_script(
        NJOBS, RUN_DIR, EXE_PATH)

    assert subscript_str == read_text_file(['data'], 'subscript.inp', PATH)
