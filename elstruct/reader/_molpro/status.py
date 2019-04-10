""" status checkers
"""
import elstruct.par
import autoparse.pattern as app
import autoparse.find as apf


def has_normal_exit_message(output_string):
    """ does this output string have a normal exit message?
    """
    pattern = app.padded(app.NEWLINE).join([
        app.escape('Molpro calculation terminated'),
        app.escape('Variable memory released')])
    return apf.has_match(pattern, output_string, case=False)


def _has_scf_nonconvergence_error_message(output_string):
    """ does this output string have an SCF non-convergence message?
    """
    pattern = app.escape('No convergence')
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
    # get the appropriate reader and call it
    error_reader = ERROR_READER_DCT[error]
    return error_reader(output_string)


if __name__ == '__main__':
    print(has_normal_exit_message(open('output.dat').read()))
    print(has_normal_exit_message(open('good_output.dat').read()))
