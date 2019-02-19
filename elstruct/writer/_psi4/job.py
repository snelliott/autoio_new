""" job: energy, optimization, frequency, etc
"""
from ... import params as par
from . import template_keys

JOB_FUNCTION_DCT = {
    par.JOB.ENERGY: 'energy',
    par.JOB.OPTIMIZATION: 'optimize',
}

JOB_OPTIONS_KEY_DCT = {
    par.JOB.OPTIMIZATION: 'opt_options',
}


def fillvalue_dictionary(job_key, job_options=None):
    """ get the template fill values for the specific job
    """
    job_function = JOB_FUNCTION_DCT[job_key]

    fill_dct = {
        template_keys.JOB_FUNCTION: job_function,
    }

    if job_options is not None:
        assert job_key in JOB_OPTIONS_KEY_DCT
        fill_dct[JOB_OPTIONS_KEY_DCT[job_key]] = job_options

    return fill_dct
