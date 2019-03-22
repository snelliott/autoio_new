""" molecule: geometry and state
"""
import automol
import automol.writers.zmatrix
from elstruct.writer._gaussian09 import template_keys


def fillvalue_dictionary(geom, charge, mult, mol_options,
                         frozen_coordinates=()):
    """ get the template fill values for molecular geometry and state
    """
    if automol.geom.is_valid(geom):
        geom_str = automol.geom.string(geom)
        zmat_var_val_str = ''
        zmat_const_val_str = ''
    else:
        geom_str = automol.zmatrix.matrix_block_string(geom)
        val_dct = automol.zmatrix.values(geom, angstrom=True, degree=True)
        var_val_dct = {key: val for key, val in val_dct.items()
                       if key not in frozen_coordinates}
        const_val_dct = {key: val for key, val in val_dct.items()
                         if key in frozen_coordinates}
        zmat_var_val_str = automol.writers.zmatrix.setval_block_string(
            var_val_dct, setval_sign=' ').strip()
        zmat_const_val_str = automol.writers.zmatrix.setval_block_string(
            const_val_dct, setval_sign=' ').strip()

    fill_dct = {
        template_keys.MOL_OPTIONS: ', '.join(mol_options),
        template_keys.CHARGE: charge,
        template_keys.MULTIPLICITY: mult,
        template_keys.GEOMETRY: geom_str,
        template_keys.ZMATRIX_VARIABLE_VALUES: zmat_var_val_str,
        template_keys.ZMATRIX_CONSTANT_VALUES: zmat_const_val_str,
    }
    return fill_dct
