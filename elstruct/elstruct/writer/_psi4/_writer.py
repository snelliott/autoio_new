""" psi4 writer module """

import os
import automol
import autowrite as aw
import elstruct.par
import elstruct.option
from elstruct import template
from elstruct.writer._psi4 import par


PROG = elstruct.par.Program.PSI4

# set the path to the template files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


# helper functions
def write_input(job_key, method, basis, geo, mult, charge,
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

    frozen_dis_strs, frozen_ang_strs, frozen_dih_strs = (
        _frozen_coordinate_strings(geo, frozen_coordinates))

    reference = _reference(method, mult, orb_restricted)
    geo_str, zmat_val_str = _geometry_strings(geo)

    if not elstruct.par.Method.is_correlated(method):
        assert not corr_options

    scf_options = _evaluate_options(scf_options)
    casscf_options = _evaluate_options(casscf_options)
    job_options = _evaluate_options(job_options)

    if saddle:
        job_options += ('set full_hess_every 0', 'set opt_type ts',)

    psi4_method = elstruct.par.program_method_name(PROG, method)
    psi4_basis = elstruct.par.program_basis_name(PROG, basis)

    # Set the gen lines blocks
    if gen_lines is not None:
        gen_lines = '\n'.join(gen_lines[1]) if 1 in gen_lines else ''
    else:
        gen_lines = ''

    fill_dct = {
        TemplateKey.COMMENT: comment,
        TemplateKey.MEMORY: memory,
        TemplateKey.MACHINE_OPTIONS: '\n'.join(machine_options),
        TemplateKey.MOL_OPTIONS: '\n'.join(mol_options),
        TemplateKey.CHARGE: charge,
        TemplateKey.MULT: mult,
        TemplateKey.GEOM: geo_str,
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
        TemplateKey.GEN_LINES: '\n'.join(gen_lines),
    }

    return build_mako_str(
        template_file_name='all.mako',
        template_src_path=TEMPLATE_DIR,
        template_keys=fill_dct)


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


def _frozen_coordinate_strings(geo, frozen_coordinates):
    if not frozen_coordinates:
        dis_strs = ang_strs = dih_strs = ()
    else:
        coo_dct = automol.zmatrix.coordinates(geo, shift=1)
        assert all(coo_name in coo_dct for coo_name in frozen_coordinates)

        def _coordinate_strings(coo_names):
            frz_coo_names = [coo_name for coo_name in frozen_coordinates
                             if coo_name in coo_names]
            frz_coo_strs = tuple(' '.join(map(str, coo_keys))
                                 for frz_coo_name in frz_coo_names
                                 for coo_keys in coo_dct[frz_coo_name])
            return frz_coo_strs

        dis_strs = _coordinate_strings(
            automol.zmatrix.distance_names(geo))
        ang_strs = _coordinate_strings(
            automol.zmatrix.central_angle_names(geo))
        dih_strs = _coordinate_strings(
            automol.zmatrix.dihedral_angle_names(geo))
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
