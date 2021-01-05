Well ${well_label} 
  Species
${well_data}\
## Zero Energy Section
      ZeroEnergy[kcal/mol]      ${zero_ene}
  End
## Energy Transfer Sections
% if edown_str is not None:
${edown_str}
% endif
% if collid_freq_str is not None:
${collid_freq_str}
% endif
End\
