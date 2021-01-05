"""
Reads the program name and version number from the output file
"""

import autoparse.pattern as app
import autoparse.find as apf


def program_name(output_str):
    """ Reads the program name from the output file string.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: str
    """

    prog_string = _get_prog_string(output_str)
    prog_name = prog_string.split(':')[1].strip()
    prog_name = prog_name.split('.')[0]
    prog_name = 'molpro' + prog_name

    return prog_name


def program_version(output_str):
    """ Reads the program version number from the output file string.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: str
    """

    prog_string = _get_prog_string(output_str)
    prog_version = prog_string.split(':')[1].strip()
    prog_version = prog_version.split('.')[1:]
    prog_version = '.'.join(prog_version)

    return prog_version


def _get_prog_string(output_str):
    """ Parses out the program information from the output file string.

        :param output_str: string of the program's output file
        :type output_str: str
        :rtype: str
    """

    pattern = app.capturing(
                ('NAME' + app.SPACES + ':' + app.SPACES +
                 app.one_or_more(app.NONNEWLINE)))

    prog_string = apf.first_capture(pattern, output_str)

    return prog_string
