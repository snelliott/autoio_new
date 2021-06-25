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
                      aux_dct=None,
                      script_name=SCRIPT_NAME,
                      input_name=INPUT_NAME,
                      output_names=(OUTPUT_NAME,)):
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

    write_input(run_dir, input_str, aux_dct=aux_dct, input_name=input_name)
    run_script(script_str, run_dir, script_name=script_name)
    output_strs = read_output(run_dir, output_names=output_names)

    return output_strs


def from_parallel_input_strings(script_str, run_dir, input_strs,
                                aux_dct=None,
                                script_name=SCRIPT_NAME,
                                input_name=INPUT_NAME,
                                output_names=(OUTPUT_NAME,)):
    """ Runs a bunch of processes in parallel with following structure
            run_dir/run1
                    run2
                    run3
                    run.sh

        where run[n] contains the input files for several instances
        of the same program (assuming aux_dct files same for each run)
        and run.sh executes all of the instances in the run[n] directories.

        Output from all instances are returned in a list.

        *PROB WANT TO FIND A BETTER WAY TO WRITE SCRIPT STRING INTERNALLY

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

    # Build the run dirs
    if not os.path.exists(run_dir):
        os.makedirs(run_dir)

    # Set and build the sub rub run dis list
    sub_run_dirs = ()
    for run_idx, input_str in enumerate(input_strs):
        sub_run_name = 'run{}'.format(run_idx+1)
        sub_run_dir = os.path.join(run_dir, sub_run_name)
        if not os.path.exists(sub_run_dir):
            os.makedirs(sub_run_dir)
        sub_run_dirs += (sub_run_dir,)

    # Write the inputs in each sub run dir
    for sub_run_dir, input_str in zip(sub_run_dirs, input_strs):
        write_input(sub_run_dir, input_str,
                    aux_dct=aux_dct, input_name=input_name)

    # Run the central script which launches all processes from run dir
    run_script(script_str, run_dir, script_name=script_name)

    # Read all of the outputs from all processes
    output_strs_lst = ()
    for sub_run_dir in sub_run_dirs:
        output_strs = read_output(sub_run_dir, output_names=output_names)
        output_strs_lst += (output_strs,)

    return output_strs_lst


def write_input(run_dir, input_str,
                aux_dct=None,
                input_name=INPUT_NAME):
    """ write the input
    """

    if not os.path.exists(run_dir):
        os.makedirs(run_dir)

    with EnterDirectory(run_dir):

        # Write the main input file
        with open(input_name, 'w') as input_obj:
            input_obj.write(input_str)

        # Write all auxiliary input files
        if aux_dct is not None:
            for fname, fstring in aux_dct.items():
                if fstring:
                    with open(fname, 'w') as aux_obj:
                        aux_obj.write(fstring)


def read_output(run_dir, output_names=(OUTPUT_NAME,)):
    """ Read the output string from the run directory
    """

    with EnterDirectory(run_dir):

        output_strs = ()
        for output_name in output_names:
            if os.path.exists(output_name):
                if os.path.isfile(output_name):
                    with open(output_name, 'r') as output_obj:
                        output_str = output_obj.read()
                else:
                    output_str = None
            else:
                output_str = None
            output_strs += (output_str,)

    return output_strs


def run_script(script_str, run_dir, script_name=SCRIPT_NAME):
    """ run a program from a script
    """

    with EnterDirectory(run_dir):

        # Write the submit script to the run directory
        with open(script_name, 'w') as script_obj:
            script_obj.write(script_str)

        # Make the script executable
        os.chmod(
            script_name,
            mode=(os.stat(script_name).st_mode |
                  stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))

        # Call the program
        try:
            subprocess.check_call('./{:s}'.format(script_name))
        except subprocess.CalledProcessError:
            warnings.warn("Program run failed in {}".format(run_dir))
        # except subprocess.CalledProcessError as err:
            # As long as the program wrote an output, continue with a warning
            # if all(os.path.isfile(name) for name in output_names):
            #     warnings.warn("Program run failed in {}".format(run_dir))
            # else:
            #     raise err


class EnterDirectory():
    """ Handles the entrance and exit of some directory.
    """

    def __init__(self, directory):
        assert os.path.isdir(directory), (
            '{} is not a directory'.format(directory)
        )
        self.directory = directory
        self.working_directory = os.getcwd()

    def __enter__(self):
        os.chdir(self.directory)

    def __exit__(self, _exc_type, _exc_value, _traceback):
        os.chdir(self.working_directory)
