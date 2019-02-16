""" helpers for importing and managing program modules """
import importlib
import inspect
from functools import reduce as _reduce
from . import params as par


PROGRAM_MODULE_NAME_DCT = {
    par.PROGRAM.PSI4: '_psi4',
}


def call_module_function(prog, module_type, function_template,
                         *args, **kwargs):
    """ call the module implementation of a given function

    :param prog: the program
    :type prog: str
    :param module_type: which type of module it is (write or read)
    :type module_type: str
    :param function_template: a function with the desired signature
    :type function_template: function
    """
    assert prog in program_modules_with_function(module_type,
                                                 function_template)

    module = import_program_module(prog, module_type)
    function = getattr(module, function_template.__name__)
    return function(*args, **kwargs)


def program_modules_with_functions(module_type, function_templates):
    """ list the programs implementing a given set of functions
    """
    prog_lsts = [program_modules_with_function(module_type, function_template)
                 for function_template in function_templates]

    # get the intersection of all of them
    progs = _reduce(set.intersection, map(set, prog_lsts))
    return tuple(sorted(progs))


def program_modules_with_function(module_type, function_template):
    """ list the programs implementing a given function

    :param module_type: which type of module it is (write or read)
    :type module_type: str
    :param function_template: a function with the desired signature
    :type function_template: function
    """
    progs = []
    for prog in PROGRAM_MODULE_NAME_DCT:
        module = import_program_module(prog, module_type)
        if hasattr(module, function_template.__name__):
            function = getattr(module, function_template.__name__)

            # make sure the signature matches the template
            assert (inspect.getfullargspec(function) ==
                    inspect.getfullargspec(function_template))

            progs.append(prog)

    return tuple(sorted(progs))


def import_program_module(prog, module_type):
    """ import the module for a program by name

    :param prog: the program name
    :type prog: str
    :param module_type: which type of module it is (write or read)
    :type module_type: str
    """
    assert prog in PROGRAM_MODULE_NAME_DCT
    assert module_type in ('write', 'read')

    module_name = PROGRAM_MODULE_NAME_DCT[prog]

    # do a relative import using the package name, ie 'from . import _psi4'.
    # relative imports require a package name in importlib, ie 'elstruc.write'
    relative_module_name = '.{:s}'.format(module_name)
    package_name = 'elstruct.{:s}'.format(module_type)
    module = importlib.import_module(relative_module_name, package_name)
    return module
