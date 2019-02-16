""" machine: memory, parallelism, etc.
"""
from . import template_keys


def fillvalue_dictionary(comment, memory, machine_options):
    """ get the template fill values for job directives
    """
    fill_dct = {
        template_keys.COMMENT: comment,
        template_keys.MEMORY: memory,
        template_keys.MACHINE_OPTIONS: machine_options,
    }
    return fill_dct
