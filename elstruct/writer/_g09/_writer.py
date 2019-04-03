""" g09 writer module """
import os
import automol
import autowrite as aw
import elstruct.par
import elstruct.option
from elstruct import template
from elstruct import pclass
from elstruct.writer._g09 import par

# set the path to the template files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


def method_list():
    """ list of available electronic structure methods
    """
    return par.METHODS


def basis_list():
    """ list of available electronic structure basis sets
    """
    return par.BASES


def energy(method, basis, geom, mult, charge,
           # molecule options
           mol_options=(),
           # machine options
           memory=1, comment='', machine_options=(),
           # theory options
           orb_restricted=None, scf_options=(), corr_options=()):
    """ energy input string
    """
    job_key = par.JobKey.ENERGY
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, corr_options=corr_options,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def gradient(method, basis, geom, mult, charge,
             # molecule options
             mol_options=(),
             # machine options
             memory=1, comment='', machine_options=(),
             # theory options
             orb_restricted=None, scf_options=(), corr_options=(),
             # job options
             job_options=()):
    """ gradient input string
    """
    job_key = par.JobKey.GRADIENT
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, corr_options=corr_options,
        job_options=job_options,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def hessian(method, basis, geom, mult, charge,
            # molecule options
            mol_options=(),
            # machine options
            memory=1, comment='', machine_options=(),
            # theory options
            orb_restricted=None, scf_options=(), corr_options=(),
            # job options
            job_options=()):
    """ hessian input string
    """
    job_key = par.JobKey.HESSIAN
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, corr_options=corr_options,
        job_options=job_options,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def optimization(method, basis, geom, mult, charge,
                 # molecule options
                 mol_options=(),
                 # machine options
                 memory=1, comment='', machine_options=(),
                 # theory options
                 orb_restricted=None, scf_options=(), corr_options=(),
                 # job options
                 job_options=(), frozen_coordinates=()):
    """ optimization input string
    """
    job_key = par.JobKey.OPTIMIZATION
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, corr_options=corr_options,
        job_options=job_options, frozen_coordinates=frozen_coordinates,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


# helper functions
def _fillvalue_dictionary(job_key, method, basis, geom, mult, charge,
                          orb_restricted, mol_options, memory, comment,
                          machine_options, scf_options, corr_options,
                          job_options=(), frozen_coordinates=()):
    assert method in par.METHODS
    assert basis in par.BASES

    reference = _reference(method, mult, orb_restricted)
    geom_str, zmat_var_val_str, zmat_const_val_str = _geometry_strings(
        geom, frozen_coordinates)

    if method in pclass.values(elstruct.par.Method.Corr):
        assert not corr_options

    if (reference == par.G09Reference.ROHF and
            job_key in (par.JobKey.GRADIENT, par.JobKey.HESSIAN)):
        job_options = list(job_options)
        job_options.insert(0, 'EnOnly')

    g09_method = par.G09_METHOD_DCT[method]
    g09_basis = par.G09_BASIS_DCT[basis]

    # in the case of Hartree-Fock, swap the method for the reference name
    if method == elstruct.par.Method.HF:
        g09_method = reference
        reference = ''

    scf_guess_options, scf_options = _intercept_scf_guess_option(scf_options)
    scf_guess_options = _evaluate_options(scf_guess_options)
    scf_options = _evaluate_options(scf_options)
    job_options = _evaluate_options(job_options)

    fill_dct = {
        par.TemplateKey.MEMORY: memory,
        par.TemplateKey.MACHINE_OPTIONS: ','.join(machine_options),
        par.TemplateKey.REFERENCE: reference,
        par.TemplateKey.METHOD: g09_method,
        par.TemplateKey.BASIS: g09_basis,
        par.TemplateKey.SCF_OPTIONS: ','.join(scf_options),
        par.TemplateKey.SCF_GUESS_OPTIONS: ','.join(scf_guess_options),
        par.TemplateKey.MOL_OPTIONS: ','.join(mol_options),
        par.TemplateKey.COMMENT: comment,
        par.TemplateKey.CHARGE: charge,
        par.TemplateKey.MULT: mult,
        par.TemplateKey.GEOM: geom_str,
        par.TemplateKey.ZMAT_VAR_VALS: zmat_var_val_str,
        par.TemplateKey.ZMAT_CONST_VALS: zmat_const_val_str,
        par.TemplateKey.JOB_KEY: job_key,
        par.TemplateKey.JOB_OPTIONS: ','.join(job_options),
    }
    return fill_dct


def _geometry_strings(geom, frozen_coordinates):
    if automol.geom.is_valid(geom):
        geom_str = automol.geom.string(geom)
        zmat_var_val_str = ''
        zmat_const_val_str = ''
    elif automol.zmatrix.is_valid(geom):
        geom_str = automol.zmatrix.matrix_block_string(geom)
        val_dct = automol.zmatrix.values(geom, angstrom=True, degree=True)
        var_val_dct = {key: val for key, val in val_dct.items()
                       if key not in frozen_coordinates}
        const_val_dct = {key: val for key, val in val_dct.items()
                         if key in frozen_coordinates}
        zmat_var_val_str = aw.zmatrix.setval_block(
            var_val_dct, setval_sign=' ').strip()
        zmat_const_val_str = aw.zmatrix.setval_block(
            const_val_dct, setval_sign=' ').strip()
    else:
        raise ValueError("Invalid geometry value:\n{}".format(geom))

    return geom_str, zmat_var_val_str, zmat_const_val_str


def _reference(method, mult, orb_restricted):
    is_dft = method in pclass.values(elstruct.par.Method.Dft)

    # for now, orbital restriction is really only for open-shell hartree-fock
    if orb_restricted is False and mult == 1:
        raise NotImplementedError

    if orb_restricted is True and mult != 1 and is_dft:
        raise NotImplementedError

    if is_dft:
        reference = ''
    else:
        reference = (par.G09Reference.RHF if mult == 1 else
                     (par.G09Reference.ROHF if orb_restricted else
                      par.G09Reference.UHF))
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
            opts[idx] = par.G09_OPTION_EVAL_DCT[name](opt)
    return tuple(opts)
