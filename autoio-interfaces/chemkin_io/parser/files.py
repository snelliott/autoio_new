""" Functions operating on input files
"""
import ioformat.pathtools as parser
from chemkin_io.parser import mechanism as parser_mech
from chemkin_io.parser import reaction as parser_rxn
from chemkin_io.parser import thermo as parser_thermo
from mechanalyzer.calculator import rates as calc_rates
from mechanalyzer.calculator import thermo as calc_thermo


def load_rxn_ktp_dcts_chemkin(mech_filenames, direc, temps, pressures):
    """ Read one or more Chemkin-formatted mechanisms files and calculate rates at the indicated
        pressures and temperatures. Return a list of rxn_ktp_dcts.

        :param mech_filenames: filenames containing Chemkin-formatted kinetics information
        :type mech_filenames: list [filename1, filename2, ...]
        :param direc: directory with file(s) (all files must be in the same directory)
        :type direc: str 
        :param temps: temperatures at which to do calculations (Kelvin)
        :type temps: list [float]
        :param pressures: pressures at which to do calculations (atm)
        :type pressures: list [float]
        :return rxn_ktp_dcts: list of rxn_ktp_dcts
        :rtype: list of dcts [rxn_ktp_dct1, rxn_ktp_dct2, ...]
    """ 
    rxn_ktp_dcts = []
    for mech_filename in mech_filenames:
        mech_str = parser.read_file(direc, mech_filename)
        ea_units, a_units = parser_mech.reaction_units(mech_str)
        rxn_block_str = parser_mech.reaction_block(mech_str)
        rxn_param_dct = parser_rxn.param_dct(rxn_block_str, ea_units, a_units)
        rxn_ktp_dct = calc_rates.eval_rxn_param_dct(rxn_param_dct, pressures, temps)
        rxn_ktp_dcts.append(rxn_ktp_dct)

    return rxn_ktp_dcts


def load_spc_therm_dcts_chemkin(thermo_filenames, direc, temps):
    """ Reads one or more Chemkin-formatted thermo files and calculates thermo at the indicated
        temperatures. Outputs a list of spc_therm_dcts.

        :param thermo_filenames: filenames containing Chemkin-formatted thermo information
        :type thermo_filenames: list [filename1, filename2, ...]
        :param direc: directory with file(s) (all files must be in the same directory)
        :type direc: str
        :param temps: temperatures at which to do calculations (Kelvin)
        :type temps: list [float]
        :return spc_therm_dcts: list of spc_therm_dcts
        :rtype: list of dcts [spc_therm_dct1, spc_therm_dct2, ...]
    """
    spc_therm_dcts = []
    for thermo_filename in thermo_filenames:
        thermo_str = parser.read_file(direc, thermo_filename)
        thermo_block_str = parser_mech.thermo_block(thermo_str)
        spc_nasa7_dct = parser_thermo.create_spc_nasa7_dct(thermo_block_str)
        spc_therm_dct = calc_thermo.create_spc_therm_dct(spc_nasa7_dct, temps)
        spc_therm_dcts.append(spc_therm_dct)

    return spc_therm_dcts

