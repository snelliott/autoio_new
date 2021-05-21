$comment
${comment}
$end

$molecule
${charge} ${mult}
${geom}

% if zmat_var_vals != '':
${zmat_var_vals}
% endif
$end

% if zmat_const_vals != '':
$opt
CONSTRAINT
${zmat_const_vals}
ENDCONSTRAINT
$end

$rem
    JOBTYPE        ${job_key}
    ${method_str}
    UNRESTRICTED   ${unrestricted}
    BASIS          ${basis}
    XC_GRID        ${dft_options}
    GUESS(CHK)     ${scf_guess_options}
    MEM_TOTAL      ${memory_mb}
$end
