""" molecule: geometry and state
"""
import automol
from . import template_keys


def fillvalue_dictionary(geom, charge, mult, mol_options):
    """ get the template fill values for molecular geometry and state
    """

    if automol.geom.is_valid(geom):
        geom_str = automol.geom.string(geom)
        zmat_setval_str = ''
    else:
        geom_str = automol.zmatrix.matrix_block_string(geom)
        zmat_setval_str = automol.zmatrix.setval_block_string(geom)

    fill_dct = {
        template_keys.GEOMETRY: geom_str,
        template_keys.ZMATRIX_VALUES: zmat_setval_str,
        template_keys.CHARGE: charge,
        template_keys.MULTIPLICITY: mult,
        template_keys.MOL_OPTIONS: '\n'.join(mol_options),
    }
    return fill_dct
