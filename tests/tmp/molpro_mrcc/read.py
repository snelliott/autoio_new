""" irc readers
"""

import elstruct.reader


def test__mr_reader():
    """ writes an energy file for multiref method in molpro
        writes the information to files
    """
    with open('output.dat', 'r') as outfile:
        output_string = outfile.read()

    prog = 'molpro2015'
    method = 'ccsdt'
    ene = elstruct.reader.energy(prog, method, output_string)
    print(ene)
    method = 'ccsdt(q)'
    ene = elstruct.reader.energy(prog, method, output_string)
    print(ene)


if __name__ == '__main__':
    test__mr_reader()
