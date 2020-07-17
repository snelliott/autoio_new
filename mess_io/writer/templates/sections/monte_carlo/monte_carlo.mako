  MonteCarlo
    MoleculeSpecification   ${atom_list}
${flux_mode_str}\
    SymmetryFactor               ${sym_factor}
    DataFile                     ${data_file_name}
    ElectronicLevels[1/cm]       ${nlevels}
${levels}
    GroundEnergy[kcal/mol]       ${ground_energy}
% if reference_energy is not None:
    ReferenceEnergy[kcal/mol]    ${reference_energy}
% endif
% if nfreqs > 0:
  NonFluxionalFrequencies[1/cm]  ${nfreqs}
${freqs}
  NoHessian
% endif
% if ref_config_file_name:
ReferenceConfiguration           ${ref_config_file_name} 
% endif
% if use_cm_shift:
  UseCMShift
% endif
