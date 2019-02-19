""" Library of functions to retrieve structural information from a Psi4 1.0
output file
"""
import autoparse.pattern as rep
import autoparse.find as ref
import automol


def optimized_cartesian_geometry(output_string):
    """ get optimized cartesian geometry from output
    """
    # Pattern to idetify block of output string where optimized geometry is located
    start_pattern = rep.escape('Final (previous) structure:')
    end_pattern = rep.escape('Saving final (previous) structure')

    # Obtain block of output string containing the optimized geometry in xyz coordinates
    geom_block_str = ref.last_block(start_pattern, end_pattern, output_string)
    cart_geom = automol.geom.from_string(geom_block_str, strict=False)
    return cart_geom


def optimized_zmatrix_geometry(output_string):
    """ get optimized z-matrix geometry from output
    """
    # Pattern to idetify block of output string where optimized geometry is located
    start_pattern = rep.escape('Geometry (in Angstrom)')
    end_pattern = rep.escape('Removing binary optimization data file.')

    # Obtain block of output string containing the optimized geometry in zmatrix coordinates
    geom_block_str = ref.last_block(start_pattern, end_pattern, output_string)
    zmat, zmat_var_dct = automol.zmatrix.from_zmat_string(geom_block_str)
    return (zmat, zmat_var_dct)
