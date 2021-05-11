% if rotor_id != '':
Rotor  Hindered   # ${rotor_id}
% else:
Rotor  Hindered
% endif
% if geo:
  Geometry[angstrom]     ${natom}
${geo}
% endif
  Group                  ${group}
  Axis                   ${axis}
  Symmetry               ${symmetry}
  Potential[kcal/mol]    ${npotential}
${potential} 
% if hmin is not None:
  HamiltonSizeMin            ${hmin}
% endif
% if hmax is not None:
  HamiltonSizeMax            ${hmax}
% endif
% if lvl_ene_max is not None:
  LevelEnergyMax[kcal/mol]   ${lvl_ene_max}
% endif
% if therm_pow_max is not None:
  ThermalPowerMax      ${therm_pow_max}
% endif
End  ! HindRot
