""" core run function
"""

import os
import stat
import subprocess
import warnings


SCRIPT_NAME = 'run.sh'
INPUT_NAME = 'run.inp'
OUTPUT_NAME = 'run.out'


def direct(input_writer, script_str, run_dir, prog,
           geo, charge, mult, method, basis, **kwargs):
    """ Generates an input file for an electronic structure job and
        runs it directly.

        :param input_writer: elstruct writer module function for desired job
        :type input_writer: elstruct function
        :param script_str: string of bash script that contains
            execution instructions electronic structure job
        :type script_str: str
        :param run_dir: name of directory to run electronic structure job
        :type run_dir: str
        :param prog: electronic structure program to run
        :type prog: str
        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
        :param charge: molecular charge
        :type charge: int
        :param mult: spin multiplicity
        :type mult: int
        :param method: electronic structure method
        :type method: str
        :returns: the input string, the output string, and the run directory
        :rtype: (str, str)
    """
    input_str = input_writer(
        prog=prog,
        geo=geo, charge=charge, mult=mult, method=method, basis=basis,
        **kwargs)
    output_str = from_input_string(script_str, run_dir, input_str)
    return input_str, output_str


def from_input_string(script_str, run_dir, input_str):
    """ run the program in a temporary directory and return the output

        :param script_str: string of bash script that contains
            execution instructions electronic structure job
        :type script_str: str
        :param run_dir: name of directory to run electronic structure job
        :type run_dir: str
        :param input_str: string of input file for electronic structure job
        :type input_str: str
        :returns: the output string and the run directory
        :rtype: str
    """

    with _EnterDirectory(run_dir):
        # write the submit script to the run directory
        with open(SCRIPT_NAME, 'w') as script_obj:
            script_obj.write(script_str)

        # make the script executable
        os.chmod(SCRIPT_NAME, mode=os.stat(SCRIPT_NAME).st_mode | stat.S_IEXEC)

        # write the input string to the run directory
        with open(INPUT_NAME, 'w') as input_obj:
            input_obj.write(input_str)

        # call the electronic structure program
        try:
            subprocess.check_call('./{:s}'.format(SCRIPT_NAME))
        except subprocess.CalledProcessError as err:
            # as long as the program wrote an output, continue with a warning
            if os.path.isfile(OUTPUT_NAME):
                warnings.warn("elstruct run failed in {}".format(run_dir))
            else:
                raise err

        # read the output string from the run directory
        assert os.path.isfile(OUTPUT_NAME), (
            '{} is should be a file, but it is not'.format(OUTPUT_NAME)
        )
        with open(OUTPUT_NAME, 'r') as output_obj:
            output_str = output_obj.read()

    return output_str


class _EnterDirectory():
    """ Controls entering and exiting directories for running calculations.
    """

    def __init__(self, directory):
        assert os.path.isdir(directory)
        self.directory = directory
        self.working_directory = os.getcwd()

    def __enter__(self):
        os.chdir(self.directory)

    def __exit__(self, _exc_type, _exc_value, _traceback):
        os.chdir(self.working_directory)
