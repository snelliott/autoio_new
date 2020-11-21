"""
Write various parts of a Chemkin mechanism file
"""

from chemkin_io.writer import reaction as writer
from chemkin_io.writer import _util as util
import numpy as np

def write_mech_file(elem_tuple, spc_dct, rxn_param_dct, filename='mech.txt',comments=''):
    """ Writes the Chemkin-formatted mechanism file. Writes
        the output to a text file.

        :param elem_tuple: tuple containing the element names
        :type elem_tuple: tuple
        :param spc_dct: dct containing the species data
        :type spc_dct: dct {spc_name:data}
        :param rxn_param_dct: dct containing the reaction parameters
        :type rxn_param_dct: dct {rxn:params}
    """
    elem_str = elements_block(elem_tuple)
    spc_str = species_block(spc_dct)
    rxn_str = reactions_block(rxn_param_dct,comments=comments)
    total_str = elem_str + spc_str + rxn_str

    # Write to a text file
    file = open(filename, "w")
    file.writelines(total_str)
    file.close()


def elements_block(elem_tuple):
    """ Writes the elements block of the mechanism file

        :param elem_tuple: tuple containing the element names
        :type elem_tuple: tuple
        :return elem_str: str containing the elements block
        :rtype: str
    """
    elem_str = 'ELEMENTS \n\n'
    for elem in elem_tuple:
        elem_str += elem + '\n'
    elem_str += '\nEND \n\n\n'

    return elem_str


def species_block(spc_dct):
    """ Writes the species block of the mechanism file

        :param spc_dct: dct containing the species data
        :type spc_dct: dct {spc_name:data}
        :return spc_str: str containing the species block
        :rtype: str
    """
    # Get the max species name length
    max_len = 0
    for spc_name in spc_dct.keys():
        if len(spc_name) > max_len:
            max_len = len(spc_name)

    buffer = 5

    # Write the spc_str
    spc_str = 'SPECIES \n\n'
    for spc_name, spc_data in spc_dct.items():
        spc_str += (
            '{0:<' + str(max_len+buffer) + 's}{1:>9s}{2:>9s}\n').format(
                spc_name, '! InChi: ', spc_data['inchi'])

    spc_str += '\nEND \n\n\n'

    return spc_str


def reactions_block(rxn_param_dct,ea_units='cal/mol',comments=''):
    """ Writes the reaction block of the mechanism file

        :param rxn_param_dct: dct containing the reaction parameters
        :type rxn_param_dct: dct {rxn:params}
        :return total_rxn_str: str containing the reaction block
        :rtype: str
    """
    # create empty dictionary with comments if empty
    if comments == '':
        comments = dict(zip(rxn_param_dct.keys(),np.zeros((len(rxn_param_dct),1))))

    # Get the length of the longest reaction name
    max_len = 0
    for rxn, param_dct in rxn_param_dct.items():
        rxn_name = util.format_rxn_name(rxn, param_dct)
        if len(rxn_name) > max_len:
            max_len = len(rxn_name)

    # Loop through each reaction and get the string to write to text file
    total_rxn_str = 'REACTIONS \n\n'
    for rxn, param_dct in rxn_param_dct.items():

        # Convert the reaction name from tuple of tuples to string
        # (Note: this includes '+M' or '(+M)' if appropriate)
        rxn_name = util.format_rxn_name(rxn, param_dct)

        if param_dct[3] is not None:  # Chebyshev
            assert param_dct[0] is not None, (
                f'For {rxn}, Chebyshev params included, highP params absent'
            )
            highp_params = param_dct[0]
            alpha = param_dct[3]['alpha_elm']
            tmin = param_dct[3]['t_limits'][0]
            tmax = param_dct[3]['t_limits'][1]
            pmin = param_dct[3]['p_limits'][0]
            pmax = param_dct[3]['p_limits'][1]
            rxn_str = writer.chebyshev(rxn_name, highp_params, alpha, 
                tmin, tmax, pmin, pmax)

        elif param_dct[4] is not None:  # PLOG
            assert param_dct[0] is not None, (
                f'For {rxn}, PLOG params included, highP params absent'
            )
            plog_dct = param_dct[4]
            highp_params = param_dct[0]
            rxn_str = writer.plog(
                rxn_name, highp_params, plog_dct,
                max_length=max_len, ea_units=ea_units)

        elif param_dct[2] is not None:  # Troe
            assert param_dct[0] is not None, (
                f'For {rxn}, Troe params included, highP params absent'
            )
            assert param_dct[1] is not None, (
                f'For {rxn}, Troe, highP params included, lowP params absent'
            )
            assert param_dct[6] is not None, (
                f'For {rxn}, Troe, highP, lowP params included, (+M) absent'
            )

            highp_params = param_dct[0]
            lowp_params = param_dct[1]
            troe_params = param_dct[2]
            collid_factors = param_dct[5]
            rxn_str = writer.troe(
                rxn_name, highp_params, lowp_params,
                troe_params, collid_factors,
                max_length=max_len, ea_units=ea_units)

        elif param_dct[1] is not None:  # Lindemann
            assert param_dct[0] is not None, (
                f'For {rxn}, lowP params included, highP params absent'
            )
            assert param_dct[6] is not None, (
                f'For {rxn}, highP, lowP params included, (+M) absent'
            )

            highp_params = param_dct[0]
            lowp_params = param_dct[1]
            collid_factors = param_dct[5]

            rxn_str = writer.lindemann(
                rxn_name, highp_params, lowp_params, collid_factors,
                max_length=max_len, ea_units=ea_units
            )

        else:  # Simple Arrhenius
            assert param_dct[0] is not None, (
                f'For {rxn}, the highP params absent'
            )

            highp_params = param_dct[0]
            rxn_str = writer.arrhenius(
                rxn_name, highp_params,
                max_length=max_len, ea_units=ea_units
            )

        # add inline comments on the first line
        if isinstance(comments[rxn],dict):
            if comments[rxn]['cmts_inline'] != '':
                rxn_str_split = rxn_str.split('\n')
                rxn_str_split[0] = rxn_str_split[0] + ' ' + comments[rxn]['cmts_inline'] 
                # rewrite rxn_str
                rxn_str = '\n'.join(rxn_str_split) + '\n'
    
        # check for comments: header
        if isinstance(comments[rxn],dict):
            total_rxn_str += comments[rxn]['cmts_top']

        total_rxn_str += rxn_str

    total_rxn_str += '\nEND \n'

    return total_rxn_str
