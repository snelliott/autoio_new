"""
 tests pes reader
"""

import os
import numpy
import mess_io
from _util import read_text_file


INP_STR = read_text_file(['data', 'inp'], 'full_rates.inp')


def test__pes():
    """ tests mess_io.reader.pes
    """

    # Test reading with removing any fake wells
    energy_dct1, conn_lst1 = mess_io.reader.pes(
        input_string=INP_STR,
        read_fake=False)

    ref_energy_dct1 = {
        'P1': 0.0,
        'P2': 3.22,
        'B1': 13.23
    }
    ref_conn_lst1 = (
        ('P1', 'B1'),
        ('B1', 'P2')
    )

    assert set(energy_dct1.keys()) == set(ref_energy_dct1.keys())
    assert all(numpy.isclose(energy_dct1[key], ref_energy_dct1[key])
               for key in energy_dct1)
    assert conn_lst1 == ref_conn_lst1

    # Test reading the entire PES with fake wells
    energy_dct2, conn_lst2 = mess_io.reader.pes(
        input_string=INP_STR,
        read_fake=True)

    ref_energy_dct2 = {
        'F1': -1.0,
        'F2': 2.22,
        'P1': 0.0,
        'P2': 3.22,
        'FRB1': 0.0,
        'FPB1': 3.22,
        'B1': 13.23
    }

    ref_conn_lst2 = (
        ('P1', 'FRB1'),
        ('FRB1', 'F1'),
        ('P2', 'FPB1'),
        ('FPB1', 'F2'),
        ('F1', 'B1'),
        ('B1', 'F2')
    )

    assert set(energy_dct2.keys()) == set(ref_energy_dct2.keys())
    assert all(numpy.isclose(energy_dct2[key], ref_energy_dct2[key])
               for key in energy_dct2)
    assert conn_lst2 == ref_conn_lst2


if __name__ == '__main__':
    test__pes()
