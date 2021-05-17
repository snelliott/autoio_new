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


def format_rxn_name(rxn):
    """ Receives a rxn and creates an appropriate string
        to be written in a Chemkin mech. Adds third body if applicable

        :param rxn: reaction names and third body
        :type rxn: tuple ((rct1, rct2), (prd1, prd2), (third_bod1,))
        :return rxn_name: formatted reaction name for writing in the mech
        :rtype: str
    """
    rcts = rxn[0]
    prds = rxn[1]
    thrbdy = rxn[2][0]

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

    try:
        plog = np.array(
            [param_dct_vals[4] is not None for param_dct_vals in param_dct],
            dtype=int)
        mask_nonplog = np.where(plog == 0)[0]
        mask_plog = np.where(plog == 1)[0]
    except TypeError:
        # if for any reason the dct does not have iterables
        mask_plog = []

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
