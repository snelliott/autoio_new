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
GEOM = (('O', (0.0, 0.0, -0.110)),
        ('H', (0.0, -1.635, 0.876)),
        ('H', (-0.0, 1.635, 0.876)))
RUN_DIR = tempfile.mkdtemp()
print(RUN_DIR)

INP_STR, OUT_STR = elstruct.run.direct(
    # required arguments
    input_writer=elstruct.writer.optimization,
    script_str=SCRIPT_STR,
    run_dir=RUN_DIR,
    geom=GEOM,
    charge=1,
    mult=2,
    method=METHOD,
    basis=BASIS,
    prog=PROG,
)

ENE = elstruct.reader.energy(PROG, METHOD, OUT_STR)

print(INP_STR)
with open('output.dat', 'w') as out_obj:
    out_obj.write(OUT_STR)

print(ENE)
