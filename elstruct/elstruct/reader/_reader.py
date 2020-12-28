""" Electronic structure program output reading module

    Calls functions from the various program modules. Each module must provide
    a function that matches one in the module template --
    both the function name and signature are checked.

    The resulting function signatures are exactly those in module_template.py
    with `prog` inserted as the first argument.
"""

import functools
import automol
from elstruct import program_modules as pm
from elstruct import par
from elstruct.reader import module_template


MODULE_NAME = par.Module.READER


# energy
def programs():
    """ Constructs a list of available electronic structure programs.
        At minimum, each program must have an energy reader to be enumerated.
    """
    return pm.program_modules_with_functions(
        MODULE_NAME, [module_template.energy])


def methods(prog):
    """ Constructs a list of available electronic structure methods.

        :param prog: electronic structure program to use as a backend
        :type prog: str
    """
    return par.program_methods(prog)


def energy(prog, method, output_str):
    """ Reads the electronic energy from the output string.
        Returns the energy in Hartrees.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param method: electronic structure method
        :type method: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    prog = prog.lower()
    method = method.lower()
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.energy,
        # *args
        method, output_str)


def energy_(prog, method):
    """ Reads the electronic energy from the output string. (callable)

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
    """ Constructs a list of program modules implementing gradient readers.
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.gradient)


def gradient(prog, output_str):
    """ Reads the gradient from the output string.
        Returns the gradient in atomic units.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.gradient,
        # *args
        output_str)


def gradient_(prog):
    """ Reads the gradient from the output string. (callable)
        Returns the gradient in atomic units.

        :param prog: electronic structure program to use as a backend
        :type prog: str
    """
    func = functools.partial(gradient, prog)
    func.__name__ = '_gradient_'
    return func


# hessian
def hessian_programs():
    """ Constructs a list of program modules implementing hessian readers.
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.hessian)


def hessian(prog, output_str):
    """ Reads the Hessian from the output string.
        Returns the Hessian in atomic units.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.hessian,
        # *args
        output_str)


def hessian_(prog):
    """ read hessian from the output string (callable).

    :param prog: electronic structure program to use as a backend
    :type prog: str
    """
    func = functools.partial(hessian, prog)
    func.__name__ = '_hessian_'
    return func


def harmonic_frequencies_programs():
    """ Constructs a list of program modules implementing
        harmonic vibrarional frequency readers.
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.harmonic_frequencies)


def harmonic_frequencies(prog, output_str):
    """ Reads the harmonic vibrational frequencies from the output string.
        Returns the frequencies in cm-1.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.harmonic_frequencies,
        # *args
        output_str)


def harmonic_frequencies_(prog):
    """ Reads the harmonic vibrational frequencies from the output string.
        (callable).
        Returns the frequencies in cm-1.

        :param prog: electronic structure program to use as a backend
        :type prog: str
    """
    func = functools.partial(harmonic_frequencies, prog)
    func.__name__ = '_harmonic_frequencies_'
    return func


def normal_coordinates_programs():
    """ Constructs a list of program modules implementing
        normal coordinate readers.
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.normal_coordinates)


def normal_coordinates(prog, output_str):
    """ Reads the displacement along the normal modes from the output string.
        Returns the coordinates in Bohr.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.normal_coordinates,
        # *args
        output_str)


def normal_coordinates_(prog):
    """ Reads the displacement along the normal modes from the output string.
        (callable)
        Returns the coordinates in Bohr.

        :param prog: electronic structure program to use as a backend
        :type prog: str
    """
    func = functools.partial(normal_coordinates, prog)
    func.__name__ = '_normal_coordinates_'
    return func


# irc_information
def irc_programs():
    """ Constructs a list of program modules implementing
        Intrinsic Reaction Coordinate readers.
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.irc_points)


def irc_points(prog, output_str):
    """ Reads the geometries, gradients, and Hessians at each point along the
        Intrinsic Reaction Coordinate from the output string.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.irc_points,
        # *args
        output_str)


def irc_points_(prog):
    """ Reads the coordinates and electronic energies (relative to saddple point)
        of the Intrinsic Reaction Coordinate.

        :param prog: electronic structure program to use as a backend
        :type prog: str
    """
    func = functools.partial(irc_points, prog)
    func.__name__ = '_irc_points_'
    return func


def irc_path(prog, output_str):
    """ read irc_path from the output string

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.irc_path,
        # *args
        output_str)


def irc_path_(prog):
    """ read irc_path from the output string (callable)

        :param prog: electronic structure program to use as a backend
        :type prog: str
    """
    func = functools.partial(irc_path, prog)
    func.__name__ = '_irc_path_'
    return func


# optimization
def opt_geometry_programs():
    """ Constructs a list of program modules implementing
        optimized geometry readers.
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.opt_geometry)


def opt_geometry(prog, output_str):
    """ Reads the optimized geometry from the output string.
        Returns the geometry in Bohr.

        For robustness: if geometry read fails, try reading
        the z-matrix and converting.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    try:
        geo = _opt_geometry(prog, output_str)
    except TypeError:
        zma = opt_zmatrix(prog, output_str)
        geo = automol.zmatrix.geometry(zma)
    return geo


def _opt_geometry(prog, output_str):
    """ Reads the optimized geometry from the output string.
        Returns the geometry in Bohr.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.opt_geometry,
        # *args
        output_str)


def opt_geometry_(prog):
    """ Reads the optimized geometry from the output string. (callable)
        Returns the geometry in Bohr.

        :param prog: electronic structure program to use as a backend
        :type prog: str
    """
    func = functools.partial(opt_geometry, prog)
    func.__name__ = '_opt_geometry_'
    return func


# z-matrix geometry optimizations
def opt_zmatrix_programs():
    """ Contucts a list of program modules implementing optimized Z-Matrix readers.
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.opt_zmatrix)


def opt_zmatrix(prog, output_str):
    """ Reads the optimized Z-Matrix from the output string.
        Returns the geometry in Bohr+Radians.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.opt_zmatrix,
        # *args
        output_str)


def opt_zmatrix_(prog):
    """ Reads the optimized Z-Matrix from the output string. (callable)
        Returns the geometry in Bohr+Radians.

        :param prog: electronic structure program to use as a backend
        :type prog: str
    """
    func = functools.partial(opt_zmatrix, prog)
    func.__name__ = '_opt_zmatrix_'
    return func


# vpt2
def vpt2_programs():
    """ Constructs a list of program modules implementing
        2nd-order vibrational perturbation theory (VPT2) readers.
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.vpt2)


def vpt2(prog, output_str):
    """ Reads VPT2 information from the output string.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.vpt2,
        # *args
        output_str)


def vpt2_(prog):
    """ Reads VPT2 information from the output string. (callable)

        :param prog: electronic structure program to use as a backend
        :type prog: str
    """
    func = functools.partial(vpt2, prog)
    func.__name__ = '_vpt2_'
    return func


# dipole moment
def dipole_moment_programs():
    """ Constructs a list of program modules implementing
        static dipole moment readers.
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.dipole_moment)


def dipole_moment(prog, output_str):
    """ Reads the static dipole moment from the output string.
        Returns the dipole moment in Debye.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.dipole_moment,
        # *args
        output_str)


def dipole_moment_(prog):
    """ Reads the static dipole moment from the output string. (callable)
        Returns the dipole moment in Debye.

        :param prog: electronic structure program to use as a backend
        :type prog: str
    """
    func = functools.partial(dipole_moment, prog)
    func.__name__ = '_dipole_moment_'
    return func


# dipole moment
def polarizability_programs():
    """ Constructs a list of program modules implementing
        polarizability tensor readers.
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.polarizability)


def polarizability(prog, output_str):
    """ Reads the polarizability tensor from the output string.
        Returns the dipole moment in _.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.polarizability,
        # *args
        output_str)


def polarizability_(prog):
    """ Reads the polarizability tensor from the output string. (callable)
        Returns the dipole moment in _.

        :param prog: electronic structure program to use as a backend
        :type prog: str
    """
    func = functools.partial(polarizability, prog)
    func.__name__ = '_polarizability_'
    return func


# status
def has_normal_exit_message(prog, output_str):
    """ Assess whether the output file string contains the
        normal program exit message.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.has_normal_exit_message,
        # *args
        output_str)


def error_list(prog):
    """ Constructs a list of errors that be identified from the output file.

        :param prog: the electronic structure program to use as a backend
        :type prog: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.error_list)


def success_list(prog):
    """ Constructs a list of successes that be identified from the output file.

        :param prog: the electronic structure program to use as a backend
        :type prog: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.success_list)


def has_error_message(prog, error, output_str):
    """ Assess whether the output file string contains error messages
        for any of the procedures in the job.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param error: a key indicating the type of error message
        :type error: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.has_error_message,
        # *args
        error, output_str)


def check_convergence_messages(prog, error, success, output_str):
    """ Assess whether the output file string contains messages
        denoting all of the requested procedures in the job have converged.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param error: a key indicating the type of error message
        :type error: str
        :param success: a key indicating the type of success message
        :type success: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.check_convergence_messages,
        # *args
        error, success, output_str)


# versions
def program_name(prog, output_str):
    """ Reads the name of the electronic structure code from the output file.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.program_name, output_str)


def program_version(prog, output_str):
    """ Reads the version of the electronic structure code from the output file.

        :param prog: electronic structure program to use as a backend
        :type prog: str
        :param output_str: string of the program's output file
        :type output_str: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.program_version, output_str)
