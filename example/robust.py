""" elstruct input
"""
import tempfile
import elstruct
from elstruct import option, Option

PROG = 'psi4'
METHOD = 'mp2'
ORB_RESTRICTED = True
BASIS = 'sto-3g'
RUN_DIR = tempfile.mkdtemp()
print(RUN_DIR)

INP_STR, OUT_STR = elstruct.run.robust(
    # required arguments
    script_str="#!/usr/bin/env bash\n"
               "psi4 -i run.inp -o run.out >> stdout.log &> stderr.log",
    run_dir=RUN_DIR,
    input_writer=elstruct.writer.optimization,
    prog=PROG,
    method=METHOD,
    basis=BASIS,
    geom=((('O', (None, None, None), (None, None, None)),
           ('H', (0, None, None), ('R1', None, None)),
           ('H', (0, 1, None), ('R2', 'A2', None))),
          {'R1': 2.0, 'R2': 1.5, 'A2': 1.5}),
    mult=1,
    charge=0,
    orb_restricted=ORB_RESTRICTED,
    errors=[
        elstruct.Error.SCF_NOCONV,
        elstruct.Error.OPT_NOCONV,
    ],
    options_mat=[
        [{'scf_options': (Option.Scf.Guess.CORE,)},
         {'scf_options': (Option.Scf.Guess.HUCKEL,)},
         {'scf_options': (option.specify(Option.Scf.DIIS_, True),
                          Option.Scf.Guess.HUCKEL,)}],
        [{'job_options': (Option.Opt.Coord.CARTESIAN,)},
         {'job_options': (Option.Opt.Coord.ZMATRIX,)},
         {'job_options': (Option.Opt.Coord.REDUNDANT,)}]
    ],
    # optional_arguments
    comment='<testing comment line>',
    scf_options=(option.specify(Option.Scf.DIIS_, False),
                 option.specify(Option.Scf.MAXITER_, 15),),
    job_options=(option.specify(Option.Opt.MAXITER_, 10),),
)

ENE = elstruct.reader.energy(PROG, METHOD, OUT_STR)
ZMA = elstruct.reader.opt_zmatrix(PROG, OUT_STR)

print(INP_STR)
print(ENE)
print(ZMA)
