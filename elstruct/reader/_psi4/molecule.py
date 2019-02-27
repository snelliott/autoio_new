""" molecular geometry and structure readers
"""
import autoparse.pattern as rep
import autoparse.find as ref
import automol


def optimized_geometry(output_string):
    """ get optimized cartesian geometry from output
    """
    # idetify block of output string where optimized geometry is located
    start_pattern = rep.escape('Final (previous) structure:')
    end_pattern = rep.escape('Saving final (previous) structure')
    geom_block_str = ref.last_block(start_pattern, end_pattern, output_string)
    # parse the geometry from the block using automol
    geom = automol.geom.from_string(geom_block_str, strict=False)
    return geom


def optimized_zmatrix(output_string):
    """ get optimized z-matrix geometry from output
    """
    # idetify block of output string where optimized geometry is located
    start_pattern = rep.escape('Geometry (in Angstrom)')
    end_pattern = rep.escape('Removing binary optimization data file.')
    # parse the geometry from the block using automol
    geom_block_str = ref.last_block(start_pattern, end_pattern, output_string)
    zmat = automol.zmatrix.from_zmat_string(geom_block_str)
    return zmat
