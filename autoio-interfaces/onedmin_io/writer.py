"""
Executes the automation part of OneDMin
"""

import os
from random import randrange
from ioformat import build_mako_str


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')


def input_file(nsamp, smin, smax, ranseed=None,
               target_xyz_name='target.xyz', bath_xyz_name='bath.xyz',
               spin_method=2):
    """ writes the 1dmin input file for each instance
    """

    if ranseed is not None:
        assert isinstance(ranseed, int)
    else:
        ranseed = randrange(1E8, 1E9)

    assert isinstance(nsamp, int)
    assert target_xyz_name.endswith('.xyz')
    assert bath_xyz_name.endswith('.xyz')
    assert isinstance(smin, float)
    assert isinstance(smax, float)

    # Set the dictionary for the 1DMin input file
    inp_keys = {
        "ranseed": ranseed,
        "nsamples": nsamp,
        "target_xyz_name": target_xyz_name,
        "bath_xyz_name": bath_xyz_name,
        "smin": smin,
        "smax": smax,
        "spin_method": spin_method
    }

    return build_mako_str(
        template_file_name='onedmin_inp.mako',
        template_src_path=TEMPLATE_PATH,
        template_keys=inp_keys)


def submission_script(njobs, run_dir, exe_path):
    """ launches the job

        :param njobs: number of OneDMin processes to run
        :type njobs: int
        :param run_dir: directory to run each OneDMin process
        :type run_dir: str
        :param exe_path: full path to the OneDMin executable
        :type exe_path: str
    """

    # Write the string for running all of the job lines
    # job_lines = 'mkdir -p {0}/run1\n'.format(run_dir)
    job_lines = 'cd {0}/run1\n'.format(run_dir)
    job_lines += 'time $ONEDMINEXE < input.dat > output.dat &\n'
    for i in range(njobs-1):
        # job_lines += 'mkdir -p ../run{0}\n'.format(str(i+2))
        job_lines += 'cd ../run{0}\n'.format(str(i+2))
        job_lines += 'time $ONEDMINEXE < input.dat > output.dat &\n'
    job_lines += 'wait\n'

    # Set the dictionary for the 1DMin input file
    exe_keys = {
        "exe_path": exe_path,
        "job_lines": job_lines
    }

    return build_mako_str(
        template_file_name='onedmin_sub.mako',
        template_src_path=TEMPLATE_PATH,
        template_keys=exe_keys)
