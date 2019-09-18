"""
Obtain information from VPT2 calculations
"""

import elstruct.reader


def test__vpt2_reader():
    """ vpt2 reader
    """
   
    with open('output.dat', 'r') as outfile:
        output_string = outfile.read()

    vpt2_dict = elstruct.reader.vpt2('gaussian09', output_string)

    for key, val in vpt2_dict.items():
        print('\n\n')
        print(key)
        print(val)


if __name__ == '__main__':
    test__vpt2_reader()
