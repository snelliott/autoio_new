""" psi4 writer module """
import os
from ... import template
from ... import params as par
from . import machine
from . import theory
from . import molecule
from . import job

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


def energy_input_string(method, basis, geom, charge, mult,
                        memory=1, comment='', machine_options='',
                        scf_options='', corr_options='',
                        zmat_var_dct=None):
    """ energy input string
    """
    assert method in method_list()
    job_key = par.JOB.ENERGY

    fill_dct = {}
    fill_dct.update(machine.fillvalue_dictionary(comment, memory,
                                                 machine_options))
    fill_dct.update(molecule.fillvalue_dictionary(geom, charge, mult,
                                                  zmat_var_dct))
    fill_dct.update(theory.fillvalue_dictionary(method, basis, scf_options,
                                                corr_options))
    fill_dct.update(job.fillvalue_dictionary(job_key))
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str


def optimization_input_string(method, basis, geom, charge, mult,
                              memory=1, comment='', machine_options='',
                              scf_options='', corr_options='', opt_options='',
                              zmat_var_dct=None):
    """ optimization input string
    """
    assert method in method_list()
    job_key = par.JOB.OPTIMIZATION

    fill_dct = {}
    fill_dct.update(machine.fillvalue_dictionary(comment, memory,
                                                 machine_options))
    fill_dct.update(molecule.fillvalue_dictionary(geom, charge, mult,
                                                  zmat_var_dct))
    fill_dct.update(theory.fillvalue_dictionary(method, basis, scf_options,
                                                corr_options))
    fill_dct.update(job.fillvalue_dictionary(job_key, opt_options))
    inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
    return inp_str
