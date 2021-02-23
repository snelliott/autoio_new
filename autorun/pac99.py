""" Runners for PAC99 program
"""

import subprocess
import pac99_io.reader
import thermp_io.reader
from autorun.thermp import direct as thermp_direct
from autorun._run import EnterDirectory


# Read the new groups file stored with src
NEW_GROUPS_NAME = 'new.groups'
NEW_GROUPS_STR = ''


# Specialized runner
def thermo(script_str, run_dir,
           pf_str, formula, hform0, temps,
           enthalpyt=0.0, breakt=1000.0, convert=False):
    """ calc thermo
    """

    # Run ThermP and read the Heat-of-Formation at 298K
    _, thermp_out_str = thermp_direct(
        script_str, run_dir,
        pf_str, formula, hform0, temps,
        enthalpyt=enthalpyt, breakt=breakt)
    hform298 = thermp_io.reader.hf298k(thermp_out_str)

    # Run PACC99 and obtain the polynomials
    nasa_poly = nasa_polynomial(
        run_dir, input_str, name, formula_dct, convert=convert)

    return hform298, nasa_poly


def nasa_polynomial(run_dir, input_str, name, formula_dct, convert=False):
    """ Generates NASA polynomial from run

        :param convert: convert the polynomial to more standard CHEMKIN
        :type convert
    """

    # Run PAC99 to get the output file
    output_str = direct(run_dir, input_str, formula)

    # Obtain the NASA polynomial, convert if necessary
    if output_str is not None:
        poly_str = pac99_io.reader.nasa_polynomial(output_str)
        if convert:
            poly_str = pac99_io.pac2ckin_poly(name, formula_dct, poly_str)
    else:
        poly_str = None

    return poly_str


# Generalized runners
def direct(run_dir, input_str, formula):
    """ Generates an input file for a ThermP job runs it directly.

        Need formula input to run the script
        :param input_str: string of input file with .i97 suffix
    """

    output_str = _pac99_from_input_string(
        run_dir, input_str, formula)

    return input_str, output_str


def _pac99_from_input_string(run_dir, input_str, formula):
    """
    Run pac99 for a given species name (formula)
    https://www.grc.nasa.gov/WWW/CEAWeb/readme_pac99.htm
    requires formula+'i97' and new.groups files
    """

    # Write the input string to the run directory
    with EnterDirectory(run_dir):

        # Write the input string to the run directory
        input_name = formula+'.i97'
        with open(input_name, 'w') as input_obj:
            input_obj.write(input_str)

        # Write the new groups file to
        with open(NEW_GROUPS_NAME, 'w') as new_grps_obj:
            new_grps_obj.write(NEW_GROUPS_STR)

        # Run pac99
        proc = subprocess.Popen('pac99', stdin=subprocess.PIPE)
        proc.communicate(bytes(formula, 'utf-8'))

        # Open output files and check them
        o97_output_name = formula+'.o97'
        with open(o97_output_name, 'r') as o97_output_obj:
            o97_output_str = o97_output_obj.read()

        c97_output_name = formula+'.c97'
        with open(c97_output_name, 'r') as c97_output_obj:
            c97_output_str = c97_output_obj.read()

        if _check(o97_output_str, c97_output_str):
            output_str = o97_output_str
        else:
            output_str = None

    return output_str


def _check(o97_output_str, c97_output_str):
    """ assess the output (.o97, .c97 fileS)
    """

    success = True
    if 'INSUFFICIENT DATA' in o97_output_str:
        print('*ERROR: PAC99 fit failed, maybe increase temperature ranges?')
        success = False

    if not c97_output_str:
        print('No polynomial produced from PAC99 fits, check for errors')
        success = False

    return success
