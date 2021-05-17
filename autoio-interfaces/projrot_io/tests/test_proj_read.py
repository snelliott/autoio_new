"""
 tests reading of projrot output
"""
import os
import numpy
from ioformat import read_text_file
import projrot_io

PATH = os.path.dirname(os.path.realpath(__file__))


def test__reader():
    """ test projrot_io.reader.rpht_output
    """

    ref_real1 = (1000.0, 2000.0, 3000.0, 4000.0, 5000.0)

    out_str1 = read_text_file(['data'], 'min.out', PATH)
    real1, imag1 = projrot_io.reader.rpht_output(out_str1)
    assert numpy.allclose(real1, ref_real1)
    assert not imag1

    ref_real2 = (2000.0, 3000.0, 4000.0, 5000.0)
    ref_imag2 = (1111.11,)

    out_str2 = read_text_file(['data'], 'one_imag.out', PATH)
    real2, imag2 = projrot_io.reader.rpht_output(out_str2)
    assert numpy.allclose(real2, ref_real2)
    assert numpy.allclose(imag2, ref_imag2)

    ref_real3 = (3000.0, 4000.0, 5000.0)
    ref_imag3 = (1111.11, 2222.22)

    out_str3 = read_text_file(['data'], 'two_imag.out', PATH)
    real3, imag3 = projrot_io.reader.rpht_output(out_str3)
    assert numpy.allclose(real3, ref_real3)
    assert numpy.allclose(imag3, ref_imag3)


if __name__ == '__main__':
    test__reader()
