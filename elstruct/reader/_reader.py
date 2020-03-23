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


def harmonic_frequencies_programs():
    """ list of program modules implementing harmonic_frequencies readers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.harmonic_frequencies)


def harmonic_frequencies(prog, output_string):
    """ read harmonic_frequencies from the output string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.harmonic_frequencies,
        # *args
        output_string)


def harmonic_frequencies_(prog):
    """ read harmonic_frequencies from the output string (callable)
    :param prog: electronic structure program to use as a backend
    :type prog: str
    """
    func = functools.partial(harmonic_frequencies, prog)
    func.__name__ = '_harmonic_frequencies_'
    return func


# irc_information
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


def irc_energies(prog, output_string):
    """ read irc_energies from the output string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.irc_energies,
        # *args
        output_string)


def irc_energies_(prog):
    """ read irc_energies from the output string (callable)
    :param prog: electronic structure program to use as a backend
    :type prog: str
    """
    func = functools.partial(irc_energies, prog)
    func.__name__ = '_irc_energies_'
    return func


def irc_coordinates(prog, output_string):
    """ read irc_coordinates from the output string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.irc_coordinates,
        # *args
        output_string)


def irc_coordinates_(prog):
    """ read irc_coordinates from the output string (callable)
    :param prog: electronic structure program to use as a backend
    :type prog: str
    """
    func = functools.partial(irc_coordinates, prog)
    func.__name__ = '_irc_coordinates_'
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


def success_list(prog):
    """ list of successs that be identified from the output file

    :param prog: the electronic structure program to use as a backend
    :type prog: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.success_list)


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


def check_convergence_messages(prog, error, success, output_string):
    """ does this output string have an error message?

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param error: a key indicating the type of error message
    :type error: str
    :param success: a key indicating the type of success message
    :type success: str
    :param output_string: the program output string
    :type output_string: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.check_convergence_messages,
        # *args
        error, success, output_string)


# versions
def program_name(prog, output_string):
    """ get the name of the electronic structure code from the output
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.program_name, output_string)


def program_version(prog, output_string):
    """ get the name of the electronic structure code from the output
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.program_version, output_string)
