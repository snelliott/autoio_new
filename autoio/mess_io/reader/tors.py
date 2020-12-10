"""
Reads the outoput of a MESSPF calculation for the
frequencies and ZPEs for torsional modes

Right now, we assume only a single species is in the output
"""

import autoparse.pattern as app
import autoparse.find as apf


def analytic_freqs(output_string):
    """ Reads the analytic frequencies for each of the
        hindered rotors from MESS output file string. 

        Frequency corresponds to the minimum from a Fourier fit to 
        the user supplied hindered rotor potential in the input.

        :param output_string: string of lines of MESS output file
        :type output_string: str
        :return freqs: frequency for each of the rotors
        :rtype: list(float)
    """

    # Pattern for the frequency of a rotor
    pattern = (app.escape('analytic  frequency at minimum[1/cm] =') +
               app.one_or_more(app.SPACE) +
               app.capturing(app.NUMBER))

    # Obtain each frequency from the output string
    tors_freqs = [float(val)
                  for val in apf.all_captures(pattern, output_string)]

    return tors_freqs


def grid_min_freqs(output_string):
    """ Reads the analytic frequencies for each of the
        hindered rotors from MESS output file string.

        Frequency corresponds to the minimum from the minimum on the grid
        of the user supplied hindered rotor potential in the input.

        :param output_string: string of lines of MESS output file
        :type output_string: str
        :return freqs: frequency for each of the rotors
        :rtype: list(float)
    """

    # Pattern for the frequency of a rotor
    pattern = (app.escape('first point frequency estimate =') +
               app.one_or_more(app.SPACE) +
               app.capturing(app.NUMBER) + 
               app.one_or_more(app.SPACE) +
               app.escape('1/cm'))

    # Obtain each frequency from the output string
    tors_freqs = [float(val)
                  for val in apf.all_captures(pattern, output_string)]

    print('tors freqs test in grid_min_freq:', tors_freqs)

    return tors_freqs


def zpves(output_string):
    """ Reads the zero-point energies for each of the
        hindered rotors from MESS output file string.

        :param output_string: string of lines of MESS output file
        :type output_string: str
        :return zpves: zero-point energy for each of the rotors
        :rtype: list(float)
    """

    # Patterns for the ZPVE of a rotor
    num_patterns = (app.EXPONENTIAL_FLOAT, app.FLOAT)
    pattern1 = (app.escape('minimum energy[kcal/mol]') +
                app.one_or_more(app.SPACE) +
                '=' +
                app.one_or_more(app.SPACE) +
                app.capturing(app.one_of_these(num_patterns)))

    pattern2 = (app.escape('ground energy [kcal/mol]') +
                app.one_or_more(app.SPACE) +
                '=' +
                app.one_or_more(app.SPACE) +
                app.capturing(app.one_of_these(num_patterns)))

    # Obtain each ZPVE from the output string
    tmp1 = [-float(val)
            for val in apf.all_captures(pattern1, output_string)]
    tmp2 = [float(val)
            for val in apf.all_captures(pattern2, output_string)]
    tors_zpes = [sum(tmp) for tmp in zip(tmp1, tmp2)]
    # print('tors_zpes calc test:', tmp1, tmp2, tors_zpes)

    return tors_zpes
