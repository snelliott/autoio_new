""" Run INTDER code
"""

import intder_io
from autorun._run import from_input_string


INPUT_NAME = 'intder.inp'
OUTPUT_NAMES = ('intder.out',)


def direct(script_str, run_dir,
           geo, hess, zma=None,
           input_name=INPUT_NAME,
           output_names=OUTPUT_NAMES):
    """ Run INTDER
    """

    input_str = intder_io.writer.input_file(geo, zma=zma)
    hess_str = intder_io.writer.cart_hess_file(hess)
    aux_dct = {'file15': hess_str}

    output_strs = from_input_string(
        script_str, run_dir, input_str,
        aux_dct=aux_dct,
        input_name=input_name,
        output_names=output_names)

    return output_strs
