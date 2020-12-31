""" molpro2015 writer module """
import os
import automol
import autowrite as aw
import elstruct.par
import elstruct.option
from elstruct import template
from elstruct.writer._molpro2015 import par as prog_par

PROG = elstruct.par.Program.MOLPRO2015

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

    # Set the spin
    singlet = (mult == 1)
    spin = mult - 1

    # Set the reference
    molpro_scf_method = (prog_par.Reference.RHF if orb_restricted else
                         prog_par.Reference.UHF)

    # set correlated method; check if multiref
    molpro_corr_method, ismultiref = _set_method(method, singlet)

    # Set the basis
    molpro_basis = elstruct.par.program_basis_name(PROG, basis)

    # Set the geometry
    geo_str, zmat_val_str = _geometry_strings(geo)

    # Set the memory; convert from GB to MW
    memory_mw = int(memory * (1024.0 / 8.0))

    # Set the job directives and options
    scf_options = _evaluate_options(scf_options)
    casscf_options = _evaluate_options(casscf_options)
    corr_options = _evaluate_options(corr_options)
    job_options = _evaluate_options(job_options)

    # Make no scf method if calling a multiref method
    if ismultiref:
        molpro_scf_method = ''
        scf_options = []

    if saddle:
        job_options += ('root=2',)

    job_directives = [','.join(job_options)]
    if frozen_coordinates:
        job_directives.append('inactive,' + ','.join(frozen_coordinates))

    if job_key == 'hessian':
        job_directives.append('print,hessian,low=5')

    # Set the gen lines blocks
    if gen_lines is not None:
        gen_lines_1 = '\n'.join(gen_lines[1]) if 1 in gen_lines else ''
        gen_lines_2 = '\n'.join(gen_lines[2]) if 2 in gen_lines else ''
        gen_lines_3 = '\n'.join(gen_lines[3]) if 3 in gen_lines else ''
    else:
        gen_lines_1 = ''
        gen_lines_2 = ''
        gen_lines_3 = 'molpro_energy=energy\nshow[1,e25.15],molpro_energy'

    # Create a dictionary to fille the template
    fill_dct = {
        TemplateKey.JOB_KEY: job_key,
        TemplateKey.COMMENT: comment,
        TemplateKey.MEMORY_MW: memory_mw,
        TemplateKey.MACHINE_OPTIONS: '\n'.join(machine_options),
        TemplateKey.MOL_OPTIONS: '\n'.join(mol_options),
        TemplateKey.GEOM: geo_str,
        TemplateKey.ZMAT_VALS: zmat_val_str,
        TemplateKey.CHARGE: charge,
        TemplateKey.SPIN: spin,
        TemplateKey.BASIS: molpro_basis,
        TemplateKey.SCF_METHOD: molpro_scf_method,
        TemplateKey.SCF_OPTIONS: ','.join(scf_options),
        TemplateKey.ISMULTIREF: ismultiref,
        TemplateKey.CASSCF_OPTIONS: '\n'.join(casscf_options),
        TemplateKey.CORR_METHOD: molpro_corr_method,
        TemplateKey.CORR_OPTIONS: ','.join(corr_options),
        TemplateKey.JOB_OPTIONS: ';'.join(job_directives),
        TemplateKey.GEN_LINES_1: gen_lines_1,
        TemplateKey.GEN_LINES_2: gen_lines_2,
        TemplateKey.GEN_LINES_3: gen_lines_3
    }

    return build_mako_str(
        template_file_name='all.mako',
        template_src_path=TEMPLATE_DIR,
        template_keys=fill_dct)


def _set_method(method, singlet):
    # Check if MultiReference Method; then check if casscf
    if elstruct.par.Method.is_multiref(method):
        ismultiref = True
        if elstruct.par.Method.is_casscf(method):
            corr_method = ''
        else:
            corr_method = elstruct.par.program_method_name(
                PROG, method, singlet)
    # Set methods if single reference
    else:
        ismultiref = False
        if elstruct.par.Method.is_correlated(method):
            corr_method = elstruct.par.program_method_name(
                PROG, method, singlet)
        else:
            corr_method = ''

    return corr_method, ismultiref


def _geometry_strings(geo):
    """ Build the string for the input geometry

        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
        :param frozen_coordinates: only with z-matrix geometries; list of
            coordinate names to freeze
        :type fozen_coordinates: tuple[str]
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

        geo_str = aw.zmatrix.matrix_block(symbs, key_mat, name_mat, delim=', ')
        zmat_val_str = aw.zmatrix.setval_block(val_dct)
    elif geo in ('GEOMETRY', 'GEOMETRY_HERE'):
        geo_str = geo
        zmat_val_str = ''
    else:
        raise ValueError("Invalid geometry value:\n{}".format(geo))

    return geo_str, zmat_val_str


def _evaluate_options(opts):
    opts = list(opts)
    for idx, opt in enumerate(opts):
        if elstruct.option.is_valid(opt):
            name = elstruct.option.name(opt)
            assert name in prog_par.OPTION_NAMES
            opts[idx] = prog_par.MOLPRO2015_OPTION_EVAL_DCT[name](opt)
    return tuple(opts)
