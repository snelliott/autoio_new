""" Test pac99_io.reader
"""
import os

from ioformat import read_text_file
import pac99_io


PATH = os.path.dirname(os.path.realpath(__file__))


def test__polynomial():
    """ test pac99_io.reader.nasa_polynomial
        test pac99_io._convert.pac3ckin_poly
    """

    # Read and Convert C2H4N2O6
    out_str = read_text_file(['data'], 'C2H4N2O6.c97', PATH)
    pac99_poly = pac99_io.reader.nasa_polynomial(out_str)
    assert pac99_poly == (
        read_text_file(['data'], 'C2H4N2O6.paccpoly', PATH).strip())

    name = 'C2H4N2O6'
    atom_dct = {'C': 2, 'H': 4, 'N': 2, 'O': 6}
    ckin_poly = pac99_io.pac2ckin_poly(name, atom_dct, pac99_poly)
    assert ckin_poly == read_text_file(['data'], 'C2H4N2O6.ckinpoly', PATH)

    # Read and Convert CO
    out_str = read_text_file(['data'], 'CO.c97', PATH)
    pac99_poly = pac99_io.reader.nasa_polynomial(out_str)
    assert pac99_poly == (
        read_text_file(['data'], 'CO.paccpoly', PATH)).strip()

    name = 'CO'
    atom_dct = {'C': 1, 'O': 1}
    ckin_poly = pac99_io.pac2ckin_poly(name, atom_dct, pac99_poly)
    assert ckin_poly == read_text_file(['data'], 'CO.ckinpoly', PATH)

    # Read and Convert H2
    out_str = read_text_file(['data'], 'H2.c97', PATH)
    pac99_poly = pac99_io.reader.nasa_polynomial(out_str)
    assert pac99_poly == (
        read_text_file(['data'], 'H2.paccpoly', PATH)).strip()

    name = 'H2'
    atom_dct = {'H': 2}
    ckin_poly = pac99_io.pac2ckin_poly(name, atom_dct, pac99_poly)
    assert ckin_poly == read_text_file(['data'], 'H2.ckinpoly', PATH)
