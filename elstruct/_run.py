""" a simple helper command for running a given program
"""
import os
import tempfile
import subprocess
import warnings


def run(script_str, input_str,
        shell_exe='bash',
        script_name='run.sh',
        input_name='input.dat',
        output_name='output.dat',
        return_path=False):
    """ run the program in a temporary directory and return the output
    """
    tmp_dir = tempfile.mkdtemp()

    with _EnterDirectory(tmp_dir):
        # write the submit script to the run directory
        with open(script_name, 'w') as script_obj:
            script_obj.write(script_str)

        # write the input string to the run directory
        with open(input_name, 'w') as input_obj:
            input_obj.write(input_str)

        # call the electronic structure program
        try:
            subprocess.check_call([shell_exe, script_name])
        except subprocess.CalledProcessError as err:
            # as long as the program wrote an output, continue with a warning
            if os.path.isfile(output_name):
                warnings.warn("elstruct run failed in {}".format(tmp_dir))
            else:
                raise err

        # read the output string from the run directory
        with open(output_name, 'r') as output_obj:
            output_str = output_obj.read()

    return output_str if not return_path else (output_str, tmp_dir)


class _EnterDirectory():

    def __init__(self, directory):
        assert os.path.isdir(directory)
        self.directory = directory
        self.working_directory = os.getcwd()

    def __enter__(self):
        os.chdir(self.directory)

    def __exit__(self, _exc_type, _exc_value, _traceback):
        os.chdir(self.working_directory)
