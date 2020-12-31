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


def _evaluate_options(opts):
    opts = list(opts)
    for idx, opt in enumerate(opts):
        if elstruct.option.is_valid(opt):
            name = elstruct.option.name(opt)
            assert name in prog_par.OPTION_NAMES
            opts[idx] = prog_par.MRCC2018_OPTION_EVAL_DCT[name](opt)
    return tuple(opts)
