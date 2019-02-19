""" input writing module

(look at the module_template for the function signatures and docstrings)
"""
from . import module_template
from .. import program_modules as pm


def optimized_cartesian_geometry(prog, *args, **kwargs):
    """ _ """
    return pm.call_module_function(
        prog, 'read', module_template.optimized_cartesian_geometry,
        *args, **kwargs
    )
