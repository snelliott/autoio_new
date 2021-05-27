""" Read various OneDMin output files
"""

import os
import numpy
from ioformat import read_text_file
import onedmin_io.reader


PATH = os.path.dirname(os.path.realpath(__file__))
LJ_OUT_STR = read_text_file(['data'], 'lj.out', PATH)
ONEDMIN_OUT_STR = read_text_file(['data'], 'onedmin.out', PATH)


def test__lennard_jones():
    """ test onedmin_io.reader.lennard_jones
    """

    ref_sigmas = (6.587188430859643, 6.908800920151311, 6.609902938887646)
    ref_epsilons = (17.88616, 15.23453, 17.731)

    sigmas, epsilons = onedmin_io.reader.lennard_jones(LJ_OUT_STR)

    assert numpy.allclose(ref_sigmas, sigmas)
    assert numpy.allclose(ref_epsilons, epsilons)


def test__program_version():
    """ test onedmin_io.reader.program_version
    """

    ref_prog = '1.0'

    prog = onedmin_io.reader.program_version(ONEDMIN_OUT_STR)

    assert prog == ref_prog


def test__ranseed():
    """ test onedmin_io.reader.random_seed_value
    """

    ref_ranseed = 153214316

    ranseed = onedmin_io.reader.random_seed_value(ONEDMIN_OUT_STR)

    assert ranseed == ref_ranseed
