Barrier ${ts_label} ${reac_label} ${prod_label}
${ts_data}\
## Zero Ene
% if zero_ene is not None:
   ZeroEnergy[kcal/mol]    ${zero_ene}
% endif
## Tunnel Section
% if tunnel != '':
${tunnel}
% endif
End ! Barrier
