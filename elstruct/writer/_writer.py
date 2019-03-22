""" input writing module

Calls functions from the various program modules. Each module must provide a
function that matches one in the module template -- both the function name and
signature are checked before calling the function. The resulting function
signatures are exactly those in module_template.py with `prog` inserted as the
first required argument.
"""
from elstruct import program_modules as pm
from elstruct import par
from elstruct.writer import module_template

MODULE_NAME = par.Module.WRITER


# energy input writers
def programs():
    """ list of available electronic structure programs

    (must at least implement an energy writer)
    """
    return pm.program_modules_with_functions(
        MODULE_NAME, [module_template.method_list,
                      module_template.basis_list,
                      module_template.energy])


def method_list(prog):
    """ list of available electronic structure methods

    :param prog: the electronic structure program to use as a backend
    :type prog: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.method_list)


def basis_list(prog):
    """ list of available electronic structure basis sets

    :param prog: the electronic structure program to use as a backend
    :type prog: str
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.basis_list)


def energy(prog, method, basis, geom, mult, charge, orb_restricted,
           # molecule options
           mol_options=(),
           # machine options
           memory=1, comment='', machine_options=(),
           # theory options
           scf_options=(), corr_options=()):
    """ energy input string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param method: electronic structure method
    :type method: str
    :param basis: basis set
    :type basis: str
    :param geom: cartesian or z-matrix geometry
    :type geom: tuple
    :param mult: spin multiplicity
    :type mult: int
    :param charge: molecular charge
    :type charge: int
    :param orb_restricted: whether the SCF orbitals are spin-restricted
    :type orb_restricted: bool
    :param mol_options: options for the molecule block
    :type mol_options: tuple[str]
    ;param memory: memory in GB
    :type memory: int
    :param comment: a comment string to be placed at the top of the file
    :type comment: str
    :param machine_options: machine directives (num procs, num threads, etc.)
    :type machine_options: tuple[str]
    :param scf_options: scf method directives
    :type scf_options: tuple[str]
    :param corr_options: correlation method directives
    :type corr_options: tuple[str]
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.energy,
        # *args
        method, basis, geom, mult, charge, orb_restricted,
        # **kwargs
        mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, corr_options=corr_options)


# gradient input writers
def gradient_programs():
    """ list of program modules implementing gradient input writers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.gradient)


def gradient(prog, method, basis, geom, mult, charge, orb_restricted,
             # molecule options
             mol_options=(),
             # machine options
             memory=1, comment='', machine_options=(),
             # theory options
             scf_options=(), corr_options=()):
    """ gradient input string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param method: electronic structure method
    :type method: str
    :param basis: basis set
    :type basis: str
    :param geom: cartesian or z-matrix geometry
    :type geom: tuple
    :param mult: spin multiplicity
    :type mult: int
    :param charge: molecular charge
    :type charge: int
    :param orb_restricted: whether the SCF orbitals are spin-restricted
    :type orb_restricted: bool
    :param mol_options: options for the molecule block
    :type mol_options: tuple[str]
    ;param memory: memory in GB
    :type memory: int
    :param comment: a comment string to be placed at the top of the file
    :type comment: str
    :param machine_options: machine directives (num procs, num threads, etc.)
    :type machine_options: tuple[str]
    :param scf_options: scf method directives
    :type scf_options: tuple[str]
    :param corr_options: correlation method directives
    :type corr_options: tuple[str]
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.gradient,
        # *args
        method, basis, geom, mult, charge, orb_restricted,
        # **kwargs
        mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, corr_options=corr_options)


# hessian input writers
def hessian_programs():
    """ list of program modules implementing hessian input writers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.hessian)


def hessian(prog, method, basis, geom, mult, charge, orb_restricted,
            # molecule options
            mol_options=(),
            # machine options
            memory=1, comment='', machine_options=(),
            # theory options
            scf_options=(), corr_options=()):
    """ hessian input string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param method: electronic structure method
    :type method: str
    :param basis: basis set
    :type basis: str
    :param geom: cartesian or z-matrix geometry
    :type geom: tuple
    :param mult: spin multiplicity
    :type mult: int
    :param charge: molecular charge
    :type charge: int
    :param orb_restricted: whether the SCF orbitals are spin-restricted
    :type orb_restricted: bool
    :param mol_options: options for the molecule block
    :type mol_options: tuple[str]
    ;param memory: memory in GB
    :type memory: int
    :param comment: a comment string to be placed at the top of the file
    :type comment: str
    :param machine_options: machine directives (num procs, num threads, etc.)
    :type machine_options: tuple[str]
    :param scf_options: scf method directives
    :type scf_options: tuple[str]
    :param corr_options: correlation method directives
    :type corr_options: tuple[str]
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.hessian,
        # *args
        method, basis, geom, mult, charge, orb_restricted,
        # **kwargs
        mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, corr_options=corr_options)


# optimization input writers
def optimization_programs():
    """ list of program modules implementing optimization input writers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.optimization)


def optimization(prog, method, basis, geom, mult, charge, orb_restricted,
                 # molecule options
                 mol_options=(),
                 # machine options
                 memory=1, comment='', machine_options=(),
                 # theory options
                 scf_options=(), corr_options=(),
                 # molecule/optimization options
                 frozen_coordinates=None, opt_options=()):
    """ optimization input string

    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param method: electronic structure method
    :type method: str
    :param basis: basis set
    :type basis: str
    :param geom: cartesian or z-matrix geometry
    :type geom: tuple
    :param mult: spin multiplicity
    :type mult: int
    :param charge: molecular charge
    :type charge: int
    :param orb_restricted: whether the SCF orbitals are spin-restricted
    :type orb_restricted: bool
    :param mol_options: options for the molecule block
    :type mol_options: tuple[str]
    ;param memory: memory in GB
    :type memory: int
    :param comment: a comment string to be placed at the top of the file
    :type comment: str
    :param machine_options: machine directives (num procs, num threads, etc.)
    :type machine_options: tuple[str]
    :param scf_options: scf method directives
    :type scf_options: tuple[str]
    :param corr_options: correlation method directives
    :type corr_options: tuple[str]
    :param frozen_coordinates: only with z-matrix geometries; list of
        coordinate names to freeze
    :type fozen_coordinates: tuple[str]
    :param opt_options: geometry optimization routine directives
    :type opt_options: tuple[str]
    """
    return pm.call_module_function(
        prog, MODULE_NAME, module_template.optimization,
        # *args
        method, basis, geom, mult, charge, orb_restricted,
        # **kwargs
        mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, corr_options=corr_options,
        frozen_coordinates=frozen_coordinates, opt_options=opt_options)
