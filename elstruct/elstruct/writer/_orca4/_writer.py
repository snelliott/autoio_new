""" orca4 writer module """

import os
import automol
import autowrite as aw
import elstruct.par
import elstruct.option
from elstruct import template


PROG = elstruct.par.Program.ORCA4

# set the path to the template files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


# helper functions
def write_input(job_key, geo, charge, mult, method, basis, orb_restricted,
                # molecule options
                mol_options=(),
                # machine options
                memory=1, comment='', machine_options=(),
                # theory options
                scf_options=(), casscf_options=(), corr_options=(),
                # generic options
                gen_lines=None,
                # job options
                job_options=(), frozen_coordinates=(), saddle=False):
    """ Write an input file string for an electronic structure calculation
        by processing all of the information and using it to fill in
        a Mako template of the input file.

        :param job_key: job contained in the input file
        :type job_key: str
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
        :param saddle: parameter signifiying a saddle point calculation
        :type saddle: bool
        :param gen_lines: generic lines for the input file
        :type gen_lines: dict[idx:str]
    """

    reference = _reference(method, mult, orb_restricted)
    geo_str, zmat_var_val_str, zmat_const_val_str = _geometry_strings(
        geo, frozen_coordinates)

    _ = machine_options
    _ = casscf_options
    _ = job_options
    _ = irc_direction
    _ = zmat_var_val_str
    _ = zmat_const_val_str

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
    numerical = False
    nprocs = 1
    coord_sys = 'xyz'

    if saddle:
        raise NotImplementedError

    # Set the gen lines blocks
    if gen_lines is not None:
        gen_lines = '\n'.join(gen_lines[1]) if 1 in gen_lines else ''
    else:
        gen_lines = ''

    fill_dct = {
        'nprocs': nprocs,
        'numerical': numerical,
        'coord_sys': coord_sys,
        TemplateKey.MEMORY: memory,
        # TemplateKey.MACHINE_OPTIONS: '\n'.join(machine_options),
        TemplateKey.REFERENCE: reference,
        TemplateKey.METHOD: orca4_method,
        TemplateKey.BASIS: orca4_basis,
        TemplateKey.SCF_OPTIONS: ','.join(scf_options),
        # TemplateKey.SCF_GUESS_OPTIONS: ','.join(scf_guess_options),
        TemplateKey.MOL_OPTIONS: ','.join(mol_options),
        TemplateKey.COMMENT: comment,
        TemplateKey.CHARGE: charge,
        TemplateKey.MULT: mult,
        TemplateKey.GEOM: geo_str,
        # TemplateKey.ZMAT_VAR_VALS: zmat_var_val_str,
        # TemplateKey.ZMAT_CONST_VALS: zmat_const_val_str,
        TemplateKey.JOB_KEY: job_key,
        # TemplateKey.JOB_OPTIONS: ','.join(job_options),
        # TemplateKey.GEN_LINES: '\n'.join(gen_lines),
    }

    return build_mako_str(
        template_file_name='all.mako',
        template_src_path=TEMPLATE_DIR,
        template_keys=fill_dct)


def _geometry_strings(geo, frozen_coordinates):
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
