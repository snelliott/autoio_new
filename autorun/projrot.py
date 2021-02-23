"""
  Get frequencies
"""

import projrot_io.writer
from autorun._run import from_input_string


INPUT_NAME = 'RPHt_input_data.dat'
OUTPUT_NAMES = (
        'RTproj_freq.dat',
        'hrproj_freq.dat',
        'RTproj_cd.dat',
        'hrproj_cd.dat',
        'imactint.dat'
)


# Specialized Runners
def frequencies(script_str, run_dir, geoms, grads, hessians,
                rotors_str='', aux_dct=None):
    """ Make frequencies
    """

    output_strs = direct(
        script_str, run_dir, geoms, grads, hessians,
        rotors_str=rotors_str, aux_dct=aux_dct)

    rtproj_str = output_strs[0]
    if rtproj_str is not None:
        rtproj_freqs, rt_imag_freq = projrot_io.reader.rpht_output(
            rtproj_str)
    hrproj_str = output_strs[1]
    if hrproj_str is not None:
        hrproj_freqs, hr_imag_freq = projrot_io.reader.rpht_output(
            hrproj_str)

    return rtproj_freqs, hrproj_freqs, rt_imag_freq, hr_imag_freq


# Generalized Runner
def direct(script_str, run_dir, geoms, grads, hessians,
           rotors_str='', aux_dct=None,
           input_name=INPUT_NAME, output_names=OUTPUT_NAMES):
    """ Generates an input file for a ProjRot job, runs it directly, and
        obtains all of the possible output
    """

    input_str = projrot_io.writer.rpht_input(
        geoms, grads, hessians, rotors_str=rotors_str)

    output_strs = from_input_string(
        script_str, run_dir, input_str,
        aux_dct=aux_dct,
        input_name=input_name,
        output_names=output_names)

    return output_strs
