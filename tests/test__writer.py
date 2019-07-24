""" test elstruct.writer
"""
from elstruct import writer


def test__programs():
    """ test writer.programs
    """
    assert set(writer.programs()) >= {'psi4', 'g09', 'molpro'}


def test__optimization_programs():
    """ test writer.optimization_programs
    """
    assert set(writer.optimization_programs()) >= {'psi4', 'g09', 'molpro'}


if __name__ == '__main__':
    # test__programs()
    test__optimization_programs()
