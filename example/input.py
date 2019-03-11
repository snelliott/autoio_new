""" elstruct input
"""
import tempfile
import elstruct

PROG = 'psi4'
METHOD = 'rhf-mp2'
BASIS = 'sto-3g'
RUN_DIR = tempfile.mkdtemp()

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
    errors=[
        elstruct.ERROR.SCF_NOCONV,
        elstruct.ERROR.OPT_NOCONV,
    ],
    options_mat=[
        [{elstruct.OPTION.SCF.KEY: ('set scf guess huckel',)},
         {elstruct.OPTION.SCF.KEY: ('set scf guess gwh',)},
         {elstruct.OPTION.SCF.KEY: ('set scf diis true',
                                    'set scf guess sad',)}],
        [{elstruct.OPTION.OPT.KEY: ('set opt_coordinates cartesian',)},
         {elstruct.OPTION.OPT.KEY: ('set opt_coordinates internal',)}]
    ],
    # optional_arguments
    comment='<testing comment line>',
    scf_options=('set scf diis false', 'set scf maxiter 15'),
    opt_options=('set geom_maxiter 10',),
)

ENE = elstruct.reader.energy(PROG, METHOD, OUT_STR)
ZMA = elstruct.reader.opt_zmatrix(PROG, OUT_STR)

print(INP_STR)
print(RUN_DIR)
print(ENE)
print(ZMA)
