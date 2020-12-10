""" helpers for importing and managing program modules """
import importlib
try:
    from inspect import getfullargspec as _getargspec
except ImportError:
    from inspect import getargspec as _getargspec
from functools import reduce as _reduce
from elstruct import par
from elstruct import pclass


def module_name(prog):
    """ get the module name for a program
    """
    return '_{}'.format(prog)


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
    """ list the programs implementing a given set of functions
    """
    prog_lsts = [program_modules_with_function(typ, function_template)
                 for function_template in function_templates]

    # get the intersection of all of them
    progs = _reduce(set.intersection, map(set, prog_lsts))
    return tuple(sorted(progs))


def program_modules_with_function(typ, function_template):
    """ list the programs implementing a given function

    :param typ: which type of module it is (writer or reader)
    :type typ: str
    :param function_template: a function with the desired signature
    :type function_template: function
    """
    progs = []
    for prog in pclass.values(par.Program):
        module = import_program_module(prog, typ)
        if hasattr(module, function_template.__name__):
            function = getattr(module, function_template.__name__)

            # make sure the signature matches the template
            assert _getargspec(function) == _getargspec(function_template)

            progs.append(prog)

    return tuple(sorted(progs))


def import_program_module(prog, typ):
    """ import the module for a program by name

    :param prog: the program name
    :type prog: str
    :param typ: which type of module it is (writer or reader)
    :type typ: str
    """
    assert prog in pclass.values(par.Program)
    assert typ in pclass.values(par.Module)

    name = module_name(prog)
    module = importlib.import_module('elstruct.{:s}.{:s}'.format(typ, name))
    return module
