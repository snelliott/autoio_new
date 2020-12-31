""" cfour2 writer module """

import os
import automol
import autowrite as aw
import elstruct.par
import elstruct.option
from elstruct import template
from elstruct.writer._cfour2 import par as prog_par


PROG = elstruct.par.Program.CFOUR2

# Set the path to the template files
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

    reference = _reference(mult, orb_restricted)
    geo_str, zmat_val_str = _geometry_strings(
        geo, frozen_coordinates, job_key)

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

    if automol.geom.is_valid(geo):
        coord_sys = 'CARTESIAN'
    elif automol.zmatrix.is_valid(geo):
        coord_sys = 'INTERNAL'

    # Set the gen lines blocks
    if gen_lines is not None:
        gen_lines = '\n'.join(gen_lines[1]) if 1 in gen_lines else ''
    else:
        gen_lines = ''

    # Write the input file string
    fill_dct = {
        TemplateKey.COMMENT: comment,
        TemplateKey.MEMORY: memory,
        TemplateKey.CHARGE: charge,
        TemplateKey.MULT: mult,
        TemplateKey.GEOM: geo_str,
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

    return build_mako_str(
        template_file_name='all.mako',
        template_src_path=TEMPLATE_DIR,
        template_keys=fill_dct)


def _geometry_strings(geo, frozen_coordinates, job_key):
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
        name_mat = _name_mat(zma, frozen_coordinates, job_key)
        val_dct = automol.zmatrix.values(zma, angstrom=True, degree=True)

        geo_str = aw.zmatrix.matrix_block(symbs, key_mat, name_mat)
        zmat_val_str = aw.zmatrix.setval_block(val_dct)

        # Substituite multiple whitespaces for single whitespace
        geo_str = '\n'.join([' '.join(string.split())
                             for string in geo_str.splitlines()])
        zmat_val_str = '\n'.join([' '.join(string.split())
                                  for string in zmat_val_str.splitlines()])
        zmat_val_str += '\n'

    else:
        raise ValueError("Invalid geometry value:\n{0}".format(geo))

    return geo_str, zmat_val_str


def _name_mat(zma, frozen_coordinates, job_key):
    """ Build the name matrix for a Z-Matrix data structure:

        :param zma: cartesian or z-matrix geometry
        :type zma: tuple
        :param frozen_coordinates: only with z-matrix geometries; list of
            coordinate names to freeze
        :type fozen_coordinates: tuple[str]
        :param job_key: job contained in the inpit file
        :type job_key: str
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
        reference = (prog_par.ROHF if orb_restricted else
                     prog_par.UHF)
    else:
        assert mult == 1 and orb_restricted is True
        reference = prog_par.RHF

    return reference


def _evaluate_options(options):
    options = list(options)
    for idx, option in enumerate(options):
        if elstruct.option.is_valid(option):
            name = elstruct.option.name(option)
            assert name in prog_par.OPTION_NAMES
            options[idx] = prog_par.CFOUR2_OPTION_EVAL_DCT[name](option)
    return tuple(options)
