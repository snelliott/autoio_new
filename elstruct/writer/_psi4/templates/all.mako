## 0. job/computation block
#! ${comment}
memory ${memory} GB
${machine_options}

##  1. molecule block
molecule {
${mol_options}
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
_, wfn = ${job_function}('scf', return_wfn=True, ${job_function_args})
% else:
_, wfn = ${job_function}('${corr_method}', return_wfn=True, ${job_function_args})
% endif

% if job_function == 'gradient':
grad = wfn.gradient()
grad.name = 'Gradient'
grad.print_out()
% endif

% if job_function == 'hessian':
grad = wfn.gradient()
grad.name = 'Gradient'
grad.print_out()
hess = wfn.hessian()
hess.name = 'Hessian'
hess.print_out()
% endif
