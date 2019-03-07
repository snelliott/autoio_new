""" functions for running directly from input arguments
"""
import warnings
from ..reader import has_error_message as _has_error_message
from . import optsmat
from ._core import direct as _direct


def robust(script_str, input_writer,
           prog, method, basis, geom, mult, charge,
           errors, options_mat,
           **kwargs):
    """ try several sets of options to generate an output file

    :returns: the input string, the output string, and the run directory
    :rtype: (str, str, str)
    """
    assert len(errors) == len(options_mat)

    while not optsmat.is_exhausted(options_mat):
        kwargs_dct = optsmat.updated_kwargs(kwargs, options_mat)

        # filter out the warnings from the trial runs
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            input_str, output_str, run_dir = _direct(
                script_str, input_writer,
                prog, method, basis, geom, mult, charge, **kwargs_dct)

        error_vals = [
            _has_error_message(prog, error, output_str) for error in errors]

        if not any(error_vals):
            break

        row_idx = error_vals.index(True)
        options_mat = optsmat.advance(row_idx, options_mat)

    if any(error_vals):
        raise RuntimeError("robust run failed; last run was in {}"
                           .format(run_dir))

    return (input_str, output_str, run_dir)
