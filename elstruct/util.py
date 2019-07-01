""" front-end reader utilities
"""
import numpy
from qcelemental import constants as qcc
import automol


def rotational_constants(geo):
    """ get the rotational constants in atomic units

    (may want to convert to other units here)
    """
    cons = automol.geom.rotational_constants(geo, amu=True)
    return cons


def normal_coordinates(geo, hess):
    """ normal coordinates
    """
    norm_coos, _, _ = _frequency_analysis(geo, hess)
    return norm_coos


def harmonic_frequencies(geo, hess):
    """ harmonic frequencies (in cm^-1)

    (imaginary entries returned as negative)
    """
    freqs = numpy.subtract(real_harmonic_frequencies(geo, hess),
                           imaginary_harmonic_frequencies(geo, hess))
    freqs = tuple(freqs)
    return freqs


def real_harmonic_frequencies(geo, hess):
    """ real harmonic frequencies
    """
    _, freqs_re, _ = _frequency_analysis(geo, hess)
    return freqs_re


def imaginary_harmonic_frequencies(geo, hess):
    """ imaginary harmonic frequencies
    """
    _, _, freqs_im = _frequency_analysis(geo, hess)
    return freqs_im


def _frequency_analysis(geo, hess):
    """ harmonic frequency analysis
    """
    amas = automol.geom.masses(geo, amu=False)
    mw_vec = numpy.divide(1., numpy.sqrt(numpy.repeat(amas, 3)))
    mw_mat = numpy.outer(mw_vec, mw_vec)
    mw_hess = numpy.multiply(hess, mw_mat)
    mw_hess = tuple(map(tuple, mw_hess))
    fcs, mw_norm_coos = numpy.linalg.eigh(mw_hess)

    conv = qcc.conversion_factor("hartree", "wavenumber")
    freqs = numpy.sqrt(numpy.complex_(fcs)) * conv
    freqs_im = numpy.imag(freqs)
    freqs_re = numpy.real(freqs)

    norm_coos = mw_vec * mw_norm_coos
    return norm_coos, freqs_re, freqs_im
