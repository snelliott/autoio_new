"""
 tests rates reader
"""
import os

import mess_io.reader
from _util import read_text_file


PATH = os.path.dirname(os.path.realpath(__file__))
KTP_OUT_STR = read_text_file(['data', 'out'], 'rate.out', PATH)
KE_OUT_STR = read_text_file(['data', 'out'], 'ke.out', PATH)

# Set the REACTANT and PRODUCT
REACTANT = 'W1'
PRODUCT = 'W3'


def test__ktp_dct():
    """ tests mess_io.reader.rates.ktp_dct
    """

    ktp_dct = mess_io.reader.rates.ktp_dct(
        KTP_OUT_STR, REACTANT, PRODUCT)

    for pressure in ktp_dct:
        print(pressure, ':', ktp_dct[pressure])


def test__ke_dct():
    """ tests mess_io.reader.rates.ke_dct
    """

    ke_dct = mess_io.reader.rates.ke_dct(
        KE_OUT_STR, REACTANT, PRODUCT)

    for ene in ke_dct:
        print(ene, ':', ke_dct[ene])


if __name__ == '__main__':
    test__ktp_dct()
    test__ke_dct()
