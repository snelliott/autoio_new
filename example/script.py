""" dev script
"""
import elstruct

BASIS = 'sto-3g'
GEOM = ((('O', (None, None, None), (None, None, None)),
         ('H', (0, None, None), ('R1', None, None)),
         ('H', (0, 1, None), ('R2', 'A2', None))),
        {'R1': 2.0, 'R2': 1.5, 'A2': 1.5})
MULT = 1
CHARGE = 0
PROG = 'psi4'
METHOD = 'rhf'
SCRIPT_STR = "#!/usr/bin/env bash\npsi4 >> stdout.log &> stderr.log"

INP_STR = elstruct.writer.optimization(
    prog=PROG, method=METHOD, basis=BASIS, geom=GEOM,
    mult=MULT, charge=CHARGE, scf_options=(
        'set scf maxiter 100',
        'set scf guess sad',
    ),
    opt_options=(
        'set geom_maxiter 4',
        'set opt_coordinates internal',
    )
)

OUT_STR, TMP_DIR = elstruct.run(SCRIPT_STR, INP_STR, return_path=True)

print(elstruct.reader.has_normal_exit_message(PROG, OUT_STR))
print(elstruct.reader.has_scf_nonconvergence_message(PROG, OUT_STR))
print(TMP_DIR)
# ENE = elstruct.reader.energy(PROG, METHOD, OUT_STR)
# ZMA = elstruct.reader.optimized_zmatrix(PROG, OUT_STR)
# print(ENE)
# print(ZMA)
