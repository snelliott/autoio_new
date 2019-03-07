""" job: energy, optimization, frequency, etc
"""
from ... import params as par
from . import template_keys

JOB_FUNCTION_DCT = {
    par.JOB.ENERGY: 'energy',
    par.JOB.GRADIENT: 'gradient',
    par.JOB.HESSIAN: 'hessian',
    par.JOB.OPTIMIZATION: 'optimize',
}

JOB_OPTIONS_KEY_DCT = {
    par.JOB.OPTIMIZATION: 'opt_options',
}


def fillvalue_dictionary(method, job_key, job_options=None):
    """ get the template fill values for the specific job
    """
    job_function = JOB_FUNCTION_DCT[job_key]

    job_function_args = _job_function_args(method, job_key)

    fill_dct = {
        template_keys.JOB_FUNCTION: job_function,
        template_keys.JOB_FUNCTION_ARGS: job_function_args,
    }

    if job_options is not None:
        assert job_key in JOB_OPTIONS_KEY_DCT
        fill_dct[JOB_OPTIONS_KEY_DCT[job_key]] = '\n'.join(job_options)

    return fill_dct


def _job_function_args(method, job_key):
    scf_method, corr_method = par.METHOD.split_name(method)

    job_function_args = ''
    if job_key == 'hessian':
        if scf_method == par.METHOD.UHF:
            job_function_args = 'dertype=1'
        elif scf_method == par.METHOD.ROHF and corr_method is None:
            job_function_args = 'dertype=1'

    return job_function_args
