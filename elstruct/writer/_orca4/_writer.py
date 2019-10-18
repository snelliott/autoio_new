""" orca4 writer module """
import os
import automol
import autowrite as aw
import elstruct.par
import elstruct.option
from elstruct import template
from elstruct.writer._orca4 import par
from elstruct import pclass

PROG = elstruct.par.Program.ORCA4

# set the path to the template files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


# mako template keys
class Orca4Reference():
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
    COMMENT = 'comment'
    CHARGE = 'charge'
    MULT = 'mult'
    GEOM = 'geom'
    ZMAT_VAR_VALS = 'zmat_var_vals'
    ZMAT_CONST_VALS = 'zmat_const_vals'
    # job
    JOB_KEY = 'job_key'
    JOB_OPTIONS = 'job_options'
    GEN_LINES = 'gen_lines'
    IRC_DIRECTION = 'irc_direction'


def energy(geom, charge, mult, method, basis,
           # molecule options
           mol_options=(),
           # machine options
           memory=1, comment='', machine_options=(),
           # theory options
           orb_restricted=None,
           scf_options=(), casscf_options=(), corr_options=(),
           # generic options
           gen_lines=()):
    """ energy input string
    """
    job_key = JobKey.ENERGY
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options,
        casscf_options=casscf_options,
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
             gen_lines=(),
             # job options
             job_options=()):
    """ gradient input string
    """
    job_key = JobKey.GRADIENT
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options,
        casscf_options=casscf_options,
        corr_options=corr_options,
        job_options=job_options, gen_lines=gen_lines,
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
            gen_lines=(),
            # job options
            job_options=()):
    """ hessian input string
    """
    job_key = JobKey.HESSIAN
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options,
        casscf_options=casscf_options,
        corr_options=corr_options,
        job_options=job_options, gen_lines=gen_lines,
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
                 gen_lines=(),
                 # job options
                 job_options=(), frozen_coordinates=(), saddle=False):
    """ optimization input string
    """
    job_key = JobKey.OPTIMIZATION
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options,
        casscf_options=casscf_options,
        corr_options=corr_options,
        job_options=job_options, frozen_coordinates=frozen_coordinates,
        saddle=saddle, gen_lines=gen_lines,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


# helper functions
def _fillvalue_dictionary(job_key, method, basis, geom, mult, charge,
                          orb_restricted, mol_options, memory, comment,
                          machine_options,
                          scf_options, casscf_options, corr_options,
                          job_options=(), frozen_coordinates=(),
                          saddle=False, irc_direction=None,
                          gen_lines=()):

    reference = _reference(method, mult, orb_restricted)
    geom_str, zmat_var_val_str, zmat_const_val_str = _geometry_strings(
        geom, frozen_coordinates)

    memory = memory * 1000.0

    if elstruct.par.Method.is_correlated(method):
        assert not corr_options

    orca4_method = elstruct.par.program_method_name(PROG, method)
    orca4_basis = elstruct.par.program_basis_name(PROG, basis)

    # in the case of Hartree-Fock, swap the method for the reference name
    if method == elstruct.par.Method.HF[0]:
        orca4_method = reference
        reference = ''

    # scf_guess_options, scf_options = _intercept_scf_guess_option(scf_options)
    # scf_guess_options = _evaluate_options(scf_guess_options)
    # scf_options = _evaluate_options(scf_options)
    # casscf_options = _evaluate_options(casscf_options)
    # job_options = _evaluate_options(job_options)

    if saddle:
        raise NotImplementedError

    fill_dct = {
        TemplateKey.MEMORY: memory,
        TemplateKey.MACHINE_OPTIONS: '\n'.join(machine_options),
        TemplateKey.REFERENCE: reference,
        TemplateKey.METHOD: orca4_method,
        TemplateKey.BASIS: orca4_basis,
        TemplateKey.SCF_OPTIONS: ','.join(scf_options),
        # TemplateKey.SCF_GUESS_OPTIONS: ','.join(scf_guess_options),
        TemplateKey.MOL_OPTIONS: ','.join(mol_options),
        TemplateKey.COMMENT: comment,
        TemplateKey.CHARGE: charge,
        TemplateKey.MULT: mult,
        TemplateKey.GEOM: geom_str,
        TemplateKey.ZMAT_VAR_VALS: zmat_var_val_str,
        TemplateKey.ZMAT_CONST_VALS: zmat_const_val_str,
        TemplateKey.JOB_KEY: job_key,
        TemplateKey.JOB_OPTIONS: ','.join(job_options),
        TemplateKey.GEN_LINES: '\n'.join(gen_lines),
    }
    return fill_dct


def _geometry_strings(geom, frozen_coordinates):
    if automol.geom.is_valid(geom):
        geom_str = automol.geom.string(geom)
        zmat_vval_str = ''
        zmat_cval_str = ''
    elif automol.zmatrix.is_valid(geom):
        zma = geom
        syms = automol.zmatrix.symbols(zma)
        key_mat = automol.zmatrix.key_matrix(zma, shift=1)
        name_mat = automol.zmatrix.name_matrix(zma)
        val_dct = automol.zmatrix.values(zma, angstrom=True, degree=True)
        geom_str = aw.zmatrix.matrix_block(syms, key_mat, name_mat)

        vval_dct = {key: val for key, val in val_dct.items()
                    if key not in frozen_coordinates}
        cval_dct = {key: val for key, val in val_dct.items()
                    if key in frozen_coordinates}

        zmat_vval_str = aw.zmatrix.setval_block(
            vval_dct, setval_sign=' ').strip()
        zmat_cval_str = aw.zmatrix.setval_block(
            cval_dct, setval_sign=' ').strip()
    else:
        raise ValueError("Invalid geometry value:\n{}".format(geom))

    return geom_str, zmat_vval_str, zmat_cval_str


def _reference(method, mult, orb_restricted):
    if elstruct.par.Method.is_dft(method):
        reference = ''
    elif mult != 1:
        reference = (Orca4Reference.ROHF
                     if orb_restricted else Orca4Reference.UHF)
    else:
        assert mult == 1 and orb_restricted is True
        reference = Orca4Reference.RHF
    return reference


# def _evaluate_options(opts):
#     opts = list(opts)
#     for idx, opt in enumerate(opts):
#         if elstruct.option.is_valid(opt):
#             name = elstruct.option.name(opt)
#             assert name in par.OPTION_NAMES
#             opts[idx] = par.Orca4_OPTION_EVAL_DCT[name](opt)
#     return tuple(opts)
