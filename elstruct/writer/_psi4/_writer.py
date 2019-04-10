""" psi4 writer module """
import os
import automol
import elstruct.par
import elstruct.option
from elstruct import template
from elstruct.writer._psi4 import par

PROG = elstruct.par.Program.PSI4

# set the path to the template files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


# mako template keys
class Psi4Reference():
    """ _ """
    RHF = 'rhf'
    UHF = 'uhf'
    ROHF = 'rohf'
    RKS = 'rks'
    UKS = 'uks'


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
    ZMAT_VALS = 'zmat_vals'
    BASIS = 'basis'
    REFERENCE = 'reference'
    SCF_OPTIONS = 'scf_options'
    CORR_OPTIONS = 'corr_options'
    METHOD = 'method'
    JOB_OPTIONS = 'job_options'
    FROZEN_DIS_STRS = 'frozen_dis_strs'
    FROZEN_ANG_STRS = 'frozen_ang_strs'
    FROZEN_DIH_STRS = 'frozen_dih_strs'


def energy(method, basis, geom, mult, charge,
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
    job_key = JobKey.GRADIENT
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
    job_key = JobKey.HESSIAN
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
    job_key = JobKey.OPTIMIZATION
    fill_dct = _fillvalue_dictionary(
        job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
        charge=charge, orb_restricted=orb_restricted, mol_options=mol_options,
        memory=memory, comment=comment, machine_options=machine_options,
        scf_options=scf_options, corr_options=corr_options,
        frozen_coordinates=frozen_coordinates, job_options=job_options,
    )
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


# helper functions
def _fillvalue_dictionary(job_key, method, basis, geom, mult, charge,
                          orb_restricted, mol_options, memory, comment,
                          machine_options, scf_options, corr_options,
                          job_options=(), frozen_coordinates=()):

    frozen_dis_strs, frozen_ang_strs, frozen_dih_strs = (
        _frozen_coordinate_strings(geom, frozen_coordinates))

    reference = _reference(method, mult, orb_restricted)
    geom_str, zmat_val_str = _geometry_strings(geom)

    if not elstruct.par.Method.is_correlated(method):
        assert not corr_options

    scf_options = _evaluate_options(scf_options)
    job_options = _evaluate_options(job_options)

    psi4_method = elstruct.par.program_method_name(PROG, method)
    psi4_basis = elstruct.par.program_basis_name(PROG, basis)

    fill_dct = {
        TemplateKey.COMMENT: comment,
        TemplateKey.MEMORY: memory,
        TemplateKey.MACHINE_OPTIONS: '\n'.join(machine_options),
        TemplateKey.MOL_OPTIONS: '\n'.join(mol_options),
        TemplateKey.CHARGE: charge,
        TemplateKey.MULT: mult,
        TemplateKey.GEOM: geom_str,
        TemplateKey.ZMAT_VALS: zmat_val_str,
        TemplateKey.BASIS: psi4_basis,
        TemplateKey.METHOD: psi4_method,
        TemplateKey.REFERENCE: reference,
        TemplateKey.SCF_OPTIONS: '\n'.join(scf_options),
        TemplateKey.CORR_OPTIONS: '\n'.join(corr_options),
        TemplateKey.JOB_KEY: job_key,
        TemplateKey.JOB_OPTIONS: '\n'.join(job_options),
        TemplateKey.FROZEN_DIS_STRS: frozen_dis_strs,
        TemplateKey.FROZEN_ANG_STRS: frozen_ang_strs,
        TemplateKey.FROZEN_DIH_STRS: frozen_dih_strs,
    }
    return fill_dct


def _geometry_strings(geom):
    if automol.geom.is_valid(geom):
        geom_str = automol.geom.string(geom)
        zmat_val_str = ''
    elif automol.zmatrix.is_valid(geom):
        geom_str = automol.zmatrix.matrix_block_string(geom)
        zmat_val_str = automol.zmatrix.setval_block_string(geom)
    else:
        raise ValueError("Invalid geometry value:\n{}".format(geom))

    return geom_str, zmat_val_str


def _frozen_coordinate_strings(geom, frozen_coordinates):
    if not frozen_coordinates:
        dis_strs = ang_strs = dih_strs = ()
    else:
        coo_dct = automol.zmatrix.coordinates(geom, one_indexed=True)
        assert all(coo_name in coo_dct for coo_name in frozen_coordinates)

        def _coordinate_strings(coo_names):
            frz_coo_names = [coo_name for coo_name in frozen_coordinates
                             if coo_name in coo_names]
            frz_coo_strs = tuple(' '.join(map(str, coo_keys))
                                 for frz_coo_name in frz_coo_names
                                 for coo_keys in coo_dct[frz_coo_name])
            return frz_coo_strs

        dis_strs = _coordinate_strings(
            automol.zmatrix.distance_names(geom))
        ang_strs = _coordinate_strings(
            automol.zmatrix.central_angle_names(geom))
        dih_strs = _coordinate_strings(
            automol.zmatrix.dihedral_angle_names(geom))
    return dis_strs, ang_strs, dih_strs


def _reference(method, mult, orb_restricted):
    if elstruct.par.Method.is_dft(method):
        reference = (Psi4Reference.RKS if orb_restricted else
                     Psi4Reference.UKS)
    elif mult != 1:
        reference = (Psi4Reference.ROHF if orb_restricted else
                     Psi4Reference.UHF)
    else:
        assert mult == 1 and orb_restricted is True
        reference = Psi4Reference.RHF

    return reference


def _evaluate_options(options):
    options = list(options)
    for idx, option in enumerate(options):
        if elstruct.option.is_valid(option):
            name = elstruct.option.name(option)
            assert name in par.OPTION_NAMES
            options[idx] = par.PSI4_OPTION_EVAL_DCT[name](option)
    return tuple(options)
