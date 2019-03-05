""" empty functions defining the function signatures for each program module
"""


# energy
def method_list():
    """ _ """
    raise NotImplementedError


def energy(method, output_string):
    """ _ """
    raise NotImplementedError


# gradient
def gradient(output_string):
    """ _ """
    raise NotImplementedError


# hessian
def hessian(output_string):
    """ _ """
    raise NotImplementedError


# optimization
def optimized_geometry(output_string):
    """ _ """
    raise NotImplementedError(output_string)


def optimized_zmatrix(output_string):
    """ _ """
    raise NotImplementedError(output_string)


# status
def has_normal_exit_message(output_string):
    """ _ """
    raise NotImplementedError(output_string)
