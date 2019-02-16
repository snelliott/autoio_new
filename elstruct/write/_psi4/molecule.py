""" molecule: geometry and state
"""
import automol
from . import template_keys


def fillvalue_dictionary(geom, charge, mult, zmat_var_dct):
    """ get the template fill values for molecular geometry and state
    """

    if automol.geom.is_valid(geom):
        geom_str = automol.geom.string(geom)
        zmat_vals = ''
    else:
        zmat_var_dct = {} if zmat_var_dct is None else zmat_var_dct
        geom_str = automol.zmatrix.zmat_string_matrix_block(geom, zmat_var_dct)
        zmat_vals = automol.zmatrix.zmat_string_variable_block(geom,
                                                               zmat_var_dct)

    fill_dct = {
        template_keys.GEOMETRY: geom_str,
        template_keys.ZMATRIX_VALUES: zmat_vals,
        template_keys.CHARGE: charge,
        template_keys.MULTIPLICITY: mult,
    }
    return fill_dct
