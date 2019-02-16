## 0. job/computation block
#! ${comment}
memory ${memory} GB
${machine_options}

##  1. molecule block
molecule {
${charge} ${mult}
${geom}
% if zmat_vals != '':
${zmat_vals}
% endif
}

##  2. theoretical method block
set basis ${basis}
set scf_type pk
set reference ${scf_method}
set mp2_type conv

${scf_options}
${corr_options}
% if job_function == 'optimize':
${opt_options}
% endif

% if corr_method == '':
${job_function}('scf')
% else:
${job_function}('${corr_method}')
% endif
