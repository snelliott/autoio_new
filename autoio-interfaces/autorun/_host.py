""" Library used to obtain various information about the
    shell process and run node that is associated with the
    MechDriver calculations the user launched.
"""

import os
import subprocess


def host_node():
    """ Calls the BASH `hostname` command to obtain the name of the
        node server that MechDriver is running on.

        :rtype: str
    """
    host_node = subprocess.check_output(['hostname'])
    host_node = host_node.decode('ascii')
    host_node = host_node.strip()

    return host_node


def process_id():
    """ Gets the shell process ID for the MechDriver process running.

        :rtype: int
    """
    return os.getpid()

