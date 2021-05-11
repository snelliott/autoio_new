""" Runner
"""

from autorun._run import from_input_string as from_istring


def direct(script_str, run_dir, input_str, pot_str):
    """ Lazy runner polyrate
    """

    aux_dct = {'input.fu40': pot_str}
    input_name = 'input.dat'
    output_name = 'poly.fu6'
    output_str = from_istring(
        script_str, run_dir, input_str,
        aux_dct=aux_dct,
        input_name=input_name,
        output_names=(output_name,))

    return input_str, output_str
