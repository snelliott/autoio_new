## 0. machine options block
%%mem=${memory}GB
${machine_options}
## 1. theoretical method block
#N ${scf_method}/${basis}
# SCF=(xqc,${scf_options})
## 2. job options block (when we get to it)
% if job_key == 'optimization' and opt_options != '':
# Opt=(${opt_options})
% elif job_key == 'optimization':
# Opt
% elif job_key == 'gradient':
# Force
% elif job_key == 'hessian':
# Freq
% endif
## 3. molecule block
% if mol_options != '':
# ${mol_options}
% endif

comment: ${comment}

${charge} ${mult}
${geom}
% if zmat_var_vals != '':
    Variables:
${zmat_var_vals}
% endif
% if zmat_const_vals != '':
    Constants:
${zmat_const_vals}
% endif

