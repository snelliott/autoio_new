""" dev script
"""
import itertools
import elstruct


def has_kwargs(kwarg_mat):
    """ does this kwarg matrix have kwargs left?
    """
    assert all(kwarg_row for kwarg_row in kwarg_mat)
    return kwarg_mat


def current_kwargs(kwarg_mat):
    """ get the current kwargs from the kwarg matrix
    """
    assert has_kwargs(kwarg_mat)

    # grap the first item in eatch row
    kwarg_dcts = [kwarg_row[0] for kwarg_row in kwarg_mat]

    # make sure there are no conflicting keywords
    all_keys = list(itertools.chain(*map(list, kwarg_dcts)))
    assert len(all_keys) == len(set(all_keys))

    # form the dictionary
    ret_kwarg_dct = {}
    for kwarg_dct in kwarg_dcts:
        ret_kwarg_dct.update(kwarg_dct)

    return ret_kwarg_dct


def advance_kwarg_matrix(row_idx, kwarg_mat):
    """ advance a row of the kwarg matrix
    """
    assert has_kwargs(kwarg_mat)

    kwarg_mat = list(map(list, kwarg_mat))
    kwarg_mat[row_idx].pop(0)
    assert kwarg_mat[row_idx]
    return tuple(map(tuple, kwarg_mat))


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

KWARG_MAT = [
    [{'scf_options': ('set scf diis false',
                      'set scf maxiter 18',
                      'set scf guess huckel',)},
     {'scf_options': ('set scf diis false',
                      'set scf maxiter 18',
                      'set scf guess gwh',)},
     {'scf_options': ('set scf diis true',
                      'set scf maxiter 18',
                      'set scf guess sad',)}],
    [{'opt_options': ('set geom_maxiter 10',
                      'set opt_coordinates cartesian',)},
     {'opt_options': ('set geom_maxiter 10',
                      'set opt_coordinates internal',)}]
]

ERROR_READERS = [
    elstruct.reader.has_scf_nonconvergence_message,
    elstruct.reader.has_opt_nonconvergence_message,
]


for _ in range(10):
    KWARGS = current_kwargs(KWARG_MAT)
    print(KWARGS)

    INP_STR = elstruct.writer.optimization(
        prog=PROG, method=METHOD, basis=BASIS, geom=GEOM,
        mult=MULT, charge=CHARGE, **KWARGS,
    )
    OUT_STR, TMP_DIR = elstruct.run(SCRIPT_STR, INP_STR, return_path=True)

    ERRORS = [ERROR_READER(PROG, OUT_STR) for ERROR_READER in ERROR_READERS]

    if not any(ERRORS):
        break

    ROW_IDX = ERRORS.index(True)

    KWARG_MAT = advance_kwarg_matrix(ROW_IDX, KWARG_MAT)

    print(elstruct.reader.has_normal_exit_message(PROG, OUT_STR))
    print(elstruct.reader.has_scf_nonconvergence_message(PROG, OUT_STR))
    print(elstruct.reader.has_opt_nonconvergence_message(PROG, OUT_STR))
    print(TMP_DIR)
    print()

ENE = elstruct.reader.energy(PROG, METHOD, OUT_STR)
ZMA = elstruct.reader.opt_zmatrix(PROG, OUT_STR)
print(ENE)
print(ZMA)
