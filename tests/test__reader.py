""" test elstruct.reader
"""
from elstruct import reader


def test__programs():
    """ test elstruct.reader.programs
    """
    assert set(reader.programs()) >= {
        'cfour2', 'g09', 'molpro', 'mrcc2018', 'nwchem6', 'orca4', 'psi4'}


def test__gradient_programs():
    """ test elstruct.reader.gradient_programs
    """
    assert set(reader.gradient_programs()) >= {
        'cfour2', 'g09', 'mrcc2018', 'orca4', 'psi4'}


def test__hessian_programs():
    """ test elstruct.reader.hessian_programs
    """
    assert set(reader.hessian_programs()) >= {
        'g09', 'orca4', 'psi4'}


def test__opt_geometry_programs():
    """ test elstruct.reader.opt_geometry_programs
    """
    assert set(reader.opt_geometry_programs()) >= {
        'cfour2', 'g09', 'molpro', 'orca4', 'psi4'}


def test__opt_zmatrix_programs():
    """ test elstruct.reader.opt_zmatrix_programs
    """
    assert set(reader.opt_zmatrix_programs()) >= {
        'cfour2', 'g09', 'molpro', 'psi4'}


def test__irc_programs():
    """ test elstruct.reader.irc_programs
    """
    assert set(reader.irc_programs()) >= {
        'g09'}


def test__vpt2_programs():
    """ test elstruct.reader.vpt2_programs
    """
    assert set(reader.vpt2_programs()) >= {
        'g09'}


if __name__ == '__main__':
    test__programs()
