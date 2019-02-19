""" input writing module

Calls functions from the various program modules. Each module must provide a
function that matches one in the module template -- both the function name and
signature are checked before calling the function. The resulting function
signatures are exactly those in module_template.py with `prog` inserted as the
first required argument.
"""
from . import module_template
from .. import program_modules as pm
from .. import params as par

MODULE_NAME = par.MODULE.WRITER


def programs():
    """ the list of program modules implementing anything """
    # check whether they implement the `method_list()` function
    return pm.program_modules_with_functions(
        MODULE_NAME, [module_template.method_list, module_template.basis_list])


def energy_programs():
    """ the list of program modules implementing energy input writers """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.energy_input_string)


def optimization_programs():
    """ the list of program modules implementing optimization input writers """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.optimization_input_string)


def method_list(prog, *args, **kwargs):
    """ _ """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.method_list,
        *args, **kwargs
    )


def basis_list(prog, *args, **kwargs):
    """ _ """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.basis_list,
        *args, **kwargs
    )


def energy_input_string(prog, *args, **kwargs):
    """ _ """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.energy_input_string,
        *args, **kwargs
    )


def optimization_input_string(prog, *args, **kwargs):
    """ _ """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.optimization_input_string,
        *args, **kwargs
    )
