""" molecular geometry and structure readers
"""
import autoparse.pattern as app
import autoparse.find as apf
import automol


def opt_geometry(output_string):
    """ get optimized cartesian geometry from output
    """
    # idetify block of output string where optimized geometry is located
    start_pattern = app.escape('Final (previous) structure:')
    end_pattern = app.escape('Saving final (previous) structure')
    geom_block_str = apf.last_block(start_pattern, end_pattern, output_string)
    # parse the geometry from the block using automol
    geom = automol.geom.from_string(geom_block_str, strict=False)
    return geom


def opt_zmatrix(output_string):
    """ get optimized z-matrix geometry from output
    """
    # idetify block of output string where optimized geometry is located
    start_pattern = app.escape('Geometry (in Angstrom),')
    end_pattern = app.escape('***')
    # parse the geometry from the block using automol
    geom_block_strs = apf.all_blocks(start_pattern, end_pattern, output_string)
    zmat = automol.zmatrix.from_zmat_string(geom_block_strs[-1])
    return zmat
