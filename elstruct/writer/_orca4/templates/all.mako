## 0. comment block
# ${comment}
## 1. machine options block
% pal nprocs ${nprocs} end
% MaxCore ${memory} 
## 2. theoretical method block
% if reference:
! ${reference} ${method} ${basis}
% else:
! ${method} ${basis}
% endif
## 2. job options block (when we get to it)
% if job_key == 'optimization':
! Opt
% elif job_key == 'gradient':
! EnGrad
% elif job_key == 'hessian' and not num_hess:
! NumFreq
% elif job_key == 'hessian' and num_hess:
! NumFreq
% endif
## 3. molecule block
* ${coord_sys} ${charge} ${mult}
${geom}
*

