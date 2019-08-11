## 0. comment block
${comment}
## 1. molecule block
${geom}

% if zmat_var_vals != '':
${zmat_var_vals}
% endif
## 2. job options block
*CFOUR(${job_options}
## n. theoretical method block
CALC_LEVEL=${method}
REFERENCE=${reference}
BASIS=${basis}
## n. scf options block
if scf_options != '':
${scf_options}
## n. corr options block
if corr_options != '':
${corr_options}
## n. molecule block
CHARGE=${charge}
MULTIPLICITY=${mult}
## n. coord sys block
COORDS=${coord_type}
UNITS=ANGSTROM
## n. machine options block
MEMORY_SIZE=${memory}
MEM_UNIT=GB)
## n gen lines

% if gen_lines != '':
${gen_lines}
% endif
