""" test elstruct.reader
"""
from elstruct import reader


def test__programs():
    """ test elstruct.reader.programs
    """
    assert reader.programs() == ('psi4',)


def test__method_list():
    """ test elstruct.reader.method_list
    """
    for prog in reader.programs():
        assert reader.method_list(prog)  # make sure it isn't empty


def test__opt_geometry_programs():
    """ test elstruct.reader.opt_geometry_programs
    """
    assert reader.opt_geometry_programs() == ('psi4',)


def test__opt_zmatrix_programs():
    """ test elstruct.reader.opt_zmatrix_programs
    """
    assert reader.opt_zmatrix_programs() == ('psi4',)


if __name__ == '__main__':
    test__programs()
    test__method_list()
    test__opt_geometry_programs()
    test__opt_zmatrix_programs()
