""" core run function
"""
import os
import stat
import tempfile
import subprocess
import warnings

SCRIPT_NAME = 'run.sh'
INPUT_NAME = 'input.dat'
OUTPUT_NAME = 'output.dat'


def direct(script_str, input_writer,
           prog, method, basis, geom, mult, charge, **kwargs):
    """ generate an input file from arguments and run it directly

    :returns: the input string, the output string, and the run directory
    :rtype: (str, str, str)
    """
    input_str = input_writer(prog, method, basis, geom, mult, charge, **kwargs)
    output_str, run_dir = from_input_string(script_str, input_str)
    return (input_str, output_str, run_dir)


def from_input_string(script_str, input_str):
    """ run the program in a temporary directory and return the output

    :returns: the output string and the run directory
    :rtype: (str, str)
    """
    run_dir = tempfile.mkdtemp()

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
        assert os.path.isfile(OUTPUT_NAME)
        with open(OUTPUT_NAME, 'r') as output_obj:
            output_str = output_obj.read()

    return (output_str, run_dir)


class _EnterDirectory():

    def __init__(self, directory):
        assert os.path.isdir(directory)
        self.directory = directory
        self.working_directory = os.getcwd()

    def __enter__(self):
        os.chdir(self.directory)

    def __exit__(self, _exc_type, _exc_value, _traceback):
        os.chdir(self.working_directory)
