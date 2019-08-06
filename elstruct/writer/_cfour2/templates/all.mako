## 0. comment block
${comment}
## 1. molecule block
${geom}

% if zmat_var_vals != '':
${zmat_var_vals}
% endif
## 2. job options block
% if job_key == 'energy':
*CFOUR(${job_options}
## n. theoretical method block
CALC_LEVEL=${method}
REFERENCE=${reference}
BASIS=${basis}
## n. molecule block
CHARGE=${charge}
MULTIPLICITY=${mult}
## n. coord sys block
COORDS=${coord_type}
UNITS=${units}
## n. machine options block
MEMORY_SIZE=${memory}
MEM_UNIT=GB)

