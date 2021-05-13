""" Generate the information necessary to product the vrctst input files
"""

# import os
# import autofile
# import automol
# import varecof_io
# from phydat import phycon
# from autorun._run import run_script
# from autorun._run import from_input_string
#
#
# # Default names of input and output files
# INPUT_NAME = 'tst.inp'
# AUX_NAMES = (
#     'structure.inp',
#     'divsur.inp',
#     'lr_divsur.inp',
#     'molpro.inp',
#     'mol.tml',
#     'mc_flux.inp',
#     'convert.inp',
#     'machines',
#     'molpro.sh')
# POT_INPUT_NAMES = (
#     '{}_corr.f'
#     'dummy_corr.f',
#     'pot_aux.f',
#     'makefile')
#
# # Names of strings, files that go into the input
# DUMMY_NAME = 'dummy_corr_'
# LIB_NAME = 'libcorrpot.so'
# EXE_NAME = 'molpro.sh'
# SPC_NAME = 'mol'
# GEOM_PTT = 'GEOMETRY_HERE'
# ENE_PTT = 'molpro_energy'
#
# # Default nmaes of output
# POT_OUTPUT_NAMES = (
#     'libcorrpot.so',)
#
# OUTPUT_NAMES = ('flux.out',)
# DIVSUR_OUTPUT_NAMES1 = ('divsur.out',)
#
#
# # Specialized runners
# def flux_file(script_str, run_dir):
#     """  Calculate the flux file
#     """
# #              aux_dct=None,
# #              input_name=INPUT_NAME, output_names=OUTPUT_NAMES):
# #
# #     # output_strs = direct()
# #
#     print(
#         'Generating flux file with TS N(E) from VaReCoF output...')
#     run_script(script_str, run_dir)
# #
# #     with open():
# #         flux_str = fobj.read()
# #
# #     return flux_str
#
#
# # General runners
# def direct(script_str, run_dir,
#            aux_dct=None,
#            input_name=INPUT_NAME, output_names=OUTPUT_NAMES):
#     """ Builds all of the VaReCoF input and then returns the output strings
#     """
#
#     input_str, aux_dcr = _write_varecof_input()
#
#     # Run VaReCoF
#     output_strs = from_input_string(
#         script_str, run_dir, input_str,
#         aux_dct=aux_dct,
#         input_name=input_name,
#         output_names=output_names)
#
#     return output_strs
#
#
# # Helpful runners for the more directly called ones
# def compile_potentials(vrc_path, mep_distances, potentials,
#                        bnd_frm_idxs, fortran_compiler,
#                        dist_restrict_idxs=(),
#                        pot_labels=(),
#                        pot_file_names=(),
#                        spc_name='mol'):
#     """  use the MEP potentials to compile the correction potential .so file
#     """
#
#     # Change the coordinates of the MEP distances
#     # mep_distances = [dist * phycon.BOHR2ANG for dist in mep_distances]
#
#     # Build string Fortan src file containing correction potentials
#     species_corr_str = varecof_io.writer.corr_potentials.species(
#         mep_distances,
#         potentials,
#         bnd_frm_idxs,
#         dist_restrict_idxs=dist_restrict_idxs,
#         pot_labels=pot_labels,
#         species_name=spc_name)
#
#     # Build string dummy corr file where no correction used
#     dummy_corr_str = varecof_io.writer.corr_potentials.dummy()
#
#     # Build string for auxiliary file needed for spline fitting
#     pot_aux_str = varecof_io.writer.corr_potentials.auxiliary()
#
#     # Build string for makefile to compile corr pot file into .so file
#     makefile_str = varecof_io.writer.corr_potentials.makefile(
#         fortran_compiler, pot_file_names=pot_file_names)
#
#     # Write all of the files needed to build the correction potential
#     with open(os.path.join(vrc_path, spc_name+'_corr.f'), 'w') as corr_file:
#         corr_file.write(species_corr_str)
#     with open(os.path.join(vrc_path, 'dummy_corr.f'), 'w') as corr_file:
#         corr_file.write(dummy_corr_str)
#     with open(os.path.join(vrc_path, 'pot_aux.f'), 'w') as corr_file:
#         corr_file.write(pot_aux_str)
#     with open(os.path.join(vrc_path, 'makefile'), 'w') as corr_file:
#         corr_file.write(makefile_str)
#
#     # Compile the correction potential
#     varecof_io.writer.corr_potentials.compile_corr_pot(vrc_path)
#
#     # Maybe read the potential and return it, prob not needed
#
#
# def frame_oriented_structure(vrc_path, script_str, divsur_inp_str):
#     """ get the divsur.out string containing divsur-frame geoms
#     """
#
#     # Have to to path with divsur.inp to run script (maybe can fix)
#     os.chdir(vrc_path)
#
#     # Run the VaReCoF utility script to get the divsur.out file
#     # Contains the fragment geometries in the divsur-defined coord sys
#     varecof_io.writer.util.divsur_frame_geom_script()
#
#     # Read fragment geoms from divsur.out with coordinates in the divsurframe
#     # with open(os.path.join(vrc_path, 'divsur.out'), 'r') as divsur_file:
#     #    output_string = divsur_file.read()
#
#     # geoms = varecof_io.reader.__(output_string)
#
#     # return geoms
#
#
# # STUFF FROM MECHDRIVER
# def _write_varecof_input(ref_zma, ts_info, ts_formula, high_mul,
#                          rct_ichs, rct_info, rct_zmas,
#                          active_space, mod_var_sp1_thy_info,
#                          npot, inf_sep_ene,
#                          min_idx, max_idx,
#                          vrc_dct, vrc_path, script_str):
#     """ prepare all the input files for a vrc-tst calculation
#     """
#
#     r1dists_lr = vrc_dct['r1dists_lr']
#     r1dists_sr = vrc_dct['r1dists_sr']
#     r2dists_sr = vrc_dct['r2dists_sr']
#     d1dists = vrc_dct['d1dists']
#     d2dists = vrc_dct['d2dists']
#     conditions = vrc_dct['conditions']
#     nsamp_max = vrc_dct['nsamp_max']
#     nsamp_min = vrc_dct['nsamp_min']
#     flux_err = vrc_dct['flux_err']
#     pes_size = vrc_dct['pes_size']
#     base_name = vrc_dct['base_name']
#     # exe_path = vrc_dct['exe_path']
#
#     # Build geometries needed for the varecof run
#     total_geom, frag_geoms, frag_geoms_wdummy = fragment_geometries(
#         ref_zma, rct_zmas, min_idx, max_idx)
#
#     # Set information for the pivot points needed in divsur.inp
#     frames, npivots = build_pivot_frames(
#         min_idx, max_idx, total_geom, frag_geoms, frag_geoms_wdummy)
#     pivot_angles = calc_pivot_angles(frag_geoms, frag_geoms_wdummy, frames)
#     pivot_xyzs = calc_pivot_xyzs(min_idx, max_idx, total_geom, frag_geoms)
#
#     # Write the long- and short-range divsur input files
#     lrdivsur_inp_str = varecof_io.writer.input_file.divsur(
#         r1dists_lr, 1, 1, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
#
#     # Write the short-range divsur files
#     t1angs = [pivot_angles[0]] if pivot_angles[0] is not None else []
#     t2angs = [pivot_angles[1]] if pivot_angles[1] is not None else []
#     if automol.geom.is_atom(frag_geoms[0]):
#         d1dists = []
#         t1angs = []
#     if automol.geom.is_atom(frag_geoms[1]):
#         d2dists = []
#         t2angs = []
#     if automol.geom.is_linear(frag_geoms[0]):
#         d1dists = [0.]
#         t1angs = []
#     if automol.geom.is_linear(frag_geoms[1]):
#         d2dists = [0.]
#         t2angs = []
#     if all(npiv > 1 for npiv in npivots):
#         r2dists = r2dists_sr
#     else:
#         r2dists = []
#         ioprinter.warning_message('no r2dist')
#
#     srdivsur_inp_str = varecof_io.writer.input_file.divsur(
#         r1dists_sr, npivots[0], npivots[1], pivot_xyzs[0], pivot_xyzs[1],
#         frame1=frames[0], frame2=frames[1],
#         d1dists=d1dists, d2dists=d2dists,
#         t1angs=t1angs, t2angs=t2angs,
#         r2dists=r2dists,
#         **conditions)
#
#     # Build the structure input file string
#     struct_inp_str = varecof_io.writer.input_file.structure(
#         frag_geoms_wdummy[0], frag_geoms_wdummy[1])
#
#     # Write the structure and divsur files to get the divsur out file
#     inp = ((
#         (struct_inp_str, 'structure.inp'), (srdivsur_inp_str, 'divsur.inp')))
#     _write_varecof_inp(inp, vrc_path)
#
#     # Obtain the divsur.out file with divsur-frame fragment geoms
#     divsur_out_str = build_divsur_out_file(vrc_path, os.getcwd())
#
#     # Write the tst.inp file
#     faces, faces_symm = assess_face_symmetries(divsur_out_str)
#     tst_inp_str = varecof_io.writer.input_file.tst(
#         nsamp_max, nsamp_min, flux_err, pes_size,
#         faces=faces, faces_symm=faces_symm)
#
#     # Write the molpro executable and potential energy surface input string
#     els_inp_str = varecof_io.writer.input_file.elec_struct(
#         vrc_path, base_name, npot,
#         dummy_name='dummy_corr_', lib_name='libcorrpot.so',
#         exe_name='molpro.sh',
#         geom_ptt='GEOMETRY_HERE', ene_ptt='molpro_energy')
#
#     # Write the electronic structure template file
#     tml_inp_str = _build_molpro_template_str(
#         ref_zma, ts_info, ts_formula, high_mul,
#         rct_ichs, rct_info,
#         active_space, mod_var_sp1_thy_info,
#         inf_sep_ene)
#
#     # Write the mc_flux.inp input string
#     mc_flux_inp_str = varecof_io.writer.input_file.mc_flux()
#
#     # Write the convert.inp input string
#     conv_inp_str = varecof_io.writer.input_file.convert()
#
#     # Write machines file to set compute nodes
#     machine_file_str = build_machinefile_str()
#
#     # Collate the input strings and write the remaining files
#     input_strs = (
#         lrdivsur_inp_str, tst_inp_str,
#         els_inp_str, tml_inp_str,
#         mc_flux_inp_str, conv_inp_str,
#         machine_file_str, script_str)
#     input_names = (
#         'lr_divsur.inp', 'tst.inp',
#         'molpro.inp', 'mol.tml',
#         'mc_flux.inp', 'convert.inp',
#         'machines', 'molpro.sh')
#     inp = tuple(zip(input_strs, input_names))
#     _write_varecof_inp(inp, vrc_path)
#
#
# def _build_molpro_template_str(ref_zma, ts_info, ts_formula, high_mul,
#                                rct_ichs, rct_info,
#                                active_space, mod_var_sp1_thy_info,
#                                inf_sep_ene):
#     """ Write the electronic structure template file
#     """
#
#     cas_kwargs = wfn.build_wfn(ref_zma, ts_info, ts_formula, high_mul,
#                                rct_ichs, rct_info,
#                                active_space, mod_var_sp1_thy_info)
#
#     tml_inp_str = wfn.wfn_string(
#         ts_info, mod_var_sp1_thy_info, inf_sep_ene, cas_kwargs)
#
#     return tml_inp_str
#
#
# VRC_DCT = {
#         'fortran_compiler': 'gfortran',
#         'base_name': 'mol',
#         'spc_name': 'mol',
#         'memory': 4.0,
#         'r1dists_lr': [8., 6., 5., 4.5, 4.],
#         'r1dists_sr': [4., 3.8, 3.6, 3.4, 3.2, 3., 2.8, 2.6, 2.4, 2.2],
#         'r2dists_sr': [4., 3.8, 3.6, 3.4, 3.2, 3., 2.8, 2.6, 2.4, 2.2],
#         'd1dists': [0.01, 0.5, 1.],
#         'd2dists': [0.01, 0.5, 1.],
#         'conditions': {},
#         'nsamp_max': 2000,
#         'nsamp_min': 50,
#         'flux_err': 10,
#         'pes_size': 2,
#     }
