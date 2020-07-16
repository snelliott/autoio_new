"""
Obtain information from VPT2 calculations
"""

from qcelemental import constants as qcc
import autoread as ar
import autoparse.pattern as app
import autoparse.find as apf


KJ2EH = qcc.conversion_factor('kJ/mol', 'hartree')


def anharmonic_frequencies_reader(output_string):
    """ Get the anharmonic vibrational frequencies
    """

    # block
    block = apf.last_capture(
        (app.escape('Fundamental Bands (DE w.r.t. Ground State)') +
         app.capturing(app.one_or_more(app.WILDCARD, greedy=False)) +
         app.escape('Overtones (DE w.r.t. Ground State)')), output_string)

    pattern = (
        app.INTEGER +
        app.escape('(1)') +
        app.SPACE +
        app.maybe(app.one_or_more(app.LOWERCASE_LETTER)) +
        app.one_or_more(app.SPACE) +
        app.FLOAT +
        app.one_or_more(app.SPACE) +
        app.capturing(app.FLOAT)
    )
    # pattern2 = (
        # app.INTEGER +
        # app.escape('(1)') +
        # app.SPACE +
        # app.maybe(app.one_or_more(app.LOWERCASE_LETTER)) +
        # app.one_or_more(app.SPACE) +
        # app.FLOAT +
        # app.one_or_more(app.SPACE) +
        # app.capturing(app.FLOAT) +
        # app.one_or_more(app.SPACE) +
        # app.one_or_more(app.escape('*')) +
        # app.one_or_more(app.SPACE) +
        # app.one_or_more(app.escape('*')) +
        # app.one_or_more(app.SPACE) +
        # app.FLOAT
    # )

    # Get list of values
    anharm_freq = [float(val)
                   for val in apf.all_captures(pattern, block)]
    # if not anharm_freq:
        # anharm_freq = [float(val)
                       # for val in apf.all_captures(pattern2, block)]

    return sorted(anharm_freq)


def anharm_zpve_reader(output_string):
    """ Get the anharmonic ZPVE
    """

    anharm_zpve_pattern = (
        'Total Anharm' +
        app.one_or_more(app.SPACE) +
        ':' +
        app.SPACE +
        'cm-1' +
        app.SPACE +
        '=' +
        app.one_or_more(app.SPACE) +
        app.FLOAT +
        app.SPACE +
        ';' +
        app.SPACE +
        'Kcal/mol' +
        app.SPACE +
        '=' +
        app.one_or_more(app.SPACE) +
        app.FLOAT +
        app.SPACE +
        ';' +
        app.SPACE +
        'KJ/mol' +
        app.SPACE +
        '=' +
        app.one_or_more(app.SPACE) +
        app.capturing(app.FLOAT)
    )

    # Set the string pattern containing the anharm ZPVE
    # anharm_zpve_pattern = (
    #     app.escape('ZPE(harm) = ') +
    #     app.EXPONENTIAL_FLOAT_D +
    #     app.one_or_more(app.SPACE) +
    #     'kJ/mol' +
    #     app.one_or_more(app.SPACE) +
    #     app.escape('ZPE(anh)=') +
    #     app.one_or_more(app.SPACE) +
    #     app.capturing(app.EXPONENTIAL_FLOAT_D) +
    #     app.one_or_more(app.SPACE) +
    #     'kJ/mol'
    # )

    # Retrieve the anharm ZPVE
    anh_zpve = apf.last_capture(anharm_zpve_pattern, output_string)

    # Format the ZPVE
    anh_zpve = float(anh_zpve.replace('D', 'E'))
    anh_zpve *= KJ2EH

    return anh_zpve


def anharmonicity_matrix_reader(output_string):
    """ Get the Anharmonicity Matrix
    """

    # Set strings to find anharm matrix
    start_string = 'Total Anharmonic X Matrix (in cm^-1)'
    comp_ptt = app.UNSIGNED_INTEGER

    # Obtain the matrix
    mat = ar.matrix.read(
        output_string,
        val_ptt=app.EXPONENTIAL_FLOAT_D,
        start_ptt=app.padded(app.NEWLINE).join([
            app.padded(app.escape(start_string), app.NONNEWLINE),
            app.LINE, '']),
        block_start_ptt=(app.series(comp_ptt, app.LINESPACES) +
                         app.padded(app.NEWLINE)),
        line_start_ptt=comp_ptt,
        tril=True)
    mat = tuple([tuple([float(val.replace('D', 'E')) for val in row])
                 for row in mat])

    return mat


def vibro_rot_alpha_matrix_reader(output_string):
    """ Get the Vibration-Rotation Alpha Matrix
    """

    begin_string = 'Vibro-Rot alpha Matrix (in cm^-1)'
    end_string = app.escape('Q( ') + app.UNSIGNED_INTEGER + app.escape(')')

    vib_rot_mat = ar.matrix.read(
        output_string,
        start_ptt=app.padded(app.NEWLINE).join([
            app.padded(app.escape(begin_string), app.NONNEWLINE),
            app.LINE, app.LINE, '']),
        line_start_ptt=end_string)

    return vib_rot_mat


def cent_dist_const_reader(output_string):
    """ Get the quartic centrifugal distortion constants
    """

    # block
    block = apf.last_capture(
        ('Quartic Centrifugal Distortion Constants Tau Prime' +
         app.capturing(app.one_or_more(app.WILDCARD, greedy=False)) +
         'Asymmetric Top Reduction'),
        output_string)
    if not block:
        block = apf.last_capture(
            ('Quartic Centrifugal Distortion Constants Tau Prime' +
             app.capturing(app.one_or_more(app.WILDCARD, greedy=False)) +
             'Constants in the Symmetrically Reduced Hamiltonian'),
            output_string)
    if not block:
        block = apf.last_capture(
            ('Quartic Centrifugal Distortion Constants Tau Prime' +
             app.capturing(app.one_or_more(app.WILDCARD, greedy=False)) +
             'Rotational l-type doubling constants'),
            output_string)

    # pattern
    pattern = (
        'TauP' +
        app.SPACE +
        app.capturing(app.one_or_more(app.LOWERCASE_LETTER)) +
        app.SPACES +
        app.capturing(app.EXPONENTIAL_FLOAT_D) +
        app.SPACES +
        app.EXPONENTIAL_FLOAT_D
    )

    # Get list of values
    cent_dist_const = [[lbl, float(val.replace('D', 'E'))]
                       for (lbl, val) in apf.all_captures(pattern, block)]

    return cent_dist_const


def vpt2(output_string):
    """ read various pieces of anharm data from output string
    """

    # Initialize dictionary to store information dictionary
    anharm_dict = {
        'freqs': anharmonic_frequencies_reader(output_string),
        'zpve': anharm_zpve_reader(output_string),
        'x_mat': anharmonicity_matrix_reader(output_string),
        'vibrot_mat': vibro_rot_alpha_matrix_reader(output_string),
        'cent_dist_const': cent_dist_const_reader(output_string)
    }

    return anharm_dict
