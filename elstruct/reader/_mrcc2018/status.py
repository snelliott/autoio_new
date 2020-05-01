""" status checkers
"""
import autoparse.pattern as app
import autoparse.find as apf
import elstruct.par


def has_normal_exit_message(output_string):
    """ does this output string have a normal exit message?
    """
    pattern = app.escape('Normal termination of mrcc.')
    return apf.has_match(pattern, output_string, case=False)


def _has_scf_nonconvergence_error_message(output_string):
    """ does this output string have an SCF non-convergence message?
    """
    pattern = app.padded(app.NEWLINE).join([
        app.escape('THE SCF ITERATION HAS NOT CONVERGED,'),
        app.escape('IN MAXIMAL NUMBER OF STEPS SET BY USER!')
    ])
    return apf.has_match(pattern, output_string, case=False)


ERROR_READER_DCT = {
    elstruct.par.Error.SCF_NOCONV: _has_scf_nonconvergence_error_message,
}


def error_list():
    """ list of errors that be identified from the output file
    """
    return tuple(sorted(ERROR_READER_DCT.keys()))


def has_error_message(error, output_string):
    """ does this output string have an error message?
    """
    assert error in error_list()
    error_reader = ERROR_READER_DCT[error]
    return error_reader(output_string)


def check_convergence_messages(error, success, output_string):
    """ check if error messages should trigger job success or failure
    """
    assert error in error_list()
    # assert success in sucess_list()
    _ = success

    job_success = True
    has_error = ERROR_READER_DCT[error](output_string)
    if has_error:
        job_success = False

    return job_success
