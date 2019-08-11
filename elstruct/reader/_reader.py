""" output reading module

Calls functions from the various program modules. Each module must provide a
function that matches one in the module template -- both the function name and
signature are checked. The resulting function signatures are exactly those in
module_template.py with `prog` inserted as the first argument.
"""
import functools
import automol
from elstruct import program_modules as pm
from elstruct import par
from elstruct.reader import module_template

MODULE_NAME = par.Module.READER


# energy
def programs():
    """ list of available electronic structure programs

    (must at least implement an energy reader)
    """
    return pm.program_modules_with_functions(
        MODULE_NAME, [module_template.energy])


def methods(prog):
    """ list of available electronic structure methods

    :param prog: the electronic structure program to use as a backend
    :type prog: str
    """
    return par.program_methods(prog)


def energy(prog, method, output_string):
    """ read energy from the output string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param method: electronic structure method
    :type method: str
    :param output_string: the program output string
    :type output_string: str
    """
    prog = prog.lower()
    method = method.lower()
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
    func = functools.partial(energy, prog, method)
    func.__name__ = '_energy_'
    return func


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
    """
    func = functools.partial(gradient, prog)
    func.__name__ = '_gradient_'
    return func


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
    """
    func = functools.partial(hessian, prog)
    func.__name__ = '_hessian_'
    return func


# irc_points
def irc_programs():
    """ list of program modules implementing irc_points readers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.irc_points)


def irc_points(prog, output_string):
    """ read irc_points from the output string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.irc_points,
        # *args
        output_string)


def irc_points_(prog):
    """ read irc_points from the output string (callable)
    :param prog: electronic structure program to use as a backend
    :type prog: str
    """
    func = functools.partial(irc_points, prog)
    func.__name__ = '_irc_points_'
    return func


# optimization
def opt_geometry_programs():
    """ list of program modules implementing optimized geometry readers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.opt_geometry)


def opt_geometry(prog, output_string):
    """ read optimized geometry from the output string

    (for robustness: if geometry read fails [esp for monatomics], try reading
    the z-matrix and converting)

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    try:
        geo = _opt_geometry(prog, output_string)
    except TypeError:
        zma = opt_zmatrix(prog, output_string)
        geo = automol.zmatrix.geometry(zma)
    return geo


def _opt_geometry(prog, output_string):
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


def opt_geometry_(prog):
    """ read optimized geometry from the output string (callable)
    :param prog: electronic structure program to use as a backend
    :type prog: str
    """
    func = functools.partial(opt_geometry, prog)
    func.__name__ = '_opt_geometry_'
    return func


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


def opt_zmatrix_(prog):
    """ read optimized zmatrix from the output string (callable)
    :param prog: electronic structure program to use as a backend
    :type prog: str
    """
    func = functools.partial(opt_zmatrix, prog)
    func.__name__ = '_opt_zmatrix_'
    return func


# vpt2
def vpt2_programs():
    """ list of program modules implementing vpt2 readers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.vpt2)


def vpt2(prog, output_string):
    """ read vpt2 from the output string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.vpt2,
        # *args
        output_string)


def vpt2_(prog):
    """ read vpt2 from the output string (callable)
    :param prog: electronic structure program to use as a backend
    :type prog: str
    """
    func = functools.partial(vpt2, prog)
    func.__name__ = '_vpt2_'
    return func


# dipole moment
def dipole_moment_programs():
    """ list of program modules implementing dipole_moment readers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.dipole_moment)


def dipole_moment(prog, output_string):
    """ read dipole_moment from the output string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.dipole_moment,
        # *args
        output_string)


def dipole_moment_(prog):
    """ read dipole_moment from the output string (callable)
    :param prog: electronic structure program to use as a backend
    :type prog: str
    """
    func = functools.partial(dipole_moment, prog)
    func.__name__ = '_dipole_moment_'
    return func


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


def error_list(prog):
    """ list of errors that be identified from the output file

    :param prog: the electronic structure program to use as a backend
    :type prog: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.error_list)


def has_error_message(prog, error, output_string):
    """ does this output string have an error message?

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param error: a key indicating the type of error message
    :type error: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.has_error_message,
        # *args
        error, output_string)
