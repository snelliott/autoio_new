""" output reading module

Calls functions from the various program modules. Each module must provide a
function that matches one in the module template -- both the function name and
signature are checked. The resulting function signatures are exactly those in
module_template.py with `prog` inserted as the first argument.
"""
import functools
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


def energy_(prog, method):
    """ read energy from the output string (callable)

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param method: electronic structure method
    :type method: str
    """
    return functools.partial(energy, prog, method)


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


def gradient_(prog):
    """ read gradient from the output string (callable)

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param method: electronic structure method
    :type method: str
    """
    return functools.partial(gradient, prog)


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


def hessian_(prog):
    """ read hessian from the output string (callable)

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param method: electronic structure method
    :type method: str
    """
    return functools.partial(hessian, prog)


# optimization
def optimized_geometry_programs():
    """ list of program modules implementing optimized geometry readers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.optimized_geometry)


def optimized_geometry(prog, output_string):
    """ read optimized geometry from the output string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.optimized_geometry,
        # *args
        output_string)


def optimized_geometry_(prog):
    """ read optimized geometry from the output string (callable)

    :param prog: electronic structure program to use as a backend
    :type prog: str
    """
    return functools.partial(optimized_geometry, prog)


# z-matrix geometry optimizations
def optimized_zmatrix_programs():
    """ list of program modules implementing optimized zmatrix readers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.optimized_zmatrix)


def optimized_zmatrix(prog, output_string):
    """ read optimized zmatrix from the output string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.optimized_zmatrix,
        # *args
        output_string)


def optimized_zmatrix_(prog):
    """ read optimized zmatrix from the output string (callable)

    :param prog: electronic structure program to use as a backend
    :type prog: str
    """
    return functools.partial(optimized_zmatrix, prog)


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


def has_normal_exit_message_(prog):
    """ does this output string have a normal exit message? (callable)

    :param prog: electronic structure program to use as a backend
    :type prog: str
    """
    return functools.partial(has_normal_exit_message, prog)
