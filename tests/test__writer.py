""" test elstruct.writer
"""
from elstruct import writer


def test__programs():
    """ test writer.programs
    """
    assert set(writer.programs()) >= {
        'cfour2', 'g09', 'molpro', 'mrcc2018', 'psi4'}


def test__optimization_programs():
    """ test writer.optimization_programs
    """
    assert set(writer.optimization_programs()) >= {
        'cfour2', 'g09', 'molpro', 'mrcc2018', 'psi4'}


if __name__ == '__main__':
    test__programs()
