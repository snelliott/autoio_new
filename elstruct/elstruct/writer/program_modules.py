""" helpers for importing and managing program modules
"""

from elstruct import par
from elstruct import pclass


# Functions to import and call the appropriate writer function
def call_module_function(prog, function, *args, **kwargs):
    """ call the module implementation of a given function

        :param prog: the program
        :type prog: str
        :param function_template: a function with the desired signature
        :type function_template: function
    """

    assert prog in pclass.values(par.Program)
    assert prog in program_modules_with_function(function)
    assert typ in pclass.values(par.Module)

    name = '_{}'.format(prog)
    module = importlib.import_module('elstruct.writer.{:s}'.format(name))
    writer = getattr(module, 'fillvalue_dictionary'))

    return writer(*args, **kwargs)


def program_modules_with_function(function):
    """
        :param function: a function with the desired signature
        :type function: function
    """

    progs = []
    for prog in pclass.values(par.Program):
        if function in WRITER_MODULE_DCT[prog]:
            progs.append(function)

    return progs


# Information on what writers have been implemented
class Job():
    """ Names of electronic structure jobs to ne written
    """
    ENERGY = 'energy'
    GRADIENT = 'gradient'
    HESSIAN = 'hessian'
    VPT2 = 'vpt2'
    IRC = 'irc'
    MOLPROP = 'molecular_properties'
    OPTIMIZATION = 'optimization'


# Dictionaries that dictate what writer/reader functionality
WRITER_MODULE_DCT = {
    elstruct.par.Program.CFOUR2: (
        Job.ENERGY, Job.GRADIENT, Job.HESSIAN, Job.OPTIMIZATION),
    elstruct.par.Program.GAUSSIAN09: (
        Job.ENERGY, Job.GRADIENT, Job.HESSIAN, Job.OPTIMIZATION,
        Job.MOLPROP, Job.IRC, Job.VPT2),
    elstruct.par.Program.GAUSSIAN16: (
        Job.ENERGY, Job.GRADIENT, Job.HESSIAN, Job.OPTIMIZATION,
        Job.MOLPROP, Job.IRC, Job.VPT2),
    elstruct.par.Program.MOLPRO2015: (
        Job.ENERGY, Job.GRADIENT, Job.HESSIAN, Job.OPTIMIZATION,
        Job.MOLPROP, Job.IRC, Job.VPT2),
    elstruct.par.Program.MRCC2018: (
        Job.ENERGY, Job.HESSIAN, Job.OPTIMIZATION),
    elstruct.par.Program.NWCHEM6: (
        Job.ENERGY, Job.OPTIMIZATION),
    elstruct.par.Program.ORCA4: (
        Job.ENERGY, Job.GRADIENT, Job.HESSIAN, Job.OPTIMIZATION),
    elstruct.par.Program.PSI4: (
        Job.ENERGY, Job.GRADIENT, Job.HESSIAN, Job.OPTIMIZATION,
        Job.IRC)
}
