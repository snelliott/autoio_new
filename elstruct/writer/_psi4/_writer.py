""" psi4 writer module """
import os
import automol
from ... import template
from ... import params as par
from . import template_keys
from . import machine
from . import theory
from . import molecule

PSI4_JOB_FUNCTION_DCT = {
    par.JOB.ENERGY: 'energy',
    par.JOB.GRADIENT: 'gradient',
    par.JOB.HESSIAN: 'hessian',
    par.JOB.OPTIMIZATION: 'optimize',
}


# set the path to the template files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


def method_list():
    """ list of available electronic structure methods
    """
    return theory.METHOD_LST


def basis_list():
    """ list of available electronic structure basis sets
    """
    return theory.BASIS_LST


def _fillvalue_dictionary(method, basis, geom, mult, charge, mol_options,
                          memory, comment, machine_options, scf_options,
                          corr_options):
    """ fill-values for non job-specific options
    """
    fill_dct = {}
    fill_dct.update(machine.fillvalue_dictionary(comment, memory,
                                                 machine_options))
    fill_dct.update(molecule.fillvalue_dictionary(geom, charge, mult,
                                                  mol_options))
    fill_dct.update(theory.fillvalue_dictionary(method, basis, scf_options,
                                                corr_options))
    return fill_dct


def energy(method, basis, geom, mult, charge,
           # molecule options
           mol_options=(),
           # machine options
           memory=1, comment='', machine_options=(),
           # theory options
           scf_options=(), corr_options=()):
    """ energy input string
    """
    assert method in method_list()
    job_key = par.JOB.ENERGY

    # non job-specific arguments
    fill_dct = _fillvalue_dictionary(
        method, basis, geom, mult, charge, mol_options,
        memory, comment, machine_options, scf_options,
        corr_options)

    # job-specific arguments
    fill_dct.update({
        template_keys.JOB_FUNCTION: PSI4_JOB_FUNCTION_DCT[job_key],
        template_keys.JOB_FUNCTION_ARGS: '',
    })

    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def gradient(method, basis, geom, mult, charge,
             # molecule options
             mol_options=(),
             # machine options
             memory=1, comment='', machine_options=(),
             # theory options
             scf_options=(), corr_options=()):
    """ gradient input string
    """
    assert method in method_list()
    job_key = par.JOB.GRADIENT

    # non job-specific arguments
    fill_dct = _fillvalue_dictionary(
        method, basis, geom, mult, charge, mol_options,
        memory, comment, machine_options, scf_options,
        corr_options)

    # job-specific arguments
    fill_dct.update({
        template_keys.JOB_FUNCTION: PSI4_JOB_FUNCTION_DCT[job_key],
        template_keys.JOB_FUNCTION_ARGS: '',
    })

    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def hessian(method, basis, geom, mult, charge,
            # molecule options
            mol_options=(),
            # machine options
            memory=1, comment='', machine_options=(),
            # theory options
            scf_options=(), corr_options=()):
    """ hessian input string
    """
    assert method in method_list()
    job_key = par.JOB.HESSIAN

    # non job-specific arguments
    fill_dct = _fillvalue_dictionary(
        method, basis, geom, mult, charge, mol_options,
        memory, comment, machine_options, scf_options,
        corr_options)

    # job-specific arguments
    scf_method, corr_method = par.METHOD.split_name(method)
    job_function_args = ''
    # # for these cases we have to call hessian(..., dertype=1) for some reason
    if scf_method == par.METHOD.UHF:
        job_function_args = 'dertype=1'
    elif scf_method == par.METHOD.ROHF and corr_method is None:
        job_function_args = 'dertype=1'

    fill_dct.update({
        template_keys.JOB_FUNCTION: PSI4_JOB_FUNCTION_DCT[job_key],
        template_keys.JOB_FUNCTION_ARGS: job_function_args,
    })

    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def optimization(method, basis, geom, mult, charge,
                 # molecule options
                 mol_options=(),
                 # machine options
                 memory=1, comment='', machine_options=(),
                 # theory options
                 scf_options=(), corr_options=(),
                 # molecule/optimization options
                 frozen_coordinates=None, opt_options=()):
    """ optimization input string
    """
    assert method in method_list()
    job_key = par.JOB.OPTIMIZATION

    # non job-specific arguments
    fill_dct = _fillvalue_dictionary(
        method, basis, geom, mult, charge, mol_options,
        memory, comment, machine_options, scf_options,
        corr_options)

    # job-specific arguments

    # # frozen coordinates
    freeze_option_fmt = """
set optking {{
  frozen_distance = ("
    {:s}
  ")
  frozen_bend = ("
    {:s}
  ")
  frozen_dihedral = ("
    {:s}
  ")
}}
"""

    if frozen_coordinates is not None:
        assert automol.zmatrix.is_valid(geom)
        coo_dct = automol.zmatrix.coordinates(geom, one_indexed=True)
        assert all(coo_name in coo_dct for coo_name in frozen_coordinates)

        def _coordinate_string(coo_names):
            frz_coo_names = [coo_name for coo_name in frozen_coordinates
                             if coo_name in coo_names]
            frz_coo_str = '\n    '.join(' '.join(map(str, coo_keys))
                                        for frz_coo_name in frz_coo_names
                                        for coo_keys in coo_dct[frz_coo_name])
            return frz_coo_str

        dis_str = _coordinate_string(automol.zmatrix.distance_names(geom))
        ang_str = _coordinate_string(automol.zmatrix.angle_names(geom))
        dih_str = _coordinate_string(automol.zmatrix.dihedral_names(geom))
        freeze_option_str = freeze_option_fmt.format(dis_str, ang_str, dih_str)
        opt_options += (freeze_option_str,)

    opt_options_str = '\n'.join(opt_options)
    fill_dct.update({
        template_keys.JOB_FUNCTION: PSI4_JOB_FUNCTION_DCT[job_key],
        template_keys.JOB_FUNCTION_ARGS: '',
        template_keys.OPT_OPTIONS: opt_options_str,
    })

    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str
