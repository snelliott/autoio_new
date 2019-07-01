""" elstruct direct run
"""
import tempfile
import elstruct
import automol

# PROG = 'psi4'
# SCRIPT_STR = ("#!/usr/bin/env bash\n"
#               "psi4 -i run.inp -o run.out")

PROG = 'g09'
SCRIPT_STR = ("#!/usr/bin/env bash\n"
              "g09 run.inp run.out >> stdout.log &> stderr.log")

METHOD = 'hf'
BASIS = '6-31g'
GEO = automol.geom.from_xyz_string(open('geom.xyz').read())
# ZMA = automol.geom.zmatrix(GEO)

# 1. optimization
RUN_DIR = tempfile.mkdtemp()
print('optimization:')
print(RUN_DIR)

INP_STR, OUT_STR = elstruct.run.direct(
    input_writer=elstruct.writer.optimization,
    script_str=SCRIPT_STR,
    run_dir=RUN_DIR,
    geom=GEO,
    charge=0,
    mult=2,
    method=METHOD,
    basis=BASIS,
    prog=PROG,
    saddle=True
)

OPT_GEO = elstruct.reader.opt_geometry(PROG, OUT_STR)
ROT_CONS = elstruct.util.rotational_constants(OPT_GEO)
print(ROT_CONS)


# 2. gradient
RUN_DIR = tempfile.mkdtemp()
print('gradient:')
print(RUN_DIR)

INP_STR, OUT_STR = elstruct.run.direct(
    # required arguments
    input_writer=elstruct.writer.gradient,
    script_str=SCRIPT_STR,
    run_dir=RUN_DIR,
    geom=OPT_GEO,
    charge=0,
    mult=2,
    method=METHOD,
    basis=BASIS,
    prog=PROG,
)

GRAD = elstruct.reader.gradient(PROG, OUT_STR)
print(GRAD)


# 3. frequencies
RUN_DIR = tempfile.mkdtemp()
print('hessian:')
print(RUN_DIR)

INP_STR, OUT_STR = elstruct.run.direct(
    # required arguments
    input_writer=elstruct.writer.hessian,
    script_str=SCRIPT_STR,
    run_dir=RUN_DIR,
    geom=OPT_GEO,
    charge=0,
    mult=2,
    method=METHOD,
    basis=BASIS,
    prog=PROG,
)

HESS = elstruct.reader.hessian(PROG, OUT_STR)
FREQ = elstruct.util.harmonic_frequencies(OPT_GEO, HESS)
print('frequencies:')
print(FREQ)
