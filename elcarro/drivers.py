""" elstruct driver
"""
import os
import functools
import warnings
import automol
import elstruct


def feedback_optimization(script_str, run_dir,
                          prog, method, basis, geom, mult, charge,
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
                script_str, try_dir_path, elstruct.writer.optimization,
                prog, method, basis, geom, mult, charge, **kwargs)

        if has_noconv_error_(output_str):
            geom = read_geom_(output_str)
        else:
            break

    if has_noconv_error_(output_str):
        warnings.resetwarnings()
        warnings.warn("elstruct feedback optimization failed; "
                      "last try was in {}".format(run_dir))

    return input_str, output_str
