""" status checkers
"""
import autoparse.pattern as app
import autoparse.find as apf
import elstruct.par

# Standard Exit message for a program 
EXIT_MSG = app.escape('Normal termination of Gaussian 09')

# Convergence success messages
SCF_CONV_MSG = app.one_of_these(
    [("Initial convergence to {} achieved. ".format(app.EXPONENTIAL_FLOAT_D) +
      "Increase integral accuracy." +
      app.LINE_FILL + app.NEWLINE + app.LINE_FILL +
      app.escape('SCF Done:')),
      app.escape('Rotation gradient small -- convergence achieved.')]
OPT_CONV_MSG = (
        app.escape('Optimization completed.') +
        app.LINE_FILL + app.NEWLINE + app.LINE_FILL +
        app.escape('-- Stationary point found.'))
IRC_CONV_MSG = app.escape('Reaction path calculation complete.')

# Convergence failure messages
SCF_NOCONV_MSG = app.padded(app.NEWLINE).join([
    app.escape('Convergence criterion not met.'),
    app.escape('SCF Done:')])
OPT_NOCONV_MSG = app.padded(app.NEWLINE).join([
    app.escape('Optimization stopped.'),
    app.escape('-- Number of steps exceeded,')])
IRC_NOCONV_MSG = app.escape('Maximum number of corrector steps exceeded')


def has_normal_exit_message(output_string):
    """ does this output string have a normal exit message?
    """
    return apf.has_match(NORM_EXIT_MSG, output_string, case=False)


def has_scf_convergence_message(output_string):
    """ does this output string have a convergence success message?
    """
    return apf.has_match(SCF_CONV_MSG, output_string, case=False)


def has_opt_convergence_message(output_string):
    """ does this output string have a convergence success message?
    """
    return apf.has_match(OPT_CONV_MSG, output_string, case=False)


def has_irc_convergence_message(output_string):
    """ does this output string have a convergence success message?
    """
    return apf.has_match(IRC_CONV_MSG, output_string, case=False)


def _has_scf_nonconvergence_error_message(output_string):
    """ does this output string have an SCF non-convergence message?
    """
    return apf.has_match(pattern, output_string, case=False)


def _has_opt_nonconvergence_error_message(output_string):
    """ does this output string have an optimization non-convergence message?
    """
    return apf.has_match(pattern, output_string, case=False)


def _has_irc_nonconvergence_error_message(output_string):
    """ does this output string have an optimization non-convergence message?
    """
    pattern = app.escape('Maximum number of corrector steps exceeded')
    return apf.has_match(pattern, output_string, case=False)


ERROR_READER_DCT = {
    elstruct.par.Error.SCF_NOCONV: _has_scf_nonconvergence_error_message,
    elstruct.par.Error.OPT_NOCONV: _has_opt_nonconvergence_error_message,
    elstruct.par.Error.IRC_NOCONV: _has_irc_nonconvergence_error_message,
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
    error_found = ERROR_READER_DCT[error](output_string)
    if error_found:

    return error_reader(output_string)


if __name__ == '__main__':
    with open('output.dat', 'r') as f:
        outstr = f.read()
    with open('prod1_l1.log', 'r') as f:
        pstr = f.read()
    print(has_scf_convergence_message(outstr))
    print(has_irc_convergence_message(outstr))
    print(has_scf_convergence_message(pstr))
    print(has_opt_convergence_message(pstr))
