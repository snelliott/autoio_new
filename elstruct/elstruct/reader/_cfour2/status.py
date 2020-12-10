""" status checkers
"""

import autoparse.pattern as app
import autoparse.find as apf
import elstruct.par


def has_normal_exit_message(output_string):
    """ does this output string have a normal exit message?
    """
    pattern = ('The final electronic energy is' +
               app.one_or_more(app.WILDCARD) +
               'This computation required')
    return apf.has_match(pattern, output_string, case=False)


def _has_scf_nonconvergence_error_message(output_string):
    """ does this output string have an SCF non-convergence message?
    """
    pattern = 'SCF failed to converge'
    return apf.has_match(pattern, output_string, case=False)


def _has_scf_convergence_message(output_string):
    """ does this output string have an SCF convergence message?
    """
    pattern = 'SCF has converged.'
    return apf.has_match(pattern, output_string, case=False)


def _has_cc_nonconvergence_error_message(output_string):
    """ does this output string have an CC non-convergence message?
    """
    pattern = app.escape('CC did not converge !!!')
    return apf.has_match(pattern, output_string, case=False)


def _has_cc_convergence_message(output_string):
    """ does this output string have an CC convergence message?
    """
    pattern = app.escape('timing for (T)')
    match = apf.has_match(pattern, output_string, case=False)
    if match is None:
        pattern = (
            'A miracle come to pass. The CC iterations have converged.')
        match = apf.has_match(pattern, output_string, case=False)
    return match


def _has_opt_nonconvergence_error_message(output_string):
    """ does this output string have an optimization non-convergence message?
    """
    pattern = app.escape('*Maximum number of optimization steps exceeded.')
    return apf.has_match(pattern, output_string, case=False)


def _has_opt_convergence_message(output_string):
    """ does this output string have an optimization convergence message?
    """
    pattern = app.escape(
        'Convergence criterion satisfied.  Optimization completed.')
    return apf.has_match(pattern, output_string, case=False)


ERROR_READER_DCT = {
    elstruct.par.Error.SCF_NOCONV: _has_scf_nonconvergence_error_message,
    elstruct.par.Error.CC_NOCONV: _has_cc_nonconvergence_error_message,
    elstruct.par.Error.OPT_NOCONV: _has_opt_nonconvergence_error_message,
}
SUCCESS_READER_DCT = {
    elstruct.par.Success.SCF_CONV: _has_scf_convergence_message,
    elstruct.par.Success.CC_CONV: _has_cc_convergence_message,
    elstruct.par.Success.OPT_CONV: _has_opt_convergence_message,
}


def error_list():
    """ list of errors that be identified from the output file
    """
    return tuple(sorted(ERROR_READER_DCT.keys()))


def success_list():
    """ list of sucesss that be identified from the output file
    """
    return tuple(sorted(SUCCESS_READER_DCT.keys()))


def has_error_message(error, output_string):
    """ does this output string have an error message?
    """
    assert error in error_list()
    # get the appropriate reader and call it
    error_reader = ERROR_READER_DCT[error]
    return error_reader(output_string)


def check_convergence_messages(error, success, output_string):
    """ check if error messages should trigger job success or failure
    """
    assert error in error_list()
    assert success in success_list()

    job_success = True
    has_error = ERROR_READER_DCT[error](output_string)
    if has_error:
        job_success = False

    return job_success
