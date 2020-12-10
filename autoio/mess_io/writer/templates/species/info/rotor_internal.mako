% if rotor_id != '':
InternalRotation   # ${rotor_id}
% else:
InternalRotation
% endif
% if geom:
  Geometry[angstrom]   ${natom}
${geom}
% endif
  Group                      ${group}
  Axis                       ${axis}
  Symmetry                   ${symmetry}
  GridSize                   ${grid_size}
  MassExpansionSize          ${mass_exp_size}
  PotentialExpansionSize     ${pot_exp_size}
  HamiltonSizeMin            ${hmin}
  HamiltonSizeMax            ${hmax}
End
\
