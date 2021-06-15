""" status checkers
"""
import autoparse.pattern as app
import autoparse.find as apf
import elstruct.par


# Exit message for the program
def has_normal_exit_message(output_str):
    """ does this output string have a normal exit message?
    """
    pattern = app.escape('*** Psi4 exiting successfully.')
    return apf.has_match(pattern, output_str, case=False)


# Parsers for convergence success messages
def _has_scf_convergence_message(output_str):
    """ does this output string have a convergence success message?
    """
    scf_str1 = 'Energy and wave function converged'
    pattern = app.one_of_these([scf_str1])
    return apf.has_match(pattern, output_str, case=True)


def _has_opt_convergence_message(output_str):
    """ does this output string have a convergence success message?
    """
    pattern = app.escape('**** Optimization is complete!')
    return apf.has_match(pattern, output_str, case=True)


# Parsers for various error messages
def _has_scf_nonconvergence_error_message(output_str):
    """ does this output string have an SCF non-convergence message?
    """
    pattern = app.one_of_these([
        app.escape('PsiException: Could not converge SCF iterations'),
        app.escape('Failed to converge.')
    ])
    return apf.has_match(pattern, output_str, case=False)


def _has_opt_nonconvergence_error_message(output_str):
    """ does this output string have an optimization non-convergence message?
    """
    pattern = app.escape('PsiException: Could not converge geometry '
                         'optimization')
    return apf.has_match(pattern, output_str, case=False)


def _has_symmetry_detection_error_message(output_str):
    """ does this output string have an optimization non-convergence message?
    """
    pattern = app.escape('Unrecognized point group bits:')
    return apf.has_match(pattern, output_str, case=False)


ERROR_READER_DCT = {
    elstruct.par.Error.SCF_NOCONV: _has_scf_nonconvergence_error_message,
    elstruct.par.Error.OPT_NOCONV: _has_opt_nonconvergence_error_message,
    elstruct.par.Error.SYMM_NOFIND: _has_symmetry_detection_error_message
}
SUCCESS_READER_DCT = {
    elstruct.par.Success.SCF_CONV: _has_scf_convergence_message,
    elstruct.par.Success.OPT_CONV: _has_opt_convergence_message,
}


def error_list():
    """ list of errors that be identified from the output file
    """
    return tuple(sorted(ERROR_READER_DCT.keys()))


def success_list():
    """ list of errors that be identified from the output file
    """
    return tuple(sorted(SUCCESS_READER_DCT.keys()))


def has_error_message(error, output_str):
    """ does this output string have an error message?
    """
    assert error in error_list()
    # get the appropriate reader and call it
    error_reader = ERROR_READER_DCT[error]
    return error_reader(output_str)


def check_convergence_messages(error, success, output_str):
    """ check if error messages should trigger job success or failure
    """
    assert error in error_list()
    assert success in success_list()

    job_success = False
    has_error = ERROR_READER_DCT[error](output_str)
    if has_error:
        print('has error:', error)
        has_success = SUCCESS_READER_DCT[success](output_str)
        if has_success:
            job_success = True
    else:
        job_success = True

    return job_success
