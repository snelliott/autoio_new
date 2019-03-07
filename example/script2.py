""" dev script
"""
import elstruct

# input arguments
SCRIPT_STR = "#!/usr/bin/env bash\npsi4 >> stdout.log &> stderr.log"
INPUT_WRITER = elstruct.writer.optimization
PROG = 'psi4'
METHOD = 'rhf'
BASIS = 'sto-3g'
GEOM = ((('O', (None, None, None), (None, None, None)),
         ('H', (0, None, None), ('R1', None, None)),
         ('H', (0, 1, None), ('R2', 'A2', None))),
        {'R1': 2.0, 'R2': 1.5, 'A2': 1.5})
MULT = 1
CHARGE = 0
KWARGS = {'comment': '<testing comment line>',
          'scf_options': ('set scf diis false', 'set scf maxiter 15'),
          'opt_options': ('set geom_maxiter 10',)}
ERRORS = [
    elstruct.ERROR.SCF_NOCONV,
    elstruct.ERROR.OPT_NOCONV,
]
OPTIONS_MATRIX = [
    [{elstruct.OPTION.SCF.KEY: ('set scf guess huckel',)},
     {elstruct.OPTION.SCF.KEY: ('set scf guess gwh',)},
     {elstruct.OPTION.SCF.KEY: ('set scf diis true', 'set scf guess sad',)}],
    [{elstruct.OPTION.OPT.KEY: ('set opt_coordinates cartesian',)},
     {elstruct.OPTION.OPT.KEY: ('set opt_coordinates internal',)}]
]


# how we call it
INP_STR, OUT_STR, RUN_DIR = elstruct.run.robust(
    SCRIPT_STR, INPUT_WRITER,
    PROG, METHOD, BASIS, GEOM, MULT, CHARGE,
    errors=ERRORS, options_mat=OPTIONS_MATRIX,
    **KWARGS
)

ENE = elstruct.reader.energy(PROG, METHOD, OUT_STR)
ZMA = elstruct.reader.opt_zmatrix(PROG, OUT_STR)

print(INP_STR)
print(ENE)
print(ZMA)
