# """ theory: method and basis set
# """
# from elstruct import par
# from elstruct.writer._psi4 import template_keys
#
# METHOD_LST = (
#     par.Method.RHF,
#     par.Method.B3LYP,
# )
#
# BASIS_DCT = {
#     par.Basis.STO3G: 'sto-3g',
# }
#
# BASIS_LST = tuple(sorted(BASIS_DCT.keys()))
#
# SCF_METHOD_DCT = {
#     par.Method.B3LYP: 'b3lyp',
#     par.Method.RHF: 'rhf',
# }
#
#
# def fillvalue_dictionary(method, basis, scf_options, corr_options):
#     """ get the template fill values for method and basis set
#     """
#     method = method.lower()
#     basis = basis.lower()
#     assert method in METHOD_LST
#     assert basis in BASIS_LST
#
#     if par.Method.is_dft(method):
#         scf_method = method
#     else:
#         scf_method, corr_method = par.Method.split_name(method)
#         assert corr_method is None
#         assert corr_options == ()
#
#     fill_dct = {
#         template_keys.BASIS: BASIS_DCT[basis],
#         template_keys.SCF_METHOD: SCF_METHOD_DCT[scf_method],
#         # template_keys.CORR_METHOD: corr_method_val,
#         template_keys.SCF_OPTIONS: ', '.join(scf_options),
#         # template_keys.CORR_OPTIONS: ', '.join(corr_options),
#     }
#     return fill_dct
