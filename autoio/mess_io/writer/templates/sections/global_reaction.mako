!===================================================
!  GLOBAL KEYWORD SECTION
!===================================================
TemperatureList[K]                     ${temperatures}
PressureList[atm]                      ${pressures}
!
EnergyStepOverTemperature              .2
% if excess_ene_temp is not None:
ExcessEnergyOverTemperature            ${excess_ene_temp}
% endif
ModelEnergyLimit[kcal/mol]             800
!
CalculationMethod                      direct
!
WellCutoff                             10
% if well_extend is not None:
WellExtension                          ${well_extend}
% endif
ChemicalEigenvalueMax                  0.2
!
ReductionMethod                        diagonalization 
!
AtomDistanceMin[bohr]                  1.3
RateOutput                             rate.out
