""" test mess_io.reader.pes
"""

import os
import numpy
from ioformat import read_text_file
import mess_io


PATH = os.path.dirname(os.path.realpath(__file__))
INP_STR = read_text_file(['data', 'inp'], 'mess.inp', PATH)


def test__():
    """ test mess_io.reader.pes
    """

    # Test reading with removing any fake wells
    energy_dct1, conn_lst1, _ = mess_io.reader.pes(
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
    energy_dct2, conn_lst2, _ = mess_io.reader.pes(
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
