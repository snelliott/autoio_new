""" Methods for calculation submission using BASH scripts
"""

import os
import subprocess
import warnings
import stat


SCRIPT_NAME = 'run.sh'
INPUT_NAME = 'run.inp'
OUTPUT_NAME = 'run.out'


def from_input_string(script_str, run_dir, input_str,
                      script_name=SCRIPT_NAME,
                      input_name=INPUT_NAME,
                      output_name=OUTPUT_NAME):
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
        with open(script_name, 'w') as script_obj:
            script_obj.write(script_str)

        # make the script executable
        os.chmod(script_name, mode=os.stat(script_name).st_mode | stat.S_IEXEC)

        # write the input string to the run directory
        with open(input_name, 'w') as input_obj:
            input_obj.write(input_str)

        # call the electronic structure program
        try:
            subprocess.check_call('./{:s}'.format(script_name))
        except subprocess.CalledProcessError as err:
            # as long as the program wrote an output, continue with a warning
            if os.path.isfile(output_name):
                warnings.warn("elstruct run failed in {}".format(run_dir))
            else:
                raise err

        # read the output string from the run directory
        assert os.path.isfile(output_name), (
            '{} is should be a file, but it is not'.format(output_name)
        )
        with open(output_name, 'r') as output_obj:
            output_str = output_obj.read()

    return output_str


def run_script(script_str, run_dir, script_name=SCRIPT_NAME):
    """ run a program from a script
    """

    with _EnterDirectory(run_dir):
        # Write the submit script to the run directory
        print('trying to delete {}: {}', script_name, run_dir)
        try:
            os.remove(script_name)
            with open(script_name, 'w') as script_obj:
                script_obj.write(script_str)
            print('succeeded in deleting {}:'.format(script_name))
        except IOError:
            with open(script_name, 'w') as script_obj:
                script_obj.write(script_str)
            print('failed to delete {}:'.format(script_name))

        # Make the script executable
        os.chmod(script_name, mode=os.stat(script_name).st_mode | stat.S_IEXEC)

        # Call the program
        try:
            subprocess.check_call('./{:s}'.format(script_name))
        except subprocess.CalledProcessError:
            # If the program failed, continue with a warning
            warnings.warn("run failed in {}".format(run_dir))


class _EnterDirectory():

    def __init__(self, directory):
        assert os.path.isdir(directory)
        self.directory = directory
        self.working_directory = os.getcwd()

    def __enter__(self):
        os.chdir(self.directory)

    def __exit__(self, _exc_type, _exc_value, _traceback):
        os.chdir(self.working_directory)
