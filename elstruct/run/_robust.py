""" functions for running directly from input arguments
"""
import os
import warnings
from elstruct.reader import has_error_message as _has_error_message
from elstruct.run import optsmat
from elstruct.run._core import direct as _direct


def robust(script_str, run_dir, input_writer,
           prog, method, basis, geom, mult, charge,
           errors, options_mat,
           **kwargs):
    """ try several sets of options to generate an output file

    :returns: the input string, the output string, and the run directory
    :rtype: (str, str, str)
    """
    assert len(errors) == len(options_mat)

    try_idx = 0
    while not optsmat.is_exhausted(options_mat):
        kwargs_dct = optsmat.updated_kwargs(kwargs, options_mat)

        try_dir_name = 'try{:d}'.format(try_idx+1)
        try_dir_path = os.path.join(run_dir, try_dir_name)
        assert not os.path.exists(try_dir_path)
        os.mkdir(try_dir_path)

        # filter out the warnings from the trial runs
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            input_str, output_str = _direct(
                script_str, try_dir_path, input_writer,
                prog, method, basis, geom, mult, charge,
                **kwargs_dct
            )

        error_vals = [
            _has_error_message(prog, error, output_str) for error in errors]

        if not any(error_vals):
            break

        try_idx += 1
        row_idx = error_vals.index(True)
        options_mat = optsmat.advance(row_idx, options_mat)

    if any(error_vals):
        raise RuntimeError("robust run failed; last run was in {}"
                           .format(run_dir))

    return input_str, output_str
