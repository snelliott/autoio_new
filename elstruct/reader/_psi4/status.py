""" status checkers
"""
import autoparse.pattern as rep
import autoparse.find as ref


def ran_successfully(output_string):
    """ did this job run successfully?
    """
    pattern = rep.escape('*** Psi4 exiting successfully.')
    return ref.has_match(pattern, output_string)
