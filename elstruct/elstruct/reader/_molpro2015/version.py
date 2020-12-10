"""
Reads the program name and version number from the output file
"""

import autoparse.pattern as app
import autoparse.find as apf


def program_name(output_string):
    """ reads the program name (here: MainName + MainVersion)
    """
    prog_string = _get_prog_string(output_string)
    prog_name = prog_string.split(':')[1].strip()
    prog_name = prog_name.split('.')[0]
    prog_name = 'molpro' + prog_name

    return prog_name


def program_version(output_string):
    """ reads the program version number
    """
    prog_string = _get_prog_string(output_string)
    prog_version = prog_string.split(':')[1].strip()
    prog_version = prog_version.split('.')[1:]
    prog_version = '.'.join(prog_version)

    return prog_version


def _get_prog_string(output_string):
    """ obtains the string containing the version name and number
    """

    pattern = app.capturing(
                ('NAME' + app.SPACES + ':' + app.SPACES +
                 app.one_or_more(app.NONNEWLINE)))

    prog_string = apf.first_capture(pattern, output_string)

    return prog_string
