""" elstruct input
"""
import tempfile
import automol
import elstruct
# from elstruct import option, Option

PROG = 'g09'
SCRIPT_STR = ("#!/usr/bin/env bash\n"
              "g09 run.inp run.out")
METHOD = 'b3lyp'
ORB_RESTRICTED = True
BASIS = 'sto-3g'
GEOM = ((('O', (None, None, None), (None, None, None)),
         ('H', (0, None, None), ('R1', None, None)),
         ('H', (0, 1, None), ('R2', 'A2', None))),
        {'R1': 2.0, 'R2': 1.5, 'A2': 1.5})
GEOM = automol.zmatrix.geometry(GEOM)
RUN_DIR = tempfile.mkdtemp()
print(RUN_DIR)
print(GEOM)

INP_STR, OUT_STR = elstruct.run.direct(
    # required arguments
    script_str=SCRIPT_STR,
    run_dir=RUN_DIR,
    input_writer=elstruct.writer.hessian,
    prog=PROG,
    method=METHOD,
    basis=BASIS,
    geom=GEOM,
    mult=1,
    charge=0,
    orb_restricted=ORB_RESTRICTED,
)

ENE = elstruct.reader.energy(PROG, METHOD, OUT_STR)
# ZMA = elstruct.reader.opt_zmatrix(PROG, OUT_STR)

print(INP_STR)
with open('output.dat', 'w') as out_obj:
    out_obj.write(OUT_STR)
print(ENE)
# print(ZMA)
