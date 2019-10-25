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


# irc points
def irc_points(output_string):
    """ _ """
    raise NotImplementedError


def irc_energies(output_string):
    """ _ """
    raise NotImplementedError


def irc_coordinates(output_string):
    """ _ """
    raise NotImplementedError


# optimization
def opt_geometry(output_string):
    """ _ """
    raise NotImplementedError(output_string)


def opt_zmatrix(output_string):
    """ _ """
    raise NotImplementedError(output_string)


# vpt2
def vpt2(output_string):
    """ _ """
    raise NotImplementedError(output_string)


# properties
def dipole_moment(output_string):
    """ _ """
    raise NotImplementedError(output_string)


# status
def has_normal_exit_message(output_string):
    """ _ """
    raise NotImplementedError(output_string)


def error_list():
    """ _ """
    raise NotImplementedError()


def success_list():
    """ _ """
    raise NotImplementedError()


def has_error_message(error, output_string):
    """ _ """
    raise NotImplementedError(error, output_string)


def check_convergence_messages(error, success, output_string):
    """ _ """
    raise NotImplementedError(error, success, output_string)


# version
def program_name(output_string):
    """ _ """
    raise NotImplementedError(output_string)


def program_version(output_string):
    """ _ """
    raise NotImplementedError(output_string)
