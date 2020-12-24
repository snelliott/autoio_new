""" Tests the writing of the energy transfer section
"""

import onedmin_io
from _util import read_text_file


# Input parameters
RANSEED = 28384920
NSAMP = 10
TARGET_XYZ_NAME = 'target.xyz'
BATH_XYZ_NAME = 'bath.xyz'
SMIN = 2.0
SMAX = 5.0

# Submission script parameters
NJOBS = 20
JOB_PATH = 'job'
ONEDMIN_PATH = 'run'
EXE_NAME = '1dmin.x'


def test__input_file():
    """ test onedmin_io.writer.input_file
    """

    onedmin_inp1_str = onedmin_io.writer.input_file(
        RANSEED, NSAMP, SMIN, SMAX,
        TARGET_XYZ_NAME, BATH_XYZ_NAME)

    onedmin_inp2_str = onedmin_io.writer.input_file(
        RANSEED, NSAMP, SMIN, SMAX,
        TARGET_XYZ_NAME, BATH_XYZ_NAME,
        spin_method=1)

    assert onedmin_inp1_str == read_text_file(['data'], 'onedmin1.inp')
    assert onedmin_inp2_str == read_text_file(['data'], 'onedmin2.inp')


def test__submission_script():
    """ test onedmin_io.writer.submission_script
    """

    subscript1_str = onedmin_io.writer.submission_script(
        NJOBS, JOB_PATH, ONEDMIN_PATH)

    subscript2_str = onedmin_io.writer.submission_script(
        NJOBS, JOB_PATH, ONEDMIN_PATH,
        exe_name=EXE_NAME)

    assert subscript1_str == read_text_file(['data'], 'subscript1.inp')
    assert subscript2_str == read_text_file(['data'], 'subscript2.inp')


if __name__ == '__main__':
    test__input_file()
    test__submission_script()
