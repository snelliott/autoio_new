""" Combined thermo runners
"""

import automol.formula
import mess_io.reader
import thermp_io.reader
from autorun.thermp import direct as thermp_direct
from autorun.pac99 import nasa_polynomial


def direct(thermp_script_str, pac99_script_str, run_dir,
           pf_str, name, formula, hform0,
           enthalpyt=0.0, breakt=1000.0, convert=False):
    """ Runs ThermP and PAC99 together and parse out the results
    """

    # Obtain the temperatures from the pf.dat file used to fit the thermo
    temps, _, _, _ = mess_io.reader.pfs.partition_function(pf_str)
    temps = temps[:-1]

    # Run ThermP and read the Heat-of-Formation at 298K
    formula_str = automol.formula.string(formula)
    _, thermp_output_strs = thermp_direct(
        thermp_script_str, run_dir,
        pf_str, formula_str, hform0, temps,
        enthalpyt=enthalpyt, breakt=breakt)
    hform298 = thermp_io.reader.hf298k(thermp_output_strs[0])

    # Run PACC99 and obtain the polynomials
    nasa_poly = nasa_polynomial(
        pac99_script_str, run_dir, thermp_output_strs[1], name, formula,
        convert=convert)

    return hform298, nasa_poly
