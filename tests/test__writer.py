""" test elstruct.writer
"""
from elstruct import writer


def test__programs():
    """ test writer.programs
    """
    assert writer.programs() == ('psi4',)


def test__method_list():
    """ test writer.method_list
    """
    for prog in writer.programs():
        methods = writer.method_list(prog)
        assert methods  # make sure it isn't empty
        print((prog, methods))


def test__basis_list():
    """ test writer.basis_list
    """
    for prog in writer.programs():
        bases = writer.basis_list(prog)
        assert bases  # make sure it isn't empty
        print((prog, bases))


def test__optimization_programs():
    """ test writer.optimization_programs
    """
    assert writer.optimization_programs() == ('psi4',)


if __name__ == '__main__':
    # test__programs()
    # test__method_list()
    # test__basis_list()
    test__optimization_programs()
