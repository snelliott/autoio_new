"""
Writes strings containing the rate parameters
"""

# Define the buffer between the longest reaction name and the Arr params 
ALL_BUFFERS = 5

# Functions to write the parameters in the correct format
def troe(reaction, high_params, low_params, troe_params, colliders, ea_units='kcal/mol', max_length=45, buffer=ALL_BUFFERS):
    """ Write the string containing the Lindemann fitting parameters
        formatted for ChemKin input files.

        :param reaction: ChemKin formatted string with chemical equation
        :type reaction: str
        :param high_params: Arrhenius Fitting Parameters used for high-P
        :type high_params: list(float)
        :param low_params: Arrhenius Fitting Parameters used for low-P
        :type low_params: list(float)
        :param troe_params: Troe alpha, T3, T1, and T2 (T2 is optional) fitting parameters
        :type troe_params: list(float)
        :param colliders: names and collision enhancement factors for bath spc
        :type colliders: list((str, float))
        :return troe_str: ChemKin reaction string with Troe parameters
        :rtype: str
    """
    ea_factor = _check_ea_units(ea_units)  # get the Ea conversion factor

    assert len(high_params) == 3, (
        f'There are {len(high_params)} high-P params for {reaction}. Should be 3.'
        ) 
    assert len(low_params) == 3, (
        f'There are {len(low_params)} low-P params for {reaction}. Should be 3.'
        )
    assert len(troe_params) in (3, 4), (
        f'There are {len(troe_params)} Troe params for {reaction}. Should be 3 or 4.'
        )

    [high_a, high_n, high_ea] = high_params
    [low_a, low_n, low_ea] = low_params  
    [alpha, ts_3, ts_1, ts_2] = troe_params

    # Write reaction header and high-pressure params
    troe_str = ('{0:<' + str(max_length+buffer) + 's}{1:>10.3E}{2:>9.3f}{3:9.0f}\n').format(
        reaction, high_a, high_n, ea_factor * high_ea)

    # Write the LOW string
    troe_str += ('{0:>10s}{1:>' + str(max_length+buffer) + '.3E}{2:>9.3f}{3:9.0f}   /\n').format(
        'LOW  /', low_a, low_n, ea_factor * low_ea)

    # Write the TROE string
    if ts_2:  # if the T** parameter exists
        troe_str += ('{0:>10s}{1:>8.3f}{2:>12.3E}{3:>12.3E}{4:>12.3E} /\n').format(
            'TROE /', alpha, ts_3, ts_1, ts_2)
    else:
        troe_str += ('{0:>10s}{1:>8.3f}{2:>12.3E}{3:>12.3E}   /\n').format(
            'TROE /', alpha, ts_3, ts_1)        

    # Write the collider efficiencies string
    if colliders:
        troe_str += _format_collider_string(colliders)

    # # Now write the low-pressure and Troe params
    # troe_str += _format_params_string(
    #     'LOW', low_params, newline=True, val='exp')
    # troe_str += _format_params_string(
    #     'TROE', troe_params, newline=False, val='exp')

    return troe_str


def lindemann(reaction, high_params, low_params, colliders, ea_units='kcal/mol', max_length=45, buffer=ALL_BUFFERS):
    """ Write the string containing the Lindemann fitting parameters
        formatted for ChemKin input files

        :param reaction: ChemKin formatted string with chemical equation
        :type reaction: str
        :param high_params: Arrhenius Fitting Parameters used for high-P
        :type high_params: list(float)
        :param low_params: Arrhenius Fitting Parameters used for low-P
        :type low_params: list(float)
        :param colliders: names and collision enhancement factors for bath spc
        :type colliders: list((str, float))
        :param ea_units: units of the *input* Ea; either 'kcal/mol' or 'cal/mol'
        :type ea_units: str
        :return lind_str: Chemkin reaction string with Lindemann parameters, Ea in cal/mol
        :rtype: str
    """
    ea_factor = _check_ea_units(ea_units)  # get the Ea conversion factor
    [high_a, high_n, high_ea] = high_params
    [low_a, low_n, low_ea] = low_params    

    # Write reaction header and high-pressure params
    lind_str = ('{0:<' + str(max_length+buffer) + 's}{1:>10.3E}{2:>9.3f}{3:9.0f}\n').format(
        reaction, high_a, high_n, ea_factor * high_ea)

    # Write the LOW string
    lind_str += ('{0:>10s}{1:>' + str(max_length+buffer) + '.3E}{2:>9.3f}{3:9.0f}   /\n').format(
        'LOW  /', low_a, low_n, ea_factor * low_ea)

    # Write the collider efficiencies string
    if colliders:
        lind_str += _format_collider_string(colliders)

    return lind_str


def plog(reaction, high_params, plog_params_dct, ea_units='kcal/mol', max_length=45, buffer=ALL_BUFFERS, temp_dct=None, err_dct=None):
    """ Write the string containing the PLOG fitting parameters
        formatted for ChemKin input files.

        :param reaction: ChemKin formatted string with chemical equation
        :type reaction: str
        :param rate_params_dct: Arrhenius fitting parameters at each pressure
        :type rate_params_dct: dict[pressure: [rate params]]
        :param temp_dct: temperature ranges for fits at each pressure
        :type temp_dct: dict[pressure: [temps]]
        :param err_dct: mean and max ftting errors at each pressure
        :type err_dct: dict[pressure: [errs]]
        :return plog_str: ChemKin reaction string with PLOG parameters
        :rtype: str
    """
    ea_factor = _check_ea_units(ea_units)  # get the Ea conversion factor
    
    # Find nparams and ensure there are correct num in each dct entry
    double_plog_fit = False
    for pressure, params in plog_params_dct.items():
        assert len(params) in (3, 6), (
            f'In {reaction}, the length of the {pressure} entry is {len(params)}. It should be 3 or 6.'
            )
        if len(params) == 6:
           double_plog_fit = True

    # Add fake high pressure parameters if they are not in the dictionary
    double_highp_fit = False
    if not high_params: 
        high_params = [1.00, 0.00, 0.00]
    elif len(high_params) == 6:  # if high-P params are a double fit
        double_highp_fit = True 

    # Obtain a list of the pressures and sort from low to high pressure
    unsorted_pressures = plog_params_dct.keys()
    pressures = sorted(unsorted_pressures)

    # If the high-P rate is a single Arrhenius fit    
    if double_highp_fit:  
        
        [high_a1, high_n1, high_ea1, high_a2, high_n2, high_ea2] = high_params

        # Write the first set of high-P params
        plog_str = ('{0:<' + str(max_length+buffer) + 's}{1:>10.3E}{2:>9.3f}{3:9.0f}\n').format(
            reaction, high_a1, high_n1, ea_factor * high_ea1)
        plog_str += '    DUP \n'

        # Add the first set of PLOG params
        for pressure in pressures:
            plog_params = plog_params_dct[pressure]
            [a, n, ea,*other] = plog_params
            plog_str += ('{0:<' + str(max_length+buffer-10) + 's}{1:<10.3f}{2:>10.3E}{3:>9.3f}{4:9.0f} /\n').format(
                '    PLOG /', pressure, a, n, ea_factor * ea)

        # Add the second set of high-P params
        plog_str += ('{0:<' + str(max_length+buffer) + 's}{1:>10.3E}{2:>9.3f}{3:9.0f}\n').format(
            reaction, high_a2, high_n2, ea_factor * high_ea2)
        plog_str += '    DUP \n'
        
        # Add the second set of PLOG params
        if double_plog_fit:  # if one (or more) PLOG params contains a double fit
            for pressure in pressures:
                plog_params = plog_params_dct[pressure]
                if len(plog_params) == 6:  # if the params actually contain a double fit        
                    [*other, a, n, ea] = plog_params
                    plog_str += ('{0:<' + str(max_length+buffer-10) + 's}{1:<10.3f}{2:>10.3E}{3:>9.3f}{4:9.0f} /\n').format(
                        '    PLOG /', pressure, a, n, ea_factor * ea)
            
        else:  # if none of the PLOG params contains a double fit, add dummy fit at the highest P
            plog_str += ('{0:<' + str(max_length+buffer-10) + 's}{1:<10.3f}{2:>10.3E}{3:>9.3f}{4:9.0f} /\n').format(
                '    PLOG /', pressures[-1], 1, 0, 0)

    # If the high-P rate is a single Arrhenius fit
    else:
        
        [high_a, high_n, high_ea] = high_params

        # Write the high-P params
        plog_str = ('{0:<' + str(max_length+buffer) + 's}{1:>10.3E}{2:>9.3f}{3:9.0f}\n').format(
            reaction, high_a, high_n, ea_factor * high_ea)

        # Loop through the PLOG params
        for pressure in pressures:
            plog_params = plog_params_dct[pressure]
            [a, n, ea,*other] = plog_params
            plog_str += ('{0:<' + str(max_length+buffer-10) + 's}{1:<10.3f}{2:>10.3E}{3:>9.3f}{4:9.0f} /\n').format(
                '    PLOG /', pressure, a, n, ea_factor * ea)

            # If the params contain a double fit
            if len(plog_params) == 6:         
                [*other, a, n, ea] = plog_params
                plog_str += ('{0:<' + str(max_length+buffer-10) + 's}{1:<10.3f}{2:>10.3E}{3:>9.3f}{4:9.0f} /\n').format(
                    '    PLOG /', pressure, a, n, ea_factor * ea)

    return plog_str


def chebyshev(reaction, high_params, alpha, tmin, tmax, pmin, pmax):
    """ Write the string containing the Chebyshev fitting parameters
        formatted for ChemKin input files.

        :param reaction: ChemKin formatted string with chemical equation
        :type reaction: str
        :param high_params: Arrhenius Fitting Parameters used for high-P
        :type high_params: list(float)
        :param alpha: Chebyshev coefficient matrix
        :type alpha: numpy.ndarray
        :param tmin: minimum temperature Chebyshev model is defined
        :type tmin: float
        :param tmax: maximum temperature Chebyshev model is defined
        :type tmax: float
        :param pmin: minimum pressure Chebyshev model is defined
        :type pmin: float
        :return cheb_str: ChemKin reaction string with Chebyshev parameters
        :rtype: str
    """
    assert len(high_params) == 3
    # assert alpha mat is a 2d matrix

    [high_a, high_n, high_ea] = high_params

    # Write reaction header (with third body added) and high-pressure params
    reaction = _format_rxn_str_for_pdep(reaction, pressure='all')
    cheb_str = '{0:<32s}{1:>10.3E}{2:>9.3f}{3:9.0f} \n'.format(
        reaction, high_a, high_n, 1000*high_ea)

    # Write the temperature and pressure ranges
    cheb_str += _format_params_string(
        'TCHEB', (tmin, tmax), newline=True, val='float')
    cheb_str += _format_params_string(
        'PCHEB', (pmin, pmax), newline=True, val='float')

    # Write the dimensions of the alpha matrix
    nrows = len(alpha)
    ncols = len(alpha[0])
    cheb_str += '{0:>10s}/    {1:d} {2:d} /\n'.format('CHEB', nrows, ncols)

    # Write the parameters from the alpha matrix
    for idx, row in enumerate(alpha):
        newline = bool(idx+1 != nrows)
        cheb_str += _format_params_string('CHEB', row, newline=newline)

    return cheb_str


def arrhenius(reaction, high_params, ea_units='kcal/mol', max_length=45, buffer=ALL_BUFFERS):
    """ Write the string containing the Arrhenius fitting parameters
        formatted for ChemKin input files

        :param reaction: ChemKin formatted string with chemical equation
        :type reaction: str
        :param high_params: Arrhenius fitting parameters used for high-P
        :type high_params: list(float)
        :param ea_units: units of the *input* Ea; either 'kcal/mol' or 'cal/mol'
        :type ea_units: str
        :return arr_str: ChemKin reaction string with Lindemann parameters, Ea in cal/mol
        :rtype: str
    """
    assert len(high_params) in (3,6), (
        f'There are {len(high_params)} high-P params for {reaction}. Should be 3 or 6.'
        ) 
    ea_factor = _check_ea_units(ea_units)

        
    if len(high_params) == 3:  # single Arrhenius
        [high_a, high_n, high_ea] = high_params
        arr_str = ('{0:<' + str(max_length+buffer) + 's}{1:>10.3E}{2:>9.3f}{3:9.0f}\n').format(
            reaction, high_a, high_n, ea_factor * high_ea)

    else:  # double Arrhenius
        [high_a1, high_n1, high_ea1, high_a2, high_n2, high_ea2] = high_params
        arr_str = ('{0:<' + str(max_length+buffer) + 's}{1:>10.3E}{2:>9.3f}{3:9.0f}\n').format(
            reaction, high_a1, high_n1, ea_factor * high_ea1)
        arr_str += '    DUP \n'
        arr_str += ('{0:<' + str(max_length+buffer) + 's}{1:>10.3E}{2:>9.3f}{3:9.0f}\n').format(
            reaction, high_a2, high_n2, ea_factor * high_ea2)
        arr_str += '    DUP \n'

    return arr_str


# Various formatting functions
def fit_info(pressures, temp_dct, err_dct):
    """ Write the string detailing the temperature ranges and fitting errors
        associated with the rate-constant fits at each pressure.

        :param pressures: pressures the k(T,P)s were calculated at
        :type pressures: list(float)
        :param temp_dct: temperature ranges (K) fits were done at each pressure
        :type temp_dct: dict[pressure, [temp range]]
        :param err_dct: errors associated with the fits at each pressure
        :type err_dct: dict[pressure, [mean err, max err]]
        :return inf_str: string containing all of the fitting info
        :rtype: str
    """

    # Make temp, err dcts empty if fxn receives None; add 'high' to pressures
    temp_dct = temp_dct if temp_dct else {}
    err_dct = err_dct if err_dct else {}
    if 'high' in temp_dct or 'high' in err_dct:
        pressures += ['high']

    # Check the temp and err dcts have same presures as rate_dcts
    if temp_dct:
        assert set(pressures) == set(temp_dct.keys())
    err_dct = err_dct if err_dct else {}
    if err_dct:
        assert set(pressures) == set(err_dct.keys())

    # Write string showing the temp fit range and fit errors
    inf_str = '! Info Regarding Rate Constant Fits\n'
    for pressure in pressures:
        if temp_dct:
            [min_temp, max_temp] = temp_dct[pressure]
            temps_str = '{0:.0f}-{1:.0f} K'.format(
                min_temp, max_temp)
            temp_range_str = 'Temps: {0:>12s}, '.format(
                temps_str)
        else:
            temp_range_str = ''
        if err_dct:
            [mean_err, max_err] = err_dct[pressure]
            err_str = '{0:11s} {1:>5.1f}%,  {2:7s} {3:>5.1f}%'.format(
                'MeanAbsErr:', mean_err, 'MaxErr:', max_err)
        else:
            err_str = ''

        # Put together the who info string
        if pressure != 'high':
            pstr = '{0:<9.3f}'.format(pressure)
        else:
            pstr = '{0:<9s}'.format('High')
        inf_str += '! Pressure: {0} {1} {2}\n'.format(
            pstr, temp_range_str, err_str)

    return inf_str


# Various formatting functions
def _format_rxn_str_for_pdep(reaction, pressure='all'):
    """ Add the bath gas M species to the reaction string for
        pressure dependent reactions in the appropriate format.

        :param reaction: chemical equation for the reaction
        :type reaction: str
        :param pressure: signifies the level of pressure dependence
        :type pressure: str
        :return: three_body_reaction: chemical equation with M body
        :rtype: str
    """
    # Determine format of M string to be added to reaction string
    assert pressure in ('low', 'all')
    if pressure == 'all':
        m_str = ' (+M)'
    else:
        m_str = ' + M'

    # Add the M string to both sides of the reaction string
    [lhs, rhs] = reaction.split('=')
    three_body_reaction = lhs + m_str + ' = ' + rhs + m_str

    return three_body_reaction


def _format_collider_string(colliders):
    """ Write the string for the bath gas collider and their efficiencies
        for the Lindemann and Troe functional expressions:

        :param colliders: the {collider: efficiency} dct
        :type colliders: dct {str: float}
        :return: collider_str: Chemkin-format string with colliders and efficiencies
        :rtype: str
    """

    collider_str = '    '  # buffer
    collider_str += ''.join(
        ('{0:s} / {1:4.3f} /   '.format(collider, efficiency)
         for collider, efficiency in colliders.items()))
    collider_str += '\n'

    return collider_str


def _format_params_string(header, params, newline=False, val='exp'):
    """ Write a string containing fitting params used for several
        functional forms.

        :param header: name of functional form the parameters correspond to
        :type header: str
        :param params: fitting parameters
        :type params: list(float)
        :param newline: signals whether to add a newline
        :type newline: bool
        :return: params_str: string containing the parameters
        :rtype: str
    """
    
    assert val in ('exp', 'float')

    if val == 'exp':
        val_str = '{0:12.3E}'
    else:
        val_str = '{0:12.2f}'

    params_str = '{0:>10s}/ '.format(header.upper())
    params_str += ''.join((val_str.format(param) for param in params))
    params_str += ' /'
    if newline:
        params_str += '\n'

    return params_str

def _check_ea_units(ea_units):
    """ This functions sets the ea_conversion factor 
        and also checks that the units input by the 
        user are valid.
    """
    if ea_units == 'kcal/mol':
        ea_factor = 1000
    elif ea_units == 'cal/mol':
        ea_factor = 1
    else:
        raise InputError(f"The units for Ea must be either 'kcal/mol' or 'cal/mol' but were input as {ea_units}")
    
    return ea_factor


def _format_rxn_name(rxn_key, param_vals):
    """ Receives a rxn_key and the corresponding param_vals 
        from a rxn_param_dct and writes it to a string that 
        the above functions can handle. Adds +M or (+M) if
        applicable.
    """
    rcts = rxn_key[0]
    prds = rxn_key[1]

    # Convert to list if only one species
    if not isinstance(rcts, list):
        rcts = [rcts]
    if not isinstance(prds, list):
        prds = [prds]

    # Write the strings
    for idx, rct in enumerate(rcts):
        if idx == 0:
            rct_str = rct
        else:
            rct_str += ' + ' + rct
    for idx, prd in enumerate(prds):
        if idx == 0:
            prd_str = prd
        else:
            prd_str += ' + ' + prd
    
    # Add the +M or (+M) text if it is applicable
    if param_vals[6] is not None:
        rct_str += ' ' + param_vals[6]
        prd_str += ' ' + param_vals[6]
    
    rxn_name = rct_str + ' = ' + prd_str
    
    return rxn_name
