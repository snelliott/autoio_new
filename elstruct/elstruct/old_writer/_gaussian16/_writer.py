""" gaussian16 writer module """

import os
import automol
import autowrite as aw
import elstruct.par
import elstruct.option
from elstruct import template
from elstruct import pclass
from elstruct.writer._gaussian16 import par


PROG = elstruct.par.Program.GAUSSIAN16

# set the path to the template files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


# mako template keys
class GAUSSIAN16Reference():
    """ _ """
    RHF = 'rhf'
    UHF = 'uhf'
    ROHF = 'rohf'


class JobKey():
    """ _ """
    ENERGY = 'energy'
    OPTIMIZATION = 'optimization'
    GRADIENT = 'gradient'
    HESSIAN = 'hessian'
    VPT2 = 'vpt2'
    IRC = 'irc'
    MOLPROP = 'molec_properties'


class TemplateKey():
    """ mako template keys """
    # machine
    MEMORY = 'memory'
    MACHINE_OPTIONS = 'machine_options'
    # theoretical method
    REFERENCE = 'reference'
    METHOD = 'method'
    BASIS = 'basis'
    SCF_OPTIONS = 'scf_options'
    SCF_GUESS_OPTIONS = 'scf_guess_options'
    # molecule / state
    MOL_OPTIONS = 'mol_options'
    CHARGE = 'charge'
    MULT = 'mult'
    GEOM = 'geom'
    ZMAT_VAR_VALS = 'zmat_var_vals'
    ZMAT_CONST_VALS = 'zmat_const_vals'
    # job
    COMMENT = 'comment'
    JOB_KEY = 'job_key'
    JOB_OPTIONS = 'job_options'
    GEN_LINES = 'gen_lines'


def energy(geo, charge, mult, method, basis,
           # molecule options
           mol_options=(),
           # machine options
           memory=1, comment='', machine_options=(),
           # theory options
           orb_restricted=None,
           scf_options=(), casscf_options=(), corr_options=(),
           # generic options
           gen_lines=None):
    """ Writes an input file string for an electronic energy calculation
        for a specified electronic structure program.

        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
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
        :param machine_options: machine directives
            (num procs, num threads, etc.)
        :type machine_options: tuple[str]
        :param orb_type: 'R' indicates restricted orbitals, 'U' indicates
            unrestricted orbitals; can also be 'RR', 'RU', or 'UU'.
            Where first (second) character sets R/U for singlets (multiplets)
        :type orb_type: str
        :param scf_options: scf method directives
        :type scf_options: tuple[str]
        :param casscf_options: casscf method directives
        :type casscf_options: tuple[str]
        :param corr_options: correlation method directives
        :type corr_options: tuple[str]
        :param gen_lines: generic lines for the input file
        :type gen_lines: dict[idx:str]
    """
    job_key = JobKey.ENERGY
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geo=geo, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        gen_lines=gen_lines,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def gradient(geo, charge, mult, method, basis,
             # molecule options
             mol_options=(),
             # machine options
             memory=1, comment='', machine_options=(),
             # theory options
             orb_restricted=None,
             scf_options=(), casscf_options=(), corr_options=(),
             # generic options
             gen_lines=None,
             # job options
             job_options=()):
    """ Writes an input file string for a gradient calculation
        for a specified electronic structure program.

        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
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
        :param machine_options: machine directives
            (num procs, num threads, etc.)
        :type machine_options: tuple[str]
        :param orb_type: 'R' indicates restricted orbitals, 'U' indicates
            unrestricted orbitals; can also be 'RR', 'RU', or 'UU'.
            Where first (second) character sets R/U for singlets (multiplets)
        :type orb_type: str
        :param scf_options: scf method directives
        :type scf_options: tuple[str]
        :param casscf_options: casscf method directives
        :type casscf_options: tuple[str]
        :param corr_options: correlation method directives
        :type corr_options: tuple[str]
        :param gen_lines: generic lines for the input file
        :type gen_lines: dict[idx:str]
    """
    job_key = JobKey.GRADIENT
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geo=geo, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        job_options=job_options, gen_lines=gen_lines,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def hessian(geo, charge, mult, method, basis,
            # molecule options
            mol_options=(),
            # machine options
            memory=1, comment='', machine_options=(),
            # theory options
            orb_restricted=None,
            scf_options=(), casscf_options=(), corr_options=(),
            # generic options
            gen_lines=None,
            # job options
            job_options=()):
    """ Writes an input file string for a Hessian calculation
        for a specified electronic structure program.

        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
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
        :param machine_options: machine directives
            (num procs, num threads, etc.)
        :type machine_options: tuple[str]
        :param orb_type: 'R' indicates restricted orbitals, 'U' indicates
            unrestricted orbitals; can also be 'RR', 'RU', or 'UU'.
            Where first (second) character sets R/U for singlets (multiplets)
        :type orb_type: str
        :param scf_options: scf method directives
        :type scf_options: tuple[str]
        :param casscf_options: casscf method directives
        :type casscf_options: tuple[str]
        :param corr_options: correlation method directives
        :type corr_options: tuple[str]
        :param gen_lines: generic lines for the input file
        :type gen_lines: dict[idx:str]
    """
    job_key = JobKey.HESSIAN
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geo=geo, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        job_options=job_options, gen_lines=gen_lines,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def vpt2(geo, charge, mult, method, basis,
         # molecule options
         mol_options=(),
         # machine options
         memory=1, comment='', machine_options=(),
         # theory options
         orb_restricted=None,
         scf_options=(), casscf_options=(), corr_options=(),
         # generic options
         gen_lines=None,
         # job options
         job_options=()):
    """ hessian input string
    """
    job_key = JobKey.VPT2
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geo=geo, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        job_options=job_options, gen_lines=gen_lines,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def molec_properties(geo, charge, mult, method, basis,
                     # molecule options
                     mol_options=(),
                     # machine options
                     memory=1, comment='', machine_options=(),
                     # theory options
                     orb_restricted=None,
                     scf_options=(), casscf_options=(), corr_options=(),
                     # generic options
                     gen_lines=None,
                     # job options
                     job_options=()):
    """ Writes an input file string for molecular properties calculations,
        including the dipole moment and polarizability,
        for a specified electronic structure program.

        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
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
        :param machine_options: machine directives
            (num procs, num threads, etc.)
        :type machine_options: tuple[str]
        :param orb_type: 'R' indicates restricted orbitals, 'U' indicates
            unrestricted orbitals; can also be 'RR', 'RU', or 'UU'.
            Where first (second) character sets R/U for singlets (multiplets)
        :type orb_type: str
        :param scf_options: scf method directives
        :type scf_options: tuple[str]
        :param casscf_options: casscf method directives
        :type casscf_options: tuple[str]
        :param corr_options: correlation method directives
        :type corr_options: tuple[str]
        :param gen_lines: generic lines for the input file
        :type gen_lines: dict[idx:str]
    """
    job_key = JobKey.MOLPROP
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geo=geo, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        job_options=job_options, gen_lines=gen_lines,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def irc(geo, charge, mult, method, basis,
        # molecule options
        mol_options=(),
        # machine options
        memory=1, comment='', machine_options=(),
        # theory options
        orb_restricted=None,
        scf_options=(), casscf_options=(), corr_options=(),
        # generic options
        gen_lines=None,
        # job options
        job_options=(), frozen_coordinates=()):
    """ Writes an input file string for an Intrinsic Reaction Coordinate
        calculation for a specified electronic structure program.

        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
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
        :param machine_options: machine directives
            (num procs, num threads, etc.)
        :type machine_options: tuple[str]
        :param orb_type: 'R' indicates restricted orbitals, 'U' indicates
            unrestricted orbitals; can also be 'RR', 'RU', or 'UU'.
            Where first (second) character sets R/U for singlets (multiplets)
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
        :param gen_lines: generic lines for the input file
        :type gen_lines: dict[idx:str]
    """
    job_key = JobKey.IRC
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geo=geo, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        job_options=job_options, frozen_coordinates=frozen_coordinates,
        gen_lines=gen_lines,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def optimization(geo, charge, mult, method, basis,
                 # molecule options
                 mol_options=(),
                 # machine options
                 memory=1, comment='', machine_options=(),
                 # theory options
                 orb_restricted=None,
                 scf_options=(), casscf_options=(), corr_options=(),
                 # generic options
                 gen_lines=None,
                 # job options
                 job_options=(), frozen_coordinates=(), saddle=False):
    """ Writes an input file string for a geometry optimization
        calculation for a specified electronic structure program.

        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
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
        :param machine_options: machine directives
            (num procs, num threads, etc.)
        :type machine_options: tuple[str]
        :param orb_type: 'R' indicates restricted orbitals, 'U' indicates
            unrestricted orbitals; can also be 'RR', 'RU', or 'UU'.
            Where first (second) character sets R/U for singlets (multiplets)
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
        :type gen_lines: dict[idx:str]
    """
    job_key = JobKey.OPTIMIZATION
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geo=geo, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        job_options=job_options, frozen_coordinates=frozen_coordinates,
        saddle=saddle, gen_lines=gen_lines,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


# helper functions
def _fillvalue_dictionary(job_key, method, basis, geo, mult, charge,
                          orb_restricted, mol_options, memory, comment,
                          machine_options,
                          scf_options, casscf_options, corr_options,
                          job_options=(), frozen_coordinates=(),
                          saddle=False,
                          gen_lines=None):
    """ Build a Python dictionary with parameters and values
        that can be used to fill a Mako template for writing
        an electronic structure input file.

        :param job_key: job contained in the inpit file
        :type job_key: str
        :param method: electronic structure method
        :type method: str
        :param basis: basis set
        :type basis: str
        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
        :param mult: spin multiplicity
        :type mult: int
        :param charge: molecular charge
        :type charge: int
        :param orb_restricted: parameter designating if restriced refrence used
        :type orb_restricted: bool
        :param mol_options: options for the molecule block
        :type mol_options: tuple[str]
        ;param memory: memory in GB
        :type memory: int
        :param comment: a comment string to be placed at the top of the file
        :type comment: str
        :param machine_options: machine directives
            (num procs, num threads, etc.)
        :type machine_options: tuple[str]
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
        :type gen_lines: dict[idx:str]
    """

    reference = _reference(method, mult, orb_restricted)
    geo_str, zmat_var_val_str, zmat_const_val_str = _geometry_strings(
        geo, frozen_coordinates)

    if elstruct.par.Method.is_correlated(method):
        assert not corr_options

    if (reference == GAUSSIAN16Reference.ROHF and
            job_key in (JobKey.GRADIENT, JobKey.HESSIAN)):
        job_options = list(job_options)
        job_options.insert(0, 'EnOnly')

    gaussian16_method = elstruct.par.program_method_name(PROG, method)
    gaussian16_basis = elstruct.par.program_basis_name(PROG, basis)

    # in the case of Hartree-Fock, swap the method for the reference name
    if method == elstruct.par.Method.HF[0]:
        gaussian16_method = reference
        reference = ''

    scf_guess_options, scf_options = _intercept_scf_guess_option(scf_options)
    scf_guess_options = _evaluate_options(scf_guess_options)
    scf_options = _evaluate_options(scf_options)
    casscf_options = _evaluate_options(casscf_options)
    job_options = _evaluate_options(job_options)

    if saddle:
        job_options += ('CALCFC', 'TS', 'NOEIGEN', 'MAXCYCLES=60')

    # Set the gen lines blocks
    if gen_lines is not None:
        gen_lines = '\n'.join(gen_lines[1]) if 1 in gen_lines else ''
    else:
        gen_lines = ''

    fill_dct = {
        TemplateKey.MEMORY: memory,
        TemplateKey.MACHINE_OPTIONS: '\n'.join(machine_options),
        TemplateKey.REFERENCE: reference,
        TemplateKey.METHOD: gaussian16_method,
        TemplateKey.BASIS: gaussian16_basis,
        TemplateKey.SCF_OPTIONS: ','.join(scf_options),
        TemplateKey.SCF_GUESS_OPTIONS: ','.join(scf_guess_options),
        TemplateKey.MOL_OPTIONS: ','.join(mol_options),
        TemplateKey.COMMENT: comment,
        TemplateKey.CHARGE: charge,
        TemplateKey.MULT: mult,
        TemplateKey.GEOM: geo_str,
        TemplateKey.ZMAT_VAR_VALS: zmat_var_val_str,
        TemplateKey.ZMAT_CONST_VALS: zmat_const_val_str,
        TemplateKey.JOB_KEY: job_key,
        TemplateKey.JOB_OPTIONS: ','.join(job_options),
        TemplateKey.GEN_LINES: gen_lines,
    }
    return fill_dct


def _geometry_strings(geo, frozen_coordinates):
    """ Build the string for the input geometry

        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
        :param frozen_coordinates: only with z-matrix geometries; list of
            coordinate names to freeze
        :type fozen_coordinates: tuple[str]
        :rtype: (str, str)
    """

    if automol.geom.is_valid(geo):
        geo_str = automol.geom.string(geo)
        zmat_vval_str = ''
        zmat_cval_str = ''
    elif automol.zmatrix.is_valid(geo):
        zma = geo
        symbs = automol.zmatrix.symbols(zma)
        key_mat = automol.zmatrix.key_matrix(zma, shift=1)
        name_mat = automol.zmatrix.name_matrix(zma)
        val_dct = automol.zmatrix.values(zma, angstrom=True, degree=True)
        geo_str = aw.zmatrix.matrix_block(symbs, key_mat, name_mat)

        vval_dct = {key: val for key, val in val_dct.items()
                    if key not in frozen_coordinates}
        cval_dct = {key: val for key, val in val_dct.items()
                    if key in frozen_coordinates}

        zmat_vval_str = aw.zmatrix.setval_block(
            vval_dct, setval_sign=' ').strip()
        zmat_cval_str = aw.zmatrix.setval_block(
            cval_dct, setval_sign=' ').strip()
    else:
        raise ValueError("Invalid geometry value:\n{0}".format(geo))

    return geo_str, zmat_vval_str, zmat_cval_str


def _reference(method, mult, orb_restricted):
    if elstruct.par.Method.is_dft(method):
        reference = ''
    elif mult != 1:
        reference = (GAUSSIAN16Reference.ROHF
                     if orb_restricted else GAUSSIAN16Reference.UHF)
    else:
        assert mult == 1 and orb_restricted is True
        reference = GAUSSIAN16Reference.RHF
    return reference


def _intercept_scf_guess_option(scf_opts):
    guess_opts = []
    ret_scf_opts = []
    for opt in scf_opts:
        if (elstruct.option.is_valid(opt) and opt in
                pclass.values(elstruct.par.Option.Scf.Guess)):
            guess_opts.append(opt)
        else:
            ret_scf_opts.append(opt)
    return guess_opts, ret_scf_opts


def _evaluate_options(opts):
    opts = list(opts)
    for idx, opt in enumerate(opts):
        if elstruct.option.is_valid(opt):
            name = elstruct.option.name(opt)
            assert name in par.OPTION_NAMES
            opts[idx] = par.GAUSSIAN16_OPTION_EVAL_DCT[name](opt)
    return tuple(opts)
