""" Runner
"""

import thermp_io.writer
from autorun._run import from_input_string


# Generalized runner
def direct(script_str, run_dir,
           pf_str, formula, hform0, temps,
           enthalpyt=0.0, breakt=1000.0):
    """ Generates an input file for a ThermP job runs it directly.
    """

    input_str = thermp_io.writer.input_file(
        ntemps=len(temps),
        formula=formula,
        delta_h=hform0,
        enthalpy_temp=enthalpyt,
        break_temp=breakt)
    aux_dct = {'pf.dat': pf_str}

    output_name = formula + '.i97'
    output_strs = from_input_string(
        script_str, run_dir, input_str,
        aux_dct=aux_dct,
        output_names=(output_name,))
    output_str = output_strs[0]

    return input_str, output_str
