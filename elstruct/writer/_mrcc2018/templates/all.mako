## 0. comment block
# ${comment}
## 1. memory block
mem=${memory}GB
## 2. method block
calc=${method}
basis=${basis}
scftype=${reference}
## job options block
## scfiguess=sad
## ccmaxit=2
## scftol=7
## cctol=7
## x. molecule block
charge=${charge}
mult=${mult}
## x. job block
% if job_key == 'optimization':
gopt=full
% elif job_key == 'hessian':
freq=on
% endif

geom=${coord_sys}
${geom}
