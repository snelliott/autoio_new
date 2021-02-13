""" Format things
"""

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
        from a rxn_param_dct and writes it to a string that
        the above functions can handle. Adds +M or (+M) if
        applicable.
    """
    rcts = rxn_key[0]
    prds = rxn_key[1]

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
    if param_vals[6] is not None:
        rct_str += param_vals[6]
        prd_str += param_vals[6]
    elif param_vals[3] is not None:
        # cheb writer if cheb params is not there
        rct_str += '(+M)'
        prd_str += '(+M)'
        
    rxn_name = rct_str + '=' + prd_str

    return rxn_name


def format_rxn_name_luna(rxn_key, param_vals):
    """ Receives a rxn_key and the corresponding param_vals 
        from a rxn_param_dct and writes it to a string that 
        the above functions can handle. Adds +M or (+M) if
        applicable.
    """
    rcts = rxn_key[0]
    prds = rxn_key[1]

    # write strings
    if len(rcts) == 1:
        # 1 species
        rct_str = rcts[0]
    elif len(rcts) == 2:
        # 2 species
        rct_str = rcts[0] + '+' + rcts[1]

    if len(prds) == 1:
        prd_str = prds[0]
    elif len(prds) >= 2:
        prd_str = '+'.join(list(prds))

    # Add the +M or (+M) text if it is applicable
    if param_vals[6] is not None:
        rct_str += ' ' + param_vals[6]
        prd_str += ' ' + param_vals[6]

    rxn_name = rct_str + ' = ' + prd_str

    return rxn_name
