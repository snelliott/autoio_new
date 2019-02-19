""" test elstruct.reader
"""
from elstruct import reader


def test__optimized_cartesian_geometry_programs():
    """ test elstruct.reader.optimized_cartesian_geometry_programs
    """
    assert reader.optimized_cartesian_geometry_programs() == ('psi4',)


def test__optimized_zmatrix_geometry_programs():
    """ test elstruct.reader.optimized_zmatrix_geometry_programs
    """
    assert reader.optimized_zmatrix_geometry_programs() == ('psi4',)


if __name__ == '__main__':
    test__optimized_cartesian_geometry_programs()
    test__optimized_zmatrix_geometry_programs()
