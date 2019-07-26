""" irc readers
"""

import os
from elstruct.reader._g09 import get_irc
import autofile.file


def test__irc_reader():
    """ reads the irc log file from Gaussian
        writes the information to files
    """

    # Read the output file string
    with open('output.dat', 'r') as logfile:
        OUT_STR = logfile.read()

    # Get the geometries, gradients, and Hessians
    GEOMS, GRADS, HESSIANS = get_irc(OUT_STR)

    # Make the directories
    os.system('mkdir -p geoms')
    os.system('mkdir -p grads')
    os.system('mkdir -p hessians')

    # Write the geometries, gradients, and Hessians to files
    for i, geom in enumerate(GEOMS):
        with open('geoms/geom_'+str(i+1)+'.dat', 'w') as f:
            f.write(autofile.file.write.geometry(geom))
    for i, grad in enumerate(GRADS):
        with open('grads/grad_'+str(i+1)+'.dat', 'w') as f:
            f.write(autofile.file.write.gradient(grad))
    for i, hess in enumerate(HESSIANS):
        with open('hessians/hess_'+str(i+1)+'.dat', 'w') as f:
            f.write(autofile.file.write.hessian(hess))


if __name__ == '__main__':
    test__irc_reader()
