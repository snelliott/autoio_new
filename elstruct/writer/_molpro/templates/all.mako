## 0. machine options block
***,${comment}
memory,${memory_mw},m
${machine_options}

## 1. molecule block
${mol_options}
angstrom
geometry = {
${geom}
}
set,spin=${spin}
set,charge=${charge}
## 2. theory block
basis=${basis}
%if scf_method:
{${scf_method},${scf_options}}
%endif
%if corr_method:
{${corr_method},${scf_options}}
%endif
