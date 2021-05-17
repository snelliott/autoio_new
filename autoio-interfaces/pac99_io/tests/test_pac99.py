""" Test pac99_io.reader
"""
import os

from ioformat import read_text_file
import pac99_io


PATH = os.path.dirname(os.path.realpath(__file__))
OUT_STR = read_text_file(['data'], 'mol.c97', PATH)


def test__polynomial():
    """ test pac99_io.reader.__
    """

    pac99_poly = pac99_io.reader.nasa_polynomial(OUT_STR)
    assert pac99_poly == read_text_file(['data'], 'pac99_poly.dat', PATH)

    name = 'mol'
    atom_dct = {'C': 2, 'H': 4, 'N': 2, 'O': 6}
    ckin_poly = pac99_io.pac2ckin_poly(name, atom_dct, pac99_poly)
    assert ckin_poly == read_text_file(['data'], 'ckin_poly.dat', PATH)


if __name__ == '__main__':
    test__polynomial()
