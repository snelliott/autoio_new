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
        MODULE_NAME, [module_template.energy])


def methods(prog):
    """ list of available electronic structure methods

    :param prog: the electronic structure program to use as a backend
    :type prog: str
    """
    return par.program_methods(prog)


def bases(prog):
    """ list of available electronic structure basis sets

    :param prog: the electronic structure program to use as a backend
    :type prog: str
    """
    return par.program_bases(prog)


def method_orbital_types(prog, method, singlet):
    """ list of available orbital restrictions for a given method

    :param prog: the electronic structure program to use as a backend
    :type prog: str
    :param method: electronic structure method
    :type method: str
    :param singlet: whether or not the target is a singlet (closed shell)
    :type singlet: bool
    """
    return par.program_method_orbital_types(prog, method, singlet)


def energy(geom, charge, mult, method, basis, prog,
           # molecule options
           mol_options=(),
           # machine options
           memory=1, comment='', machine_options=(),
           # theory options
           orb_type='RU',
           scf_options=(), casscf_options=(), corr_options=(),
           # generic options
           gen_lines=None):
    """ energy input string

    :param geom: cartesian or z-matrix geometry
    :type geom: tuple
    :param charge: molecular charge
    :type charge: int
    :param mult: spin multiplicity
    :type mult: int
    :param method: electronic structure method
    :type method: str
    :param basis: basis set
    :type basis: str
    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param mol_options: options for the molecule block
    :type mol_options: tuple[str]
    ;param memory: memory in GB
    :type memory: int
    :param comment: a comment string to be placed at the top of the file
    :type comment: str
    :param machine_options: machine directives (num procs, num threads, etc.)
    :type machine_options: tuple[str]
    :param orb_type: 'R' indicates restricted orbitals, 'U' indicates
        unrestricted orbitals; can also be 'RR', 'RU', or 'UU' where the first
        character sets R/U for singlets and the second sets R/U for multiplets
    :type orb_type: str
    :param scf_options: scf method directives
    :type scf_options: tuple[str]
    :param casscf_options: casscf method directives
    :type casscf_options: tuple[str]
    :param corr_options: correlation method directives
    :type corr_options: tuple[str]
    :param gen_lines: generic lines for the input file
    :type gen_lines: dct[idx]=[str]
    """
    prog, method, basis, orb_restricted = _process_theory_specifications(
        prog, method, basis, mult, orb_type)

    return pm.call_module_function(
        prog, MODULE_NAME, module_template.energy,
        # *args
        geom, charge, mult, method, basis,
        # **kwargs
        mol_options=mol_options, memory=memory, comment=comment,
        machine_options=machine_options, orb_restricted=orb_restricted,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        gen_lines=gen_lines)


# gradient input writers
def gradient_programs():
    """ list of program modules implementing gradient input writers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.gradient)


def gradient(geom, charge, mult, method, basis, prog,
             # molecule options
             mol_options=(),
             # machine options
             memory=1, comment='', machine_options=(),
             # theory options
             orb_type='RU',
             scf_options=(), casscf_options=(), corr_options=(),
             # generic options
             gen_lines=None,
             # job options
             job_options=()):
    """ gradient input string

    :param geom: cartesian or z-matrix geometry
    :type geom: tuple
    :param charge: molecular charge
    :type charge: int
    :param mult: spin multiplicity
    :type mult: int
    :param method: electronic structure method
    :type method: str
    :param basis: basis set
    :type basis: str
    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param mol_options: options for the molecule block
    :type mol_options: tuple[str]
    ;param memory: memory in GB
    :type memory: int
    :param comment: a comment string to be placed at the top of the file
    :type comment: str
    :param machine_options: machine directives (num procs, num threads, etc.)
    :type machine_options: tuple[str]
    :param orb_type: 'R' indicates restricted orbitals, 'U' indicates
        unrestricted orbitals; can also be 'RR', 'RU', or 'UU' where the first
        character sets R/U for singlets and the second sets R/U for multiplets
    :type orb_type: str
    :param scf_options: scf method directives
    :type scf_options: tuple[str]
    :param casscf_options: casscf method directives
    :type casscf_options: tuple[str]
    :param corr_options: correlation method directives
    :type corr_options: tuple[str]
    :param gen_lines: generic lines for the input file
    :type gen_lines: dct[idx]=[str]
    """
    prog, method, basis, orb_restricted = _process_theory_specifications(
        prog, method, basis, mult, orb_type)

    return pm.call_module_function(
        prog, MODULE_NAME, module_template.gradient,
        # *args
        geom, charge, mult, method, basis,
        # **kwargs
        mol_options=mol_options, memory=memory, comment=comment,
        machine_options=machine_options, orb_restricted=orb_restricted,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        gen_lines=gen_lines, job_options=job_options)


# hessian input writers
def hessian_programs():
    """ list of program modules implementing hessian input writers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.hessian)


def hessian(geom, charge, mult, method, basis, prog,
            # molecule options
            mol_options=(),
            # machine options
            memory=1, comment='', machine_options=(),
            # theory options
            orb_type='RU',
            scf_options=(), casscf_options=(), corr_options=(),
            # generic options
            gen_lines=None,
            # job options
            job_options=()):
    """ hessian input string

    :param geom: cartesian or z-matrix geometry
    :type geom: tuple
    :param charge: molecular charge
    :type charge: int
    :param mult: spin multiplicity
    :type mult: int
    :param method: electronic structure method
    :type method: str
    :param basis: basis set
    :type basis: str
    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param mol_options: options for the molecule block
    :type mol_options: tuple[str]
    ;param memory: memory in GB
    :type memory: int
    :param comment: a comment string to be placed at the top of the file
    :type comment: str
    :param machine_options: machine directives (num procs, num threads, etc.)
    :type machine_options: tuple[str]
    :param orb_type: 'R' indicates restricted orbitals, 'U' indicates
        unrestricted orbitals; can also be 'RR', 'RU', or 'UU' where the first
        character sets R/U for singlets and the second sets R/U for multiplets
    :type orb_type: str
    :param scf_options: scf method directives
    :type scf_options: tuple[str]
    :param casscf_options: casscf method directives
    :type casscf_options: tuple[str]
    :param corr_options: correlation method directives
    :type corr_options: tuple[str]
    :param gen_lines: generic lines for the input file
    :type gen_lines: dct[idx]=[str]
    """
    prog, method, basis, orb_restricted = _process_theory_specifications(
        prog, method, basis, mult, orb_type)

    return pm.call_module_function(
        prog, MODULE_NAME, module_template.hessian,
        # *args
        geom, charge, mult, method, basis,
        # **kwargs
        mol_options=mol_options, memory=memory, comment=comment,
        machine_options=machine_options, orb_restricted=orb_restricted,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        gen_lines=gen_lines, job_options=job_options)


# vpt2 input writers
def vpt2_programs():
    """ list of program modules implementing hessian input writers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.vpt2)


def vpt2(geom, charge, mult, method, basis, prog,
         # molecule options
         mol_options=(),
         # machine options
         memory=1, comment='', machine_options=(),
         # theory options
         orb_type=None,
         scf_options=(), casscf_options=(), corr_options=(),
         # generic options
         gen_lines=None,
         # job options
         job_options=()):
    """ hessian input string

    :param geom: cartesian or z-matrix geometry
    :type geom: tuple
    :param charge: molecular charge
    :type charge: int
    :param mult: spin multiplicity
    :type mult: int
    :param method: electronic structure method
    :type method: str
    :param basis: basis set
    :type basis: str
    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param mol_options: options for the molecule block
    :type mol_options: tuple[str]
    ;param memory: memory in GB
    :type memory: int
    :param comment: a comment string to be placed at the top of the file
    :type comment: str
    :param machine_options: machine directives (num procs, num threads, etc.)
    :type machine_options: tuple[str]
    :param orb_type: 'R' indicates restricted orbitals, 'U' indicates
        unrestricted orbitals; can also be 'RR', 'RU', or 'UU' where the first
        character sets R/U for singlets and the second sets R/U for multiplets
    :type orb_type: str
    :param scf_options: scf method directives
    :type scf_options: tuple[str]
    :param casscf_options: casscf method directives
    :type casscf_options: tuple[str]
    :param corr_options: correlation method directives
    :type corr_options: tuple[str]
    :param gen_lines: generic lines for the input file
    :type gen_lines: tuple[str]
    :type gen_lines: dct[idx]=[str]
    """
    prog, method, basis, orb_restricted = _process_theory_specifications(
        prog, method, basis, mult, orb_type)

    return pm.call_module_function(
        prog, MODULE_NAME, module_template.vpt2,
        # *args
        geom, charge, mult, method, basis,
        # **kwargs
        mol_options=mol_options, memory=memory, comment=comment,
        machine_options=machine_options, orb_restricted=orb_restricted,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        gen_lines=gen_lines, job_options=job_options)


# irc input writers
def irc_programs():
    """ list of program modules implementing optimization input writers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.irc)


def irc(geom, charge, mult, method, basis, prog,
        # molecule options
        mol_options=(),
        # machine options
        memory=1, comment='', machine_options=(),
        # theory options
        orb_type=None,
        scf_options=(), casscf_options=(), corr_options=(),
        # generic options
        gen_lines=None,
        # job options
        job_options=(), frozen_coordinates=(), irc_direction=None):
    """ irc input string

    :param geom: cartesian or z-matrix geometry
    :type geom: tuple
    :param charge: molecular charge
    :type charge: int
    :param mult: spin multiplicity
    :type mult: int
    :param method: electronic structure method
    :type method: str
    :param basis: basis set
    :type basis: str
    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param mol_options: options for the molecule block
    :type mol_options: tuple[str]
    ;param memory: memory in GB
    :type memory: int
    :param comment: a comment string to be placed at the top of the file
    :type comment: str
    :param machine_options: machine directives (num procs, num threads, etc.)
    :type machine_options: tuple[str]
    :param orb_type: 'R' indicates restricted orbitals, 'U' indicates
        unrestricted orbitals; can also be 'RR', 'RU', or 'UU' where the first
        character sets R/U for singlets and the second sets R/U for multiplets
    :type orb_type: str
    :param scf_options: scf method directives
    :type scf_options: tuple[str]
    :param casscf_options: casscf method directives
    :type casscf_options: tuple[str]
    :param corr_options: correlation method directives
    :type corr_options: tuple[str]
    :param job_options: geometry optimization routine directives
    :type job_options: tuple[str]
    :param frozen_coordinates: only with z-matrix geometries; list of
        coordinate names to freeze
    :type fozen_coordinates: tuple[str]
    :param irc_direction: direction along imaginary mode eigenvector to move
    :type irc_direction: string
    :param gen_lines: generic lines for the input file
    :type gen_lines: dct[idx]=[str]
    """
    prog, method, basis, orb_restricted = _process_theory_specifications(
        prog, method, basis, mult, orb_type)

    return pm.call_module_function(
        prog, MODULE_NAME, module_template.irc,
        # *args
        geom, charge, mult, method, basis,
        # **kwargs
        mol_options=mol_options, memory=memory, comment=comment,
        machine_options=machine_options, orb_restricted=orb_restricted,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        gen_lines=gen_lines,
        job_options=job_options, frozen_coordinates=frozen_coordinates,
        irc_direction=irc_direction)


# optimization input writers
def optimization_programs():
    """ list of program modules implementing optimization input writers
    """
    return pm.program_modules_with_function(
        MODULE_NAME, module_template.optimization)


def optimization(geom, charge, mult, method, basis, prog,
                 # molecule options
                 mol_options=(),
                 # machine options
                 memory=1, comment='', machine_options=(),
                 # theory options
                 orb_type=None,
                 scf_options=(), casscf_options=(), corr_options=(),
                 # generic options
                 gen_lines=None,
                 # job options
                 job_options=(), frozen_coordinates=(), saddle=False):
    """ optimization input string

    :param geom: cartesian or z-matrix geometry
    :type geom: tuple
    :param charge: molecular charge
    :type charge: int
    :param mult: spin multiplicity
    :type mult: int
    :param method: electronic structure method
    :type method: str
    :param basis: basis set
    :type basis: str
    :param prog: electronic structure program to use as a backend
    :type prog: str
    :param mol_options: options for the molecule block
    :type mol_options: tuple[str]
    ;param memory: memory in GB
    :type memory: int
    :param comment: a comment string to be placed at the top of the file
    :type comment: str
    :param machine_options: machine directives (num procs, num threads, etc.)
    :type machine_options: tuple[str]
    :param orb_type: 'R' indicates restricted orbitals, 'U' indicates
        unrestricted orbitals; can also be 'RR', 'RU', or 'UU' where the first
        character sets R/U for singlets and the second sets R/U for multiplets
    :type orb_type: str
    :param scf_options: scf method directives
    :type scf_options: tuple[str]
    :param casscf_options: casscf method directives
    :type casscf_options: tuple[str]
    :param corr_options: correlation method directives
    :type corr_options: tuple[str]
    :param job_options: geometry optimization routine directives
    :type job_options: tuple[str]
    :param frozen_coordinates: only with z-matrix geometries; list of
        coordinate names to freeze
    :type fozen_coordinates: tuple[str]
    :param saddle: optimize a saddle point?
    :type saddle: bool
    :param gen_lines: generic lines for the input file
    :type gen_lines: dct[idx]=[str]
    """
    prog, method, basis, orb_restricted = _process_theory_specifications(
        prog, method, basis, mult, orb_type)

    return pm.call_module_function(
        prog, MODULE_NAME, module_template.optimization,
        # *args
        geom, charge, mult, method, basis,
        # **kwargs
        mol_options=mol_options, memory=memory, comment=comment,
        machine_options=machine_options, orb_restricted=orb_restricted,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        gen_lines=gen_lines,
        job_options=job_options, frozen_coordinates=frozen_coordinates,
        saddle=saddle)


def _process_theory_specifications(prog, method, basis, mult, orb_type):
    assert par.is_program(prog)

    # determine the orbital restriction
    singlet = (mult == 1)
    if len(orb_type) == 2:
        orb_type = orb_type[0] if singlet else orb_type[1]

    assert orb_type in ('R', 'U')
    orb_restricted = (orb_type == 'R')

    # for non-standard DFT/Basis, the user can input whatever they want
    if not par.Method.is_nonstandard_dft(method):
        assert par.is_program_method(prog, method)

        print('eltest', prog, method, singlet, orb_type)
        assert par.is_program_method_orbital_type(
            prog, method, singlet, orb_type)

        prog = par.standard_case(prog)
        method = par.standard_case(method)

    if not par.Basis.is_nonstandard_basis(basis):
        assert par.is_program_basis(prog, basis)
        basis = par.standard_case(basis)

    return prog, method, basis, orb_restricted
