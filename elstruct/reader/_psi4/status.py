""" status checkers

policy:
    frame each as a positive question (i.e., boolean with False=bad, True=good)
"""
import autoparse.pattern as rep
import autoparse.find as ref


def has_normal_exit_message(output_string):
    """ does this output string have a normal exit message?
    """
    pattern = rep.escape('*** Psi4 exiting successfully.')
    return ref.has_match(pattern, output_string)
