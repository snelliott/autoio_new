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


# energies
def programs():
    """ programs which at least implement energy readers """
    return pm.program_modules_with_functions(
        MODULE_NAME, [module_template.method_list,
                      module_template.energy])


def method_list(prog, *args, **kwargs):
    """ _ """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.method_list,
        *args, **kwargs)


def energy(prog, *args, **kwargs):
    """ _ """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.energy,
        *args, **kwargs)


# status checkers
def ran_successfully(prog, *args, **kwargs):
    """ _ """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.ran_successfully,
        *args, **kwargs)


# cartesian geometry optimizations
def optimized_cartesian_geometry_programs():
    """ _ """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.optimized_cartesian_geometry)


def optimized_cartesian_geometry(prog, *args, **kwargs):
    """ _ """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.optimized_cartesian_geometry,
        *args, **kwargs
    )


# z-matrix geometry optimizations
def optimized_zmatrix_geometry_programs():
    """ _ """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.optimized_zmatrix_geometry)


def optimized_zmatrix_geometry(prog, *args, **kwargs):
    """ _ """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.optimized_zmatrix_geometry,
        *args, **kwargs
    )
