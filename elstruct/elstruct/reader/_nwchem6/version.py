"""
Reads the program name and version number from the output file
"""

import autoparse.pattern as app
import autoparse.find as apf


def program_name(output_string):
    """ reads the program name (here: MainName + MainVersion)
    """
    prog_string = _get_prog_string(output_string)
    num = prog_string.split()[-1]
    num = num.split('.')[0].strip()
    prog_name = prog_string.split('(')[1][:6]
    prog_name = prog_name.lower().strip()
    prog_name = prog_name + num

    return prog_name


def program_version(output_string):
    """ reads the program version number
    """
    prog_string = _get_prog_string(output_string)
    prog_version = prog_string.split()[-1].strip()

    return prog_version


def _get_prog_string(output_string):
    """ obtains the string containing the version name and number
    """

    pattern = app.capturing(
        'Northwest Computational Chemistry Package' + app.SPACE +
        app.escape('(NWChem)') + app.SPACE +
        app.DIGIT + '.' + app.DIGIT)

    prog_string = apf.first_capture(pattern, output_string)

    return prog_string
