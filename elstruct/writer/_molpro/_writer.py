""" molpro writer module """
import os
import automol
import autowrite as aw
import elstruct.par
import elstruct.option
from elstruct import template
from elstruct.writer._molpro import par

PROG = elstruct.par.Program.MOLPRO

# set the path to the template files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


# mako template keys
class MolproReference():
    """ _ """
    RHF = 'rhf'
    UHF = 'uhf'


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
    MEMORY_MW = 'memory_mw'
    MACHINE_OPTIONS = 'machine_options'
    MOL_OPTIONS = 'mol_options'
    GEOM = 'geom'
    ZMAT_VALS = 'zmat_vals'
    CHARGE = 'charge'
    SPIN = 'spin'
    BASIS = 'basis'
    SCF_METHOD = 'scf_method'
    SCF_OPTIONS = 'scf_options'
    CORR_METHOD = 'corr_method'
    CORR_OPTIONS = 'corr_options'
    JOB_OPTIONS = 'job_options'


def energy(geom, charge, mult, method, basis,
           # molecule options
           mol_options=(),
           # machine options
           memory=1, comment='', machine_options=(),
           # theory options
           orb_restricted=None, scf_options=(), corr_options=()):
    """ energy input string
    """
    job_key = JobKey.ENERGY
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted,
        mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, corr_options=corr_options,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def optimization(geom, charge, mult, method, basis,
                 # molecule options
                 mol_options=(),
                 # machine options
                 memory=1, comment='', machine_options=(),
                 # theory options
                 orb_restricted=None, scf_options=(), corr_options=(),
                 # job options
                 job_options=(), frozen_coordinates=(), saddle=False):
    """ optimization input string
    """
    job_key = JobKey.OPTIMIZATION
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, corr_options=corr_options,
        frozen_coordinates=frozen_coordinates, job_options=job_options,
        saddle=saddle
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


# helper functions
def _fillvalue_dictionary(job_key, method, basis, geom, mult, charge,
                          orb_restricted, mol_options, memory, comment,
                          machine_options, scf_options, corr_options,
                          job_options=(), frozen_coordinates=(), saddle=False):

    singlet = (mult == 1)
    molpro_scf_method = (MolproReference.RHF if orb_restricted else
                         MolproReference.UHF)
    molpro_corr_method = (
        elstruct.par.program_method_name(PROG, method, singlet)
        if elstruct.par.Method.is_correlated(method) else '')

    molpro_basis = elstruct.par.program_basis_name(PROG, basis)
    geom_str, zmat_val_str = _geometry_strings(geom)
    memory_mw = int(memory * (1000.0 / 8.0))  # convert gb to mw
    spin = mult - 1
    scf_options = _evaluate_options(scf_options)
    job_options = _evaluate_options(job_options)

    if saddle:
        job_options += ('root=2',)

    job_directives = [','.join(job_options)]
    if frozen_coordinates:
        job_directives.append('inactive,' + ','.join(frozen_coordinates))

    fill_dct = {
        TemplateKey.JOB_KEY: job_key,
        TemplateKey.COMMENT: comment,
        TemplateKey.MEMORY_MW: memory_mw,
        TemplateKey.MACHINE_OPTIONS: '\n'.join(machine_options),
        TemplateKey.MOL_OPTIONS: '\n'.join(mol_options),
        TemplateKey.GEOM: geom_str,
        TemplateKey.ZMAT_VALS: zmat_val_str,
        TemplateKey.CHARGE: charge,
        TemplateKey.SPIN: spin,
        TemplateKey.BASIS: molpro_basis,
        TemplateKey.SCF_METHOD: molpro_scf_method,
        TemplateKey.SCF_OPTIONS: ','.join(scf_options),
        TemplateKey.CORR_METHOD: molpro_corr_method,
        TemplateKey.CORR_OPTIONS: ','.join(corr_options),
        TemplateKey.JOB_OPTIONS: ';'.join(job_directives),
    }
    return fill_dct


def _geometry_strings(geom):
    if automol.geom.is_valid(geom):
        geom_str = automol.geom.string(geom)
        zmat_val_str = ''
    elif automol.zmatrix.is_valid(geom):
        zma = geom
        syms = automol.zmatrix.symbols(zma)
        key_mat = automol.zmatrix.key_matrix(zma, shift=1)
        name_mat = automol.zmatrix.name_matrix(zma)
        val_dct = automol.zmatrix.values(zma, angstrom=True, degree=True)

        geom_str = aw.zmatrix.matrix_block(syms, key_mat, name_mat, delim=', ')
        zmat_val_str = aw.zmatrix.setval_block(val_dct)
    else:
        raise ValueError("Invalid geometry value:\n{}".format(geom))

    return geom_str, zmat_val_str


def _evaluate_options(opts):
    opts = list(opts)
    for idx, opt in enumerate(opts):
        if elstruct.option.is_valid(opt):
            name = elstruct.option.name(opt)
            assert name in par.OPTION_NAMES
            opts[idx] = par.MOLPRO_OPTION_EVAL_DCT[name](opt)
    return tuple(opts)
