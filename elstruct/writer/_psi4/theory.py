""" theory: method and basis set
"""
from ... import params as par
from . import template_keys

METHOD_LST = (
    par.METHOD.RHF,
    par.METHOD.RHF_MP2,
    par.METHOD.UHF,
    par.METHOD.UHF_MP2,
    par.METHOD.ROHF,
    par.METHOD.ROHF_MP2,
)

BASIS_DCT = {
    par.BASIS.STO3G: 'sto-3g',
    par.BASIS.P321G: '3-21g',
    par.BASIS.P631G: '6-31g',
    par.BASIS.PVDZ: 'cc-pvdz',
}

BASIS_LST = tuple(sorted(BASIS_DCT.keys()))

SCF_METHOD_DCT = {
    par.METHOD.SCF.RHF: 'rhf',
    par.METHOD.SCF.UHF: 'uhf',
    par.METHOD.SCF.ROHF: 'rohf',
}

CORR_METHOD_DCT = {
    par.METHOD.CORR.MP2: 'mp2',
}


def fillvalue_dictionary(method, basis, scf_options, corr_options):
    """ get the template fill values for method and basis set
    """
    assert method in METHOD_LST
    assert basis in BASIS_LST

    scf_method, corr_method = par.METHOD.split_name(method)
    corr_method_val = (CORR_METHOD_DCT[corr_method]
                       if corr_method is not None else '')

    # make sure we aren't setting corr_options for an SCF job
    if corr_method_val == '':
        assert corr_options == ''

    fill_dct = {
        template_keys.BASIS: BASIS_DCT[basis],
        template_keys.SCF_METHOD: SCF_METHOD_DCT[scf_method],
        template_keys.CORR_METHOD: corr_method_val,
        template_keys.SCF_OPTIONS: scf_options,
        template_keys.CORR_OPTIONS: corr_options,
    }
    return fill_dct
