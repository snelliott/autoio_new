"""
Obtain information from VPT2 calculations
"""

import elstruct.reader


def test__vpt2_reader(filename):
    """ vpt2 reader
    """

    with open(filename, 'r') as outfile:
        output_string = outfile.read()

    vpt2_dict = elstruct.reader.vpt2('gaussian09', output_string)

    for key, val in vpt2_dict.items():
        print('\n')
        print(key)
        print(val)


if __name__ == '__main__':
    test__vpt2_reader('output.dat')
    test__vpt2_reader('n2.out')
