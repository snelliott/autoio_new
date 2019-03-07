""" output reading module

Calls functions from the various program modules. Each module must provide a
function that matches one in the module template -- both the function name and
signature are checked. The resulting function signatures are exactly those in
module_template.py with `prog` inserted as the first argument.
"""
from . import module_template
from .. import program_modules as pm
from .. import params as par

MODULE_NAME = par.MODULE.READER


# energy
def programs():
    """ list of available electronic structure programs

    (must at least implement an energy reader)
    """
    return pm.program_modules_with_functions(
        MODULE_NAME, [module_template.method_list,
                      module_template.energy])


def method_list(prog):
    """ list of available electronic structure methods

    :param prog: the electronic structure program to use as a backend
    :type prog: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.method_list)


def energy(prog, method, output_string):
    """ read energy from the output string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param method: electronic structure method
    :type method: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.energy,
        # *args
        method, output_string)


# gradient
def gradient_programs():
    """ list of program modules implementing gradient readers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.gradient)


def gradient(prog, output_string):
    """ read gradient from the output string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.gradient,
        # *args
        output_string)


# hessian
def hessian_programs():
    """ list of program modules implementing hessian readers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.hessian)


def hessian(prog, output_string):
    """ read hessian from the output string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.hessian,
        # *args
        output_string)


# optimization
def opt_geometry_programs():
    """ list of program modules implementing optimized geometry readers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.opt_geometry)


def opt_geometry(prog, output_string):
    """ read optimized geometry from the output string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.opt_geometry,
        # *args
        output_string)


# z-matrix geometry optimizations
def opt_zmatrix_programs():
    """ list of program modules implementing optimized zmatrix readers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.opt_zmatrix)


def opt_zmatrix(prog, output_string):
    """ read optimized zmatrix from the output string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.opt_zmatrix,
        # *args
        output_string)


# status
def has_normal_exit_message(prog, output_string):
    """ does this output string have a normal exit message?

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.has_normal_exit_message,
        # *args
        output_string)


def has_scf_nonconvergence_message(prog, output_string):
    """ does this output string have an SCF non-convergence message?

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.has_scf_nonconvergence_message,
        # *args
        output_string)


def has_opt_nonconvergence_message(prog, output_string):
    """ does this output string have an optimization non-convergence message?

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.has_opt_nonconvergence_message,
        # *args
        output_string)
