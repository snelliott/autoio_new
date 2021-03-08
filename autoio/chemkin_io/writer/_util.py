""" Format utilities
"""
import numpy as np

CKIN_TRANS_HEADER_STR = """! THEORETICAL TRANSPORT PROPERTIES
!
! (1) Shape, index denotes atom (0), linear molec. (1), nonlinear molec. (2);
! (2) Epsilon, the Lennard-Jones well depth, in K;
! (3) Sigma, the Lennard-Jones collision diameter, in Angstrom;
! (4) Mu, total dipole moment, in Debye;
! (5) Alpha, mean static polarizability, in Angstrom^3; and
! (6) Z_rot, rotational relaxation collision number at 298 K."""


def name_column_length(names):
    """ Set the width of the name column
    """

    maxlen = 0
    for name in names:
        maxlen = max(maxlen, len(name))
    if maxlen <= 9:
        maxlen = 9
    names_len = str(maxlen + 3)

    return names_len


def format_rxn_name(rxn_key, param_vals):
    """ Receives a rxn_key and the corresponding param_vals
        from a rxn_param_dct and writes an appropriate string
        to be written in a CHEMKIN mech. Adds third body if applicable

        :params rxn_key: reaction names and third body
        :type rxn_key: tuple ((rct1,rct2),(prd1,prd2),(thirdbody))
        :params param_vals: one set of parameters of the reaction
        :type param_vals: tuple(dct)
        :return rxn_name: formatted reaction name for writing in the mech
        :rtype: str
    """
    rcts = rxn_key[0]
    prds = rxn_key[1]
    thrbdy = rxn_key[2][0]

    # Convert to list if only one species
    if not isinstance(rcts, tuple):
        rcts = [rcts]
    if not isinstance(prds, tuple):
        prds = [prds]

    # Write the strings
    for idx, rct in enumerate(rcts):
        if idx == 0:
            rct_str = rct
        else:
            rct_str += '+' + rct
    for idx, prd in enumerate(prds):
        if idx == 0:
            prd_str = prd
        else:
            prd_str += '+' + prd

    # Add the +M or (+M) text if it is applicable
    if thrbdy is not None:
        rct_str += thrbdy
        prd_str += thrbdy
    elif param_vals[3] is not None:
        # cheb writer if cheb params is not there
        rct_str += '(+M)'
        prd_str += '(+M)'

    rxn_name = rct_str + '=' + prd_str

    return rxn_name


def merge_plog_dct(param_dct):
    """ Merge 2 or more duplicate PLOG dictionaries

        :param_dct: values of one rxn_param_dct
        :type tuple(tuple)
        :return param_dct
        :rtype tuple(tuple)
    """
    # extract plog dictionaries
    plog = np.array(
        [param_dct_vals[4] is not None for param_dct_vals in param_dct], dtype=int)
    mask_nonplog = np.where(plog == 0)[0]
    mask_plog = np.where(plog == 1)[0]
    if len(mask_plog) > 1:  # more than 1 set of plog params
        # merge dictionaries together or add entries
        plog_param_dct = [list(param_dct[i]) for i in mask_plog]
        merged_plog_dct = plog_param_dct[0]
        # new dictionary
        for plog_param_dct_i in plog_param_dct[1:]:
            # extend the plog values with the other parameters
            for key_i, plog_params in plog_param_dct_i[4].items():
                try:
                    merged_plog_dct[4][key_i].extend(plog_params)
                except KeyError:
                    merged_plog_dct[4][key_i] = plog_params

        # build new dct
        merged_plog_dct = [tuple(merged_plog_dct)]

        if len(mask_nonplog) > 0:
            nonplog_param_dct = [param_dct[i] for i in mask_nonplog]
            merged_plog_dct.extend(nonplog_param_dct)
        param_dct = tuple(merged_plog_dct)

    return param_dct


def merge_plog_dct(param_dct):
    """ Merge 2 or more duplicate PLOG dictionaries

        :param_dct: values of one rxn_param_dct
        :type tuple(tuple)
        :return param_dct
        :rtype tuple(tuple)
    """
    # extract plog dictionaries
    plog = np.array(
        [param_dct_vals[4] is not None for param_dct_vals in param_dct], dtype=int)
    mask_nonplog = np.where(plog == 0)[0]
    mask_plog = np.where(plog == 1)[0]
    if len(mask_plog) > 1:  # more than 1 set of plog params
        # list with all not-none parac_dct_vals[4]
        plog_param_dct = [list(param_dct[i]) for i in mask_plog]
        keys_list = [list(plog_param_dct_i[4].keys())
                     for plog_param_dct_i in plog_param_dct]
        unique_keys_list = []
        # if they share the same keys: join them together
        if all(keys_i == keys_list[0] for keys_i in keys_list):
            # new dictionary
            merged_plog_dct = plog_param_dct[0]
            # extend the plog values with the other parameters
            for key_i in keys_list[0]:
                for idx in range(1, len(mask_plog)):
                    merged_plog_dct[4][key_i].extend(
                        plog_param_dct[idx][4][key_i])
            # build new dct
            merged_plog_dct = [tuple(merged_plog_dct)]

            if len(mask_nonplog) > 0:
                nonplog_param_dct = [param_dct[i] for i in mask_nonplog]
                merged_plog_dct.extend(nonplog_param_dct)
            param_dct = tuple(merged_plog_dct)
    return param_dct
