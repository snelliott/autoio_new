""" MESS
"""

import mess_io.writer
from autorun._run import from_input_string


INPUT_NAME = 'mess.inp'
OUTPUT_NAMES = ('rate.out', 'mess.aux', 'mess.log')


# Specilialized runners
def torsions(script_str, run_dir, geo, hind_rot_str):
    """ Calculate the frequencies and ZPVES of the hindered rotors
        create a messpf input and run messpf to get tors_freqs and tors_zpes
    """

    # Write the MESSPF input file
    input_str = mess_io.writer.messhr_inp_str(geo, hind_rot_str)

    # Run the direct function
    input_name = 'pf.inp'
    output_name = 'pf.log'
    output_strs = direct(script_str, run_dir, input_str,
                         aux_dct=None,
                         input_name=input_name,
                         output_names=(output_name,))
    output_str = output_strs[0]

    # Read the torsional freqs and zpves
    tors_freqs = mess_io.reader.tors.analytic_frequencies(output_str)
    # tors_freqs = mess_io.reader.tors.grid_minimum_frequencies(output_str)
    tors_zpes = mess_io.reader.tors.zero_point_vibrational_energies(
        output_str)

    return tors_freqs, tors_zpes


def direct(script_str, run_dir, input_str, aux_dct=None,
           input_name=INPUT_NAME,
           output_names=OUTPUT_NAMES):
    """
        :param aux_dct: auxiliary input strings dict[name: string]
        :type aux_dct: dict[str: str]
        :param script_str: string of bash script that contains
            execution instructions electronic structure job
        :type script_str: str
        :param run_dir: name of directory to run electronic structure job
        :type run_dir: str
    """

    output_strs = from_input_string(
        script_str, run_dir, input_str,
        aux_dct=aux_dct,
        input_name=input_name,
        output_names=output_names)

    return output_strs
