RRHO
## Core Section
${core}
## Frequencies Section
% if nfreqs > 0:
  Frequencies[1/cm]         ${nfreqs}
${freqs}
% endif
## Electronic Levels Section
  ElectronicLevels[1/cm]    ${nlevels}
${levels}
## Hindered Rotor Section
% if hind_rot != '':
${hind_rot}\
% endif 
## Anharmonicity Section
% if anharm != '':
  Anharmonicities[1/cm]
${anharm}
% endif 
## Infrared Intensities
% if nintens > 0:
  InfraredIntensities[km/mol]  ${nintens}
${intens}
% endif
## Rovibrational Coupling Section
% if rovib_coups != '':
  RovibrationalCouplings[1/cm]
${rovib_coups}
% endif
## Rotational Distortion Section
% if rot_dists != '':
  RotationalDistortion[1/cm]
${rot_dists}
% endif
## Various Keywords
% if freq_scale_factor is not None:
  FrequencyScalingFactor    ${freq_scale_factor} 
% endif
% if use_harmfreqs_key: 
  AreFrequenciesHarmonic
% endif
