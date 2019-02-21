""" empty functions defining the function signatures for each program module
"""


def method_list():
    """ list of available electronic structure methods
    """
    raise NotImplementedError


def energy(method, output_string):
    """ get total energy from output
    """
    raise NotImplementedError


def optimized_cartesian_geometry(output_string):
    """ get optimized cartesian geometry from output
    """
    raise NotImplementedError(output_string)


def optimized_zmatrix_geometry(output_string):
    """ get optimized z-matrix geometry from output
    """
    raise NotImplementedError(output_string)
