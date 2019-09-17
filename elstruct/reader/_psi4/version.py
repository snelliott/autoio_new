"""
Reads the program name and version number from the output file
"""

import autoparse.pattern as app
import autoparse.find as apf


def program_name(output_string):
    """ reads the program name (here: MainName + MainVersion)
    """
    prog_string = _get_prog_string(output_string)
    num = prog_string.split()[1]
    num = num.split('.')[0]
    prog_name = prog_string.split()[0]
    prog_name = prog_name.lower()

    return prog_name


def program_version(output_string):
    """ reads the program version number
    """
    prog_string = _get_prog_string(output_string)
    prog_version = prog_string.split()[1]

    return prog_version


def _get_prog_string(output_string):
    """ obtains the string containing the version name and number
    """

    pattern = app.capturing(
                ('Psi4' + app.SPACE +
                 app.one_or_more(app.NONNEWLINE) + app.SPACE +
                 'release'))

    prog_string = apf.first_capture(pattern, output_string)

    return prog_string

if __name__ == '__main__':
    with open('output.dat', 'r') as f:
        a = f.read()
    print(name(a))
    print(number(a))
