""" elstruct driver
"""
import os
import functools
import warnings
import automol
import elstruct
from elcarro import optsmat


def robust_run(input_writer, script_str, run_dir,
               geom, charge, mult, method, basis, prog,
               errors=(), options_mat=(),
               **kwargs):
    """ try several sets of options to generate an output file

    :returns: the input string, the output string, and the run directory
    :rtype: (str, str, str)
    """
    assert len(errors) == len(options_mat)

    try_idx = 0
    kwargs_dct = dict(kwargs)
    while not optsmat.is_exhausted(options_mat):
        try_dir_name = 'try{:d}'.format(try_idx)
        try_dir_path = os.path.join(run_dir, try_dir_name)
        assert not os.path.exists(try_dir_path)
        os.mkdir(try_dir_path)

        # filter out the warnings from the trial runs
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            input_str, output_str = elstruct.run.direct(
                input_writer, script_str, try_dir_path,
                geom=geom, charge=charge, mult=mult, method=method,
                basis=basis, prog=prog, **kwargs_dct)

        error_vals = [
            elstruct.reader.has_error_message(prog, error, output_str)
            for error in errors]

        if not any(error_vals):
            break

        try_idx += 1
        row_idx = error_vals.index(True)
        options_mat = optsmat.advance(row_idx, options_mat)
        kwargs_dct = optsmat.updated_kwargs(kwargs, options_mat)

    if (any(error_vals) or not
            elstruct.reader.has_normal_exit_message(prog, output_str)):
        warnings.resetwarnings()
        warnings.warn("elstruct robust run failed; last run was in {}"
                      .format(run_dir))

    return input_str, output_str


def feedback_optimization(script_str, run_dir,
                          geom, charge, mult, method, basis, prog,
                          ntries=3, **kwargs):
    """ retry an optimization from the last (unoptimized) structure
    """
    assert automol.geom.is_valid(geom) or automol.zmatrix.is_valid(geom)
    is_zmat = automol.zmatrix.is_valid(geom)
    read_geom_ = (elstruct.reader.opt_geometry_(prog) if not is_zmat else
                  elstruct.reader.opt_zmatrix_(prog))
    has_noconv_error_ = functools.partial(
        elstruct.reader.has_error_message, prog, elstruct.Error.OPT_NOCONV)

    for try_idx in range(ntries):
        try_dir_name = 'try{:d}'.format(try_idx)
        try_dir_path = os.path.join(run_dir, try_dir_name)
        assert not os.path.exists(try_dir_path)
        os.mkdir(try_dir_path)

        # filter out the warnings from the trial runs
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            input_str, output_str = elstruct.run.direct(
                elstruct.writer.optimization, script_str, try_dir_path,
                geom=geom, charge=charge, mult=mult, method=method,
                basis=basis, prog=prog, **kwargs)

        if has_noconv_error_(output_str):
            geom = read_geom_(output_str)
        else:
            break

    if has_noconv_error_(output_str):
        warnings.resetwarnings()
        warnings.warn("elstruct feedback optimization failed; "
                      "last try was in {}".format(run_dir))

    return input_str, output_str
