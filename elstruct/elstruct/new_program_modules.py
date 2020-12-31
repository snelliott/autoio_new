""" helpers for importing and managing program modules
"""

from elstruct import par
from elstruct import pclass


def call_module_function(prog, typ, function_template,
                         *args, **kwargs):
    """ call the module implementation of a given function

    :param prog: the program
    :type prog: str
    :param typ: which type of module it is (writer or reader)
    :type typ: str
    :param function_template: a function with the desired signature
    :type function_template: function
    """
    assert prog in program_modules_with_function(typ,
                                                 function_template)

    module = import_program_module(prog, typ)
    function = getattr(module, function_template.__name__)
    return function(*args, **kwargs)


def program_modules_with_functions(typ, function_templates):
    """
        :param typ: which type of module it is (writer or reader)
        :type typ: str
        :param function_template: a function with the desired signature
        :type function_template: function
    """

    assert typ in (par.Module.WRITER, par.Module.Reader) 
    
    progs = []
    for prog in pclass.values(par.Program):
        if hasattr(module, function_template.__name__):


    if typ == par.Module.WRITER:
    elif 
    return tuple(WRITER_MODULE_DCT.keys())


# Dictionaries that dictate what writer/reader functionality
WRITER_MODULE_DCT = {
    elstruct.par.Program.CFOUR2: (
        elstruct.par.Job.ENERGY, elstruct.par.Job.GRADIENT,
        elstruct.par.Job.HESSIAN, elstruct.par.Job.OPTIMIZATION),
    elstruct.par.Program.GAUSSIAN09: (
        elstruct.par.Job.ENERGY, elstruct.par.Job.GRADIENT,
        elstruct.par.Job.HESSIAN, elstruct.par.Job.OPTIMIZATION,
        elstruct.par.Job.MOLPROP, elstruct.par.Job.IRC,
        elstruct.par.Job.VPT2),
    elstruct.par.Program.GAUSSIAN16: (
        elstruct.par.Job.ENERGY, elstruct.par.Job.GRADIENT,
        elstruct.par.Job.HESSIAN, elstruct.par.Job.OPTIMIZATION,
        elstruct.par.Job.MOLPROP, elstruct.par.Job.IRC,
        elstruct.par.Job.VPT2),
    elstruct.par.Program.MOLPRO2015: (
        elstruct.par.Job.ENERGY, elstruct.par.Job.GRADIENT,
        elstruct.par.Job.HESSIAN, elstruct.par.Job.OPTIMIZATION,
        elstruct.par.Job.MOLPROP, elstruct.par.Job.IRC,
        elstruct.par.Job.VPT2),
    elstruct.par.Program.MRCC2018: (
        elstruct.par.Job.ENERGY,
        elstruct.par.Job.HESSIAN, elstruct.par.Job.OPTIMIZATION),
    elstruct.par.Program.NWCHEM6: (
        elstruct.par.Job.ENERGY,
        elstruct.par.Job.OPTIMIZATION),
    elstruct.par.Program.ORCA4: (
        elstruct.par.Job.ENERGY, elstruct.par.Job.GRADIENT,
        elstruct.par.Job.HESSIAN, elstruct.par.Job.OPTIMIZATION),
    elstruct.par.Program.PSI4: (
        elstruct.par.Job.ENERGY, elstruct.par.Job.GRADIENT,
        elstruct.par.Job.HESSIAN, elstruct.par.Job.OPTIMIZATION,
        elstruct.par.Job.IRC)
}

READER_MODULE_DCT = {
    elstruct.par.Program.CFOUR2: {
    }
    elstruct.par.Program.GAUSSIAN09: {
    }
    elstruct.par.Program.GAUSSIAN16: {
    }
    elstruct.par.Program.MOLPRO2015: {
    }
    elstruct.par.Program.MRCC2018: {
    }
    elstruct.par.Program.NWCHEM6: {
    }
    elstruct.par.Program.ORCA4: {
    }
    elstruct.par.Program.PSI4: {
}
