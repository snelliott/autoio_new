""" cfour2 writer module """
import os
import automol
import autowrite as aw
import elstruct.par
import elstruct.option
from elstruct import template
from elstruct.writer._cfour2 import par

PROG = elstruct.par.Program.CFOUR2

# set the path to the template files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


# mako template keys
class Cfour2Reference():
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


class TemplateKey():
    """ mako template keys """
    JOB_KEY = 'job_key'
    COMMENT = 'comment'
    MEMORY = 'memory'
    MACHINE_OPTIONS = 'machine_options'
    MOL_OPTIONS = 'mol_options'
    CHARGE = 'charge'
    MULT = 'mult'
    GEOM = 'geom'
    ZMAT_VAR_VALS = 'zmat_var_vals'
    BASIS = 'basis'
    REFERENCE = 'reference'
    SCF_OPTIONS = 'scf_options'
    CASSCF_OPTIONS = 'casscf_options'
    CORR_OPTIONS = 'corr_options'
    METHOD = 'method'
    JOB_OPTIONS = 'job_options'
    GEN_LINES = 'gen_lines'
    SADDLE = 'saddle'
    NUMERICAL = 'numerical'
    COORD_SYS = 'coord_sys'


def energy(geom, charge, mult, method, basis,
           # molecule options
           mol_options=(),
           # machine options
           memory=1, comment='', machine_options=(),
           # theory options
           orb_restricted=None,
           scf_options=(), casscf_options=(), corr_options=(),
           # generic options
           gen_lines=None):
    """ energy input string
    """
    job_key = JobKey.ENERGY
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        gen_lines=gen_lines,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def gradient(geom, charge, mult, method, basis,
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
    """ gradient input string
    """
    job_key = JobKey.GRADIENT
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        gen_lines=gen_lines,
        job_options=job_options,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def hessian(geom, charge, mult, method, basis,
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
    job_key = JobKey.HESSIAN
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options,
        corr_options=corr_options,
        gen_lines=gen_lines,
        job_options=job_options,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def optimization(geom, charge, mult, method, basis,
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
    """ optimization input string
    """
    job_key = JobKey.OPTIMIZATION
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
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
def _fillvalue_dictionary(job_key, method, basis, geom, mult, charge,
                          orb_restricted, mol_options, memory, comment,
                          machine_options,
                          scf_options, casscf_options, corr_options,
                          gen_lines=None,
                          job_options=(), frozen_coordinates=(), saddle=False):

    reference = _reference(mult, orb_restricted)
    geom_str, zmat_val_str = _geometry_strings(
        geom, frozen_coordinates, job_key)

    # Set options for coupled cluster
    if method in ('ccsd', 'ccsd(t)'):
        corr_options = (('ABCDTYPE=AOBASIS'),)
    if method in ('ccsd', 'ccsd(t)') and reference in ('rhf', 'uhf'):
        corr_options += (('CC_PROG=ECC'),)
    elif method in ('ccsd', 'ccsd(t)') and reference in ('rohf'):
        corr_options += (('CC_PROG=VCC'),)
    elif method in ('ccsdt', 'ccsdt(q)') and reference in ('rhf'):
        corr_options += (('CC_PROG=NCC'),)
    elif method in ('ccsdt', 'ccsdt(q)') and reference in ('uhf', 'rohf'):
        raise NotImplementedError("CFOUR ONLY ALLOWS CLOSED-SHELL")

    # Unused options
    _ = mol_options
    _ = machine_options

    scf_options = _evaluate_options(scf_options)
    casscf_options = _evaluate_options(casscf_options)
    job_options = _evaluate_options(job_options)

    numerical = None

    cfour2_method = elstruct.par.program_method_name(PROG, method)
    cfour2_basis = elstruct.par.program_basis_name(PROG, basis)

    if automol.geom.is_valid(geom):
        coord_sys = 'CARTESIAN'
    elif automol.zmatrix.is_valid(geom):
        coord_sys = 'INTERNAL'

    # Set the gen lines blocks
    if gen_lines is not None:
        gen_lines = '\n'.join(gen_lines[1]) if 1 in gen_lines else ''
    else:
        gen_lines = ''

    fill_dct = {
        TemplateKey.COMMENT: comment,
        TemplateKey.MEMORY: memory,
        TemplateKey.CHARGE: charge,
        TemplateKey.MULT: mult,
        TemplateKey.GEOM: geom_str,
        TemplateKey.COORD_SYS: coord_sys,
        TemplateKey.ZMAT_VAR_VALS: zmat_val_str,
        TemplateKey.BASIS: cfour2_basis.upper(),
        TemplateKey.METHOD: cfour2_method.upper(),
        TemplateKey.REFERENCE: reference.upper(),
        TemplateKey.SCF_OPTIONS: '\n'.join(scf_options),
        TemplateKey.CORR_OPTIONS: '\n'.join(corr_options),
        TemplateKey.JOB_KEY: job_key,
        TemplateKey.JOB_OPTIONS: '\n'.join(job_options),
        TemplateKey.GEN_LINES: '\n'.join(gen_lines),
        TemplateKey.SADDLE: saddle,
        TemplateKey.NUMERICAL: numerical
    }
    return fill_dct


def _geometry_strings(geom, frozen_coordinates, job_key):
    if automol.geom.is_valid(geom):
        geom_str = automol.geom.string(geom)
        zmat_val_str = ''
    elif automol.zmatrix.is_valid(geom):
        zma = geom
        syms = automol.zmatrix.symbols(zma)
        key_mat = automol.zmatrix.key_matrix(zma, shift=1)
        name_mat = _name_mat(zma, frozen_coordinates, job_key)
        val_dct = automol.zmatrix.values(zma, angstrom=True, degree=True)

        geom_str = aw.zmatrix.matrix_block(syms, key_mat, name_mat)
        zmat_val_str = aw.zmatrix.setval_block(val_dct)

        # Substituite multiple whitespaces for single whitespace
        geom_str = '\n'.join([' '.join(string.split())
                              for string in geom_str.splitlines()])
        zmat_val_str = '\n'.join([' '.join(string.split())
                                  for string in zmat_val_str.splitlines()])
        zmat_val_str += '\n'

    else:
        raise ValueError("Invalid geometry value:\n{0}".format(geom))

    return geom_str, zmat_val_str


def _name_mat(zma, frozen_coordinates, job_key):
    """ build name mat
    """
    if job_key == 'optimization':
        name_mat = [
            [name+'*'
             if name is not None and name not in frozen_coordinates else name
             for name in row]
            for row in automol.zmatrix.name_matrix(zma)]
    else:
        name_mat = automol.zmatrix.name_matrix(zma)

    return name_mat


def _reference(mult, orb_restricted):
    if mult != 1:
        reference = (Cfour2Reference.ROHF if orb_restricted else
                     Cfour2Reference.UHF)
    else:
        assert mult == 1 and orb_restricted is True
        reference = Cfour2Reference.RHF

    return reference


def _evaluate_options(options):
    options = list(options)
    for idx, option in enumerate(options):
        if elstruct.option.is_valid(option):
            name = elstruct.option.name(option)
            assert name in par.OPTION_NAMES
            options[idx] = par.CFOUR2_OPTION_EVAL_DCT[name](option)
    return tuple(options)
