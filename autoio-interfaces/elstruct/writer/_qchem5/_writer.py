""" qchem5 writer module """

import os
from ioformat import build_mako_str
import elstruct.par
import elstruct.option
from elstruct.writer import fill


PROG = elstruct.par.Program.QCHEM5

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


# Translate elstruct job key to QChem job key
JOB_DCT = {}
# JOB_DCT = {
#     elstruct.writer.par.Job.ENERGY: 'sp',
#     elstruct.writer.par.Job.GRADIENT: 'force',
#     elstruct.writer.par.Job.HESSIAN: 'freq',
#     elstruct.writer.par.Job.MOLPROP: 'polarizability',
#     elstruct.writer.par.Job.IRC: 'rpath',
#     elstruct.writer.par.Job.OPTIMIZATION: 'opt'
# }


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

    # reset jobtype for saddle point
    job_typ = JOB_DCT[job_key]
    job_typ = 'ts' if job_typ == 'opt' and saddle else job_typ
    # For TS with inital Hessian we might have to run a combined job...

    # set correlated method; check if multiref
    prog_method, _, prog_basis = fill.program_method_names(
        PROG, method, basis, mult, orb_restricted)

    if method == '':
        '   METHOD       {}'.format(prog_method)
    else:
        method = (
            'EXCHANGE  <>\n'
            'CORRELATION <>'
        )
    # maybe just add grid here for now?
    unres = 'false' if orb_restricted else 'true'

    # set the guess options (look at gauss)

    # Set the geometry
    geo_str, zmat_val_str, _ = fill.geometry_strings(geo, frozen_coordinates)

    # Set coords for optimization (job options I guess?)
    # opt_coords = {
    #     'cart': 0,
    #     'red-intl': 1,
    #     'zma-intl': 2
    # }
    # LINE = 'GEOM_OPT_COORDS   ${opt_coords}'

    # Set the memory; convert from GB to MB
    memory_mb = int(memory * 1000.0)

    # Evaluate options
    # scf_options = fill.evaluate_options(scf_options, OPTION_EVAL_DCT)
    # casscf_options = fill.evaluate_options(casscf_options, OPTION_EVAL_DCT)
    # corr_options = fill.evaluate_options(corr_options, OPTION_EVAL_DCT)
    # job_options = fill.evaluate_options(job_options, OPTION_EVAL_DCT)
    # mol_options = fill.evaluate_options(mol_options, OPTION_EVAL_DCT)
    # machine_options = fill.evaluate_options(machine_options, OPTION_EVAL_DCT)
    _ = scf_options
    _ = casscf_options
    _ = corr_options
    _ = job_options
    _ = mol_options
    _ = machine_options
    _ = gen_lines

    # Create a dictionary to fille the template
    fill_dct = {
        fill.TemplateKey.COMMENT: comment,
        fill.TemplateKey.CHARGE: charge,
        fill.TemplateKey.BASIS: prog_basis,
        fill.TemplateKey.GEOM: geo_str,
        fill.TemplateKey.ZMAT_VALS: zmat_val_str,
        fill.TemplateKey.JOB_KEY: job_typ,
        'method': method,
        'unrestricted': unres,
        fill.TemplateKey.MEMORY: memory_mb,
    }

    return build_mako_str(
        template_file_name='all.mako',
        template_src_path=TEMPLATE_DIR,
        template_keys=fill_dct,
        remove_whitespace=False)
