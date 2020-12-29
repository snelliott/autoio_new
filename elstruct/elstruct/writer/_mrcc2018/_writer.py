""" mrcc2018 writer module """
import os
import automol
import autowrite as aw
import elstruct.par
import elstruct.option
from elstruct import template
from elstruct.writer._mrcc2018 import par

PROG = elstruct.par.Program.MRCC2018

# set the path to the template files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


# mako template keys
class MRCC2018Reference():
    """ _ """
    RHF = 'rhf'
    UHF = 'uhf'
    ROHF = 'rohf'


class JobKey():
    """ _ """
    ENERGY = 'energy'
    OPTIMIZATION = 'optimization'
    HESSIAN = 'hessian'


class TemplateKey():
    """ mako template keys """
    JOB_KEY = 'job_key'
    COMMENT = 'comment'
    MEMORY = 'memory'
    MACHINE_OPTIONS = 'machine_options'
    MOL_OPTIONS = 'mol_options'
    GEOM = 'geom'
    ZMAT_VALS = 'zmat_val_str'
    CHARGE = 'charge'
    MULT = 'mult'
    BASIS = 'basis'
    SCF_METHOD = 'scf_method'
    SCF_OPTIONS = 'scf_options'
    CASSCF_OPTIONS = 'casscf_options'
    CORR_METHOD = 'corr_method'
    CORR_OPTIONS = 'corr_options'
    JOB_OPTIONS = 'job_options'
    GEN_LINES = 'gen_lines'
    COORD_SYS = 'coord_sys'


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
        charge=charge, orb_restricted=orb_restricted,
        mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        gen_lines=gen_lines,
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
        gen_lines=gen_lines,
        job_options=job_options,
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
        gen_lines=gen_lines,
        frozen_coordinates=frozen_coordinates, job_options=job_options,
        saddle=saddle
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

    # Set the spin
    singlet = (mult == 1)

    # Set the theoretical method
    mrcc_scf_method = (MRCC2018Reference.RHF if orb_restricted else
                       MRCC2018Reference.UHF)
    mrcc_corr_method = (
        elstruct.par.program_method_name(PROG, method, singlet)
        if elstruct.par.Method.is_correlated(method) else '')
    mrcc_basis = elstruct.par.program_basis_name(PROG, basis)

    # Build the geometry
    geo_str, zmat_val_str = _geometry_strings(geo)

    # Check options
    scf_options = _evaluate_options(scf_options)
    casscf_options = _evaluate_options(casscf_options)
    job_options = _evaluate_options(job_options)
    _ = mol_options
    _ = machine_options
    _ = gen_lines

    # Set the coordinate system
    if automol.geom.is_valid(geo):
        coord_sys = 'xyz'
    elif automol.zmatrix.is_valid(geo):
        coord_sys = 'zmat'

    # No TS optimizer based on manual
    assert not saddle

    # No Frozen coordinates allowed based on manual
    assert not frozen_coordinates

    # Set the gen lines blocks
    # if gen_lines is not None:
    #     gen_lines = '\n'.join(gen_lines[1]) if 1 in gen_lines else ''
    # else:
    #     gen_lines = ''

    fill_dct = {
        TemplateKey.JOB_KEY: job_key,
        TemplateKey.COMMENT: comment,
        TemplateKey.MEMORY: memory,
        TemplateKey.GEOM: geo_str,
        TemplateKey.ZMAT_VALS: zmat_val_str,
        TemplateKey.CHARGE: charge,
        TemplateKey.MULT: mult,
        TemplateKey.BASIS: mrcc_basis,
        TemplateKey.SCF_METHOD: mrcc_scf_method,
        TemplateKey.SCF_OPTIONS: '\n'.join(scf_options),
        TemplateKey.CORR_METHOD: mrcc_corr_method,
        TemplateKey.CORR_OPTIONS: '\n'.join(corr_options),
        TemplateKey.JOB_OPTIONS: '\n'.join(job_options),
        TemplateKey.COORD_SYS: coord_sys
    }
    return fill_dct


def _geometry_strings(geo):
    """ Build the string for the input geometry

        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
        :param frozen_coordinates: only with z-matrix geometries; list of
            coordinate names to freeze
        :type fozen_coordinates: tuple[str]
        :param job_key: job contained in the inpit file
        :type job_key: str
        :rtype: (str, str)
    """

    if automol.geom.is_valid(geo):
        geo_str = automol.geom.string(geo)
        zmat_val_str = ''
    elif automol.zmatrix.is_valid(geo):
        zma = geo
        symbs = automol.zmatrix.symbols(zma)
        key_mat = automol.zmatrix.key_matrix(zma, shift=1)
        name_mat = automol.zmatrix.name_matrix(zma)
        val_dct = automol.zmatrix.values(zma, angstrom=True, degree=True)

        geo_str = aw.zmatrix.matrix_block(symbs, key_mat, name_mat)
        zmat_val_str = aw.zmatrix.setval_block(val_dct)
    else:
        raise ValueError("Invalid geometry value:\n{0}".format(geo))

    return geo_str, zmat_val_str


def _evaluate_options(opts):
    opts = list(opts)
    for idx, opt in enumerate(opts):
        if elstruct.option.is_valid(opt):
            name = elstruct.option.name(opt)
            assert name in par.OPTION_NAMES
            opts[idx] = par.MRCC2018_OPTION_EVAL_DCT[name](opt)
    return tuple(opts)
