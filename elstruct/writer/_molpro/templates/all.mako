## 0. machine options block
***,${comment}
memory,${memory_mw},m
%if machine_options:
${machine_options}
%endif
## 0b. general lines block
% if gen_lines != '':
${gen_lines}
% endif
## 1. molecule block
%if mol_options:
${mol_options}
%endif
angstrom
geometry = {
${geom}
}
% if zmat_vals != '':
${zmat_vals}
% endif
set,spin=${spin}
set,charge=${charge}
## 2. theory block
basis=${basis}
%if scf_method:
{${scf_method},${scf_options}}
%endif
%if ismultiref:
{casscf,${casscf_options}}
%endif
%if corr_method:
{${corr_method},${corr_options}}
%endif
%if job_key == 'optimization':
{optg,${job_options}}
status
%elif job_key == 'hessian':
{freq,${job_options}}
put,molden,freq.molden
status
%elif job_key == 'energy':
status,all,crash
%endif
