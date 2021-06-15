Bimolecular ${bimolec_label} 
!---------------------------------------------------
  Fragment ${species1_label}
${species1_data}\
% if not isatom1:
      ZeroEnergy[kcal/mol]    0.0
% endif
  End  ! Frag1
!---------------------------------------------------
  Fragment ${species2_label}
${species2_data}\
% if not isatom2:
      ZeroEnergy[kcal/mol]    0.0
% endif
  End  ! Frag2
!---------------------------------------------------
  GroundEnergy[kcal/mol]    ${ground_energy}
End  ! Bimol\
