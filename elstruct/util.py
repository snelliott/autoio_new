""" front-end reader utilities
"""
import functools
import numpy
from qcelemental import constants as qcc
import automol


def rotational_constants(geo):
    """ get the rotational constants in atomic units

    (may want to convert to other units here)
    """
    cons = automol.geom.rotational_constants(geo, amu=True)
    return cons


def normal_coordinates(geo, hess, project=True):
    """ normal coordinates
    """
    norm_coos, _, _ = _frequency_analysis(geo, hess, project=project)
    return norm_coos


def harmonic_frequencies(geo, hess, project=True):
    """ harmonic frequencies (in cm^-1)

    (imaginary entries returned as negative)
    """
    _, freqs_re, freqs_im = _frequency_analysis(geo, hess, project=project)
    freqs = numpy.subtract(freqs_re, freqs_im)
    freqs = tuple(freqs)
    return freqs


def mass_weighted_hessian(geo, hess, project=True):
    """ translation/rotation-projected mass-weighted hessian
    """
    amas = automol.geom.masses(geo, amu=False)
    mw_vec = numpy.divide(1., numpy.sqrt(numpy.repeat(amas, 3)))
    mw_mat = numpy.outer(mw_vec, mw_vec)
    mw_hess = numpy.multiply(hess, mw_mat)
    if project:
        dim = len(mw_vec)
        trans_norm_coos = translational_normal_coordinates(geo)
        rot_norm_coos = rotational_normal_coordinates(geo)
        tr_norm_coos = numpy.hstack([trans_norm_coos, rot_norm_coos])
        tr_proj = numpy.eye(dim) - numpy.dot(tr_norm_coos, tr_norm_coos.T)
        mw_hess = numpy.dot(numpy.dot(tr_proj, mw_hess), tr_proj)

    mw_hess = tuple(map(tuple, mw_hess))
    return mw_hess


def translational_normal_coordinates(geo, axes=None):
    """ translational normal coordinates
    """
    if axes is None:
        axes = numpy.eye(3)
    mw_vec = _column_vector(numpy.sqrt(automol.geom.masses(geo)))
    trans_norm_coos = _normalize_columns(numpy.kron(mw_vec, axes))
    return trans_norm_coos


def rotational_normal_coordinates(geo, axes=None):
    """ rotational normal coordinates
    """
    if axes is None:
        axes = numpy.eye(3)
    xyzs = numpy.array(automol.geom.coordinates(geo))
    mw_vec = _column_vector(numpy.sqrt(automol.geom.masses(geo)))
    mw_xyzs = numpy.multiply(xyzs, mw_vec)
    cross_mw_xyzs = functools.partial(numpy.cross, mw_xyzs)
    rot_norm_coos = _normalize_columns(numpy.hstack(
        list(map(_column_vector, map(cross_mw_xyzs, axes.T)))))
    return rot_norm_coos


def _frequency_analysis(geo, hess, project=True):
    """ harmonic frequency analysis
    """
    amas = automol.geom.masses(geo, amu=False)
    mw_vec = numpy.divide(1., numpy.sqrt(numpy.repeat(amas, 3)))
    mw_hess = mass_weighted_hessian(geo, hess, project=project)
    fcs, mw_norm_coos = numpy.linalg.eigh(mw_hess)

    conv = qcc.conversion_factor("hartree", "wavenumber")
    freqs = numpy.sqrt(numpy.complex_(fcs)) * conv
    freqs_im = numpy.imag(freqs)
    freqs_re = numpy.real(freqs)

    norm_coos = mw_vec * mw_norm_coos
    return norm_coos, freqs_re, freqs_im


def _normalize_columns(mat):
    """normalize the columns of a matrix
    :param mat: matrix
    :type mat: numpy.ndarray
    :rtype: numpy.ndarray
    """
    norms = list(map(numpy.linalg.norm, numpy.transpose(mat)))
    return numpy.divide(mat, norms)


def _column_vector(vec):
    """form an n x 1 column vector, flattening if necessary
    :param vec: vector or array
    :type vec: numpy.ndarray
    :rtype: numpy.ndarray
    """
    return numpy.reshape(vec, (-1, 1))
