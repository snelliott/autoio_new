"""
 tests pes reader
"""

import os
import mess_io.reader


PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PATH, 'data')
DATA_NAME = 'rates.inp'
with open(os.path.join(DATA_PATH, DATA_NAME), 'r') as datfile:
    INP_STR = datfile.read()


def test__pes():
    """ tests mess_io.reader.pes
    """

    energy_dct, conn_lst = mess_io.reader.pes(
        INP_STR, read_fake=False)
    print('\nEnergy dct')
    for name, ene in energy_dct.items():
        print(name, ene)
    print('\nConnections lst')
    for pair in conn_lst:
        print(pair)

    energy_dct, conn_lst = mess_io.reader.pes(
        INP_STR, read_fake=True)
    print('\nEnergy dct')
    for name, ene in energy_dct.items():
        print(name, ene)
    print('\nConnections lst')
    for pair in conn_lst:
        print(pair)


if __name__ == '__main__':
    test__pes()
