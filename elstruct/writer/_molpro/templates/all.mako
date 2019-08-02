## 0. machine options block
***,${comment}
memory,${memory_mw},m
%if machine_options:
${machine_options}
%endif
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
% if gen_lines != '':
${gen_lines}
% endif
## 2. theory block
basis=${basis}
%if scf_method:
{${scf_method},${scf_options}}
%endif
%if corr_method:
{${corr_method},${scf_options}}
%endif
%if job_key == 'optimization':
{optg,${job_options}}
status
%endif
%if job_key == 'energy':
status,all,crash
%endif
