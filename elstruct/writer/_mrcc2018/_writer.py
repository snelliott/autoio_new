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
        charge=charge, orb_restricted=orb_restricted,
        mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, casscf_options=casscf_options, corr_options=corr_options,
        gen_lines=gen_lines,
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
        scf_options=scf_options, casscf_options=casscf_options, corr_options=corr_options,
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
        scf_options=scf_options, casscf_options=casscf_options, corr_options=corr_options,
        gen_lines=gen_lines,
        frozen_coordinates=frozen_coordinates, job_options=job_options,
        saddle=saddle
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


# helper functions
def _fillvalue_dictionary(job_key, method, basis, geom, mult, charge,
                          orb_restricted, mol_options, memory, comment,
                          machine_options, scf_options, casscf_options, corr_options,
                          gen_lines=None,
                          job_options=(), frozen_coordinates=(), saddle=False):

    # Set the spin
    singlet = (mult == 1)
    spin = mult - 1
   
    # Set the theoretical method
    mrcc_scf_method = (MRCC2018Reference.RHF if orb_restricted else
                         MRCC2018Reference.UHF)
    mrcc_corr_method = (
        elstruct.par.program_method_name(PROG, method, singlet)
        if elstruct.par.Method.is_correlated(method) else '')
    mrcc_basis = elstruct.par.program_basis_name(PROG, basis)
    
    # Build the geometry
    geom_str, zmat_val_str = _geometry_strings(geom)
    spin = mult - 1
    
    # Check options
    scf_options = _evaluate_options(scf_options)
    casscf_options = _evaluate_options(casscf_options)
    job_options = _evaluate_options(job_options)

    # Set the coordinate system
    if automol.geom.is_valid(geom):
        coord_sys = 'xyz'
    elif automol.zmatrix.is_valid(geom):
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
        TemplateKey.GEOM: geom_str,
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

        geom_str = aw.zmatrix.matrix_block(syms, key_mat, name_mat)
        zmat_val_str = aw.zmatrix.setval_block(val_dct)
    else:
        raise ValueError("Invalid geometry value:\n{0}".format(geom))

    return geom_str, zmat_val_str


def _evaluate_options(opts):
    opts = list(opts)
    for idx, opt in enumerate(opts):
        if elstruct.option.is_valid(opt):
            name = elstruct.option.name(opt)
            assert name in par.OPTION_NAMES
            opts[idx] = par.MRCC2018_OPTION_EVAL_DCT[name](opt)
    return tuple(opts)
