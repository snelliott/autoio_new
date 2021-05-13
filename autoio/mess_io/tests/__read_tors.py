"""
 tests torsional mode reader
"""

import os
import numpy
from ioformat import read_text_file
import mess_io.reader


PATH = os.path.dirname(os.path.realpath(__file__))
OUT_STR = read_text_file(['data', 'out'], 'freq.log', PATH)


def test__freqs():
    """ test mess_io.reader.tors.analytic_frequencies
        test mess_io.reader.tors.grid_minimum_frequencies
    """

    ref_analyt_freqs = (219.082, 118.148, 124.148, 222.028, 209.659, 420.967)
    ref_gridmin_freqs = (211.585, 115.404, 104.018, 185.075, 144.794, 412.947)

    analyt_freqs = mess_io.reader.tors.analytic_frequencies(OUT_STR)
    gridmin_freqs = mess_io.reader.tors.grid_minimum_frequencies(OUT_STR)

    assert numpy.allclose(analyt_freqs, ref_analyt_freqs)
    assert numpy.allclose(gridmin_freqs, ref_gridmin_freqs)


def test__zpves():
    """ test mess_io.reader.tors.zpves
    """

    ref_zpves = (0.00048053637212001904, 0.0002661216076862006,
                 0.0002676518953394201, 0.0004898094974562318,
                 0.0004479208868480696, 0.000917415142012805)

    zpves = mess_io.reader.tors.zero_point_vibrational_energies(OUT_STR)

    assert numpy.allclose(zpves, ref_zpves)
