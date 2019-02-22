""" empty functions defining the function signatures for each program module
"""


# energy
def method_list():
    """ list of available electronic structure methods
    """
    raise NotImplementedError


def energy(method, output_string):
    """ get total energy from output
    """
    raise NotImplementedError


# optimization
def optimized_geometry(output_string):
    """ get optimized cartesian geometry from output
    """
    raise NotImplementedError(output_string)


def optimized_zmatrix(output_string):
    """ get optimized z-matrix from output
    """
    raise NotImplementedError(output_string)


# status
def ran_successfully(output_string):
    """ did this job run successfully?
    """
    raise NotImplementedError(output_string)
