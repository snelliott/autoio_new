# """ gaussian09 writer module """
# import os
# from elstruct import template
# from elstruct.writer._gaussian09 import template_keys
# from elstruct.writer._gaussian09 import theory
# from elstruct.writer._gaussian09 import molecule
#
# # set the path to the template files
# THIS_DIR = os.path.dirname(os.path.realpath(__file__))
# TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')
#
#
# def method_list():
#     """ list of available electronic structure methods
#     """
#     return theory.METHOD_LST
#
#
# def basis_list():
#     """ list of available electronic structure basis sets
#     """
#     return theory.BASIS_LST
#
#
# def energy(method, basis, geom, mult, charge,
#            # molecule options
#            mol_options=(),
#            # machine options
#            memory=1, comment='', machine_options=(),
#            # theory options
#            scf_options=(), corr_options=()):
#     """ energy input string
#     """
#     assert method in method_list()
#     fill_dct = {
#         template_keys.COMMENT: comment,
#         template_keys.MEMORY: memory,
#         template_keys.MACHINE_OPTIONS: '\n'.join(machine_options),
#     }
#     fill_dct.update(molecule.fillvalue_dictionary(geom, charge, mult,
#                                                   mol_options))
#     fill_dct.update(theory.fillvalue_dictionary(method, basis, scf_options,
#                                                 corr_options))
#
#     inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
#     return inp_str
#
#
# def gradient(method, basis, geom, mult, charge,
#              # molecule options
#              mol_options=(),
#              # machine options
#              memory=1, comment='', machine_options=(),
#              # theory options
#              scf_options=(), corr_options=()):
#     """ gradient input string
#     """
#     assert method in method_list()
#     fill_dct = {
#         template_keys.COMMENT: comment,
#         template_keys.MEMORY: memory,
#         template_keys.MACHINE_OPTIONS: '\n'.join(machine_options),
#     }
#     fill_dct.update(molecule.fillvalue_dictionary(geom, charge, mult,
#                                                   mol_options))
#     fill_dct.update(theory.fillvalue_dictionary(method, basis, scf_options,
#                                                 corr_options))
#     fill_dct[template_keys.JOB_KEY] = template_keys.JobKeys.GRAD
#
#     inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
#     return inp_str
#
#
# def hessian(method, basis, geom, mult, charge,
#             # molecule options
#             mol_options=(),
#             # machine options
#             memory=1, comment='', machine_options=(),
#             # theory options
#             scf_options=(), corr_options=()):
#     """ hessian input string
#     """
#     assert method in method_list()
#     fill_dct = {
#         template_keys.COMMENT: comment,
#         template_keys.MEMORY: memory,
#         template_keys.MACHINE_OPTIONS: '\n'.join(machine_options),
#     }
#     fill_dct.update(molecule.fillvalue_dictionary(geom, charge, mult,
#                                                   mol_options))
#     fill_dct.update(theory.fillvalue_dictionary(method, basis, scf_options,
#                                                 corr_options))
#     fill_dct[template_keys.JOB_KEY] = template_keys.JobKeys.HESS
#
#     inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
#     return inp_str
#
#
# def optimization(method, basis, geom, mult, charge,
#                  # molecule options
#                  mol_options=(),
#                  # machine options
#                  memory=1, comment='', machine_options=(),
#                  # theory options
#                  scf_options=(), corr_options=(),
#                  # molecule/optimization options
#                  frozen_coordinates=(), opt_options=()):
#     """ optimization input string
#     """
#     assert method in method_list()
#     fill_dct = {
#         template_keys.COMMENT: comment,
#         template_keys.MEMORY: memory,
#         template_keys.MACHINE_OPTIONS: '\n'.join(machine_options),
#     }
#     fill_dct.update(molecule.fillvalue_dictionary(
#         geom, charge, mult, mol_options,
#         frozen_coordinates=frozen_coordinates))
#     fill_dct.update(theory.fillvalue_dictionary(
#         method, basis, scf_options, corr_options))
#     fill_dct.update({
#         template_keys.JOB_KEY: template_keys.JobKeys.OPT,
#         template_keys.OPT_OPTIONS: ', '.join(opt_options),
#     })
#
#     inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
#     return inp_str
