""" a simple helper command for running a given program
"""
import os
import tempfile
import subprocess


def run(argv, input_str, input_name='input.dat', output_name='output.dat'):
    """ run the program in a temporary directory and return the output
    """
    tmp_dir = tempfile.mkdtemp()
    input_path = os.path.join(tmp_dir, input_name)
    output_path = os.path.join(tmp_dir, output_name)

    # write the input string to the run directory
    with open(input_path, 'w') as input_obj:
        input_obj.write(input_str)

    # call the electronic structure program
    subprocess.check_call(argv, cwd=tmp_dir)

    # read the output string from the run directory
    with open(output_path, 'r') as output_obj:
        output_str = output_obj.read()

    return output_str, tmp_dir
