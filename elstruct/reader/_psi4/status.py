""" status checkers
"""
import autoparse.pattern as rep
import autoparse.find as ref


def has_normal_exit_message(output_string):
    """ does this output string have a normal exit message?
    """
    pattern = rep.escape('*** Psi4 exiting successfully.')
    return ref.has_match(pattern, output_string, case=False)


def has_scf_nonconvergence_message(output_string):
    """ does this output string have an SCF non-convergence message?
    """
    pattern = rep.escape('PsiException: Could not converge SCF iterations')
    return ref.has_match(pattern, output_string, case=False)


def has_opt_nonconvergence_message(output_string):
    """ does this output string have an optimization non-convergence message?
    """
    pattern = rep.escape('PsiException: Could not converge geometry '
                         'optimization')
    return ref.has_match(pattern, output_string, case=False)
