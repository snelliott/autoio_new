""" Tests the writing of the energy transfer section
"""

import os
import numpy
import onedmin_io


PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(PATH, 'data')
DATA_NAME = 'onedmin.out'
# with open(os.path.join(DATA_PATH, DATA_NAME), 'r') as datfile:
#    OUT_STR = datfile.read()


def test__lennard_jones():
    """ test onedmin_io.reader.lennard_jones
    """

    ref_sigmas = ()
    ref_epsilons = ()

    # sigmas, epsilons = onedmin_io.reader.lennard_jones(OUT_STR)

    # assert numpy.allclose(ref_sigmas, sigmas)
    # assert numpy.allclose(ref_epsilons, epsilons)


if __name__ == '__main__':
    test__lennard_jones()
