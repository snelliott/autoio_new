""" template interface, using mako
"""
import os
from mako.template import Template


def read_and_fill(template_dir, template_name, fill_dct):
    """ read in a template from a tempalte directory and return the filled
    template string
    """
    template_path = os.path.join(template_dir, template_name)
    template_obj = Template(filename=template_path)
    filled_template_str = template_obj.render(**fill_dct)
    return filled_template_str
