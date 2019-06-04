""" elstruct direct run
"""
import tempfile
import elstruct

PROG = 'psi4'
SCRIPT_STR = ("#!/usr/bin/env bash\n"
              "psi4 -i run.inp -o run.out")

# PROG = 'g09'
# SCRIPT_STR = ("#!/usr/bin/env bash\n"
#               "g09 run.inp run.out >> stdout.log &> stderr.log")

METHOD = 'dft:b3lyp'
BASIS = 'basis:sto-3g'
GEO = (('O', (0.0, 0.0, -0.110)),
       ('H', (0.0, -1.635, 0.876)),
       ('H', (-0.0, 1.635, 0.876)))
RUN_DIR = tempfile.mkdtemp()
print(RUN_DIR)


# 1. optimization
INP_STR, OUT_STR = elstruct.run.direct(
    # required arguments
    input_writer=elstruct.writer.optimization,
    script_str=SCRIPT_STR,
    run_dir=RUN_DIR,
    geom=GEO,
    charge=1,
    mult=2,
    method=METHOD,
    basis=BASIS,
    prog=PROG,
)

OPT_GEO = elstruct.reader.opt_geometry(PROG, OUT_STR)
ROT_CONS = elstruct.util.rotational_constants(OPT_GEO)
print(ROT_CONS)


# 2. frequencies
INP_STR, OUT_STR = elstruct.run.direct(
    # required arguments
    input_writer=elstruct.writer.hessian,
    script_str=SCRIPT_STR,
    run_dir=RUN_DIR,
    geom=OPT_GEO,
    charge=1,
    mult=2,
    method=METHOD,
    basis=BASIS,
    prog=PROG,
)

HESS = elstruct.reader.hessian(PROG, OUT_STR)
FREQ = elstruct.util.real_harmonic_frequencies(OPT_GEO, HESS)
IM_FREQ = elstruct.util.imaginary_harmonic_frequencies(OPT_GEO, HESS)
print(FREQ)
print(IM_FREQ)
