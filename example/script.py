""" dev script

kwargs needs to be renamed, because this is really specific to the _options
arguments
"""
import itertools
import elstruct


def _extend_kwargs(kwarg_dct1, kwarg_dct2):
    kwarg_dct = dict(kwarg_dct1).copy()

    for key, val in kwarg_dct2.items():
        kwarg_dct[key] = kwarg_dct[key] + val if key in kwarg_dct else val

    return kwarg_dct


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

BASE_KWARGS = {'scf_options': ('set scf diis false', 'set scf maxiter 15'),
               'opt_options': ('set geom_maxiter 10',)}

KWARG_MAT = [
    [{'scf_options': ('set scf guess huckel',)},
     {'scf_options': ('set scf guess gwh',)},
     {'scf_options': ('set scf diis true', 'set scf guess sad',)}],
    [{'opt_options': ('set opt_coordinates cartesian',)},
     {'opt_options': ('set opt_coordinates internal',)}]
]

ERRORS = [
    elstruct.ERROR.SCF_NOCONV,
    elstruct.ERROR.OPT_NOCONV,
]


for _ in range(10):
    KWARGS = _extend_kwargs(BASE_KWARGS, current_kwargs(KWARG_MAT))
    print(KWARGS)

    INP_STR, OUT_STR, TMP_DIR = elstruct.run.direct(
        SCRIPT_STR, elstruct.writer.optimization,
        prog=PROG, method=METHOD, basis=BASIS, geom=GEOM,
        mult=MULT, charge=CHARGE, **KWARGS,
    )

    HAS_ERROR_LST = [
        elstruct.reader.has_error_message(PROG, ERROR, OUT_STR)
        for ERROR in ERRORS]

    if not any(HAS_ERROR_LST):
        break

    ROW_IDX = HAS_ERROR_LST.index(True)

    KWARG_MAT = advance_kwarg_matrix(ROW_IDX, KWARG_MAT)

    print(elstruct.reader.has_normal_exit_message(PROG, OUT_STR))
    print(TMP_DIR)
    print()

ENE = elstruct.reader.energy(PROG, METHOD, OUT_STR)
ZMA = elstruct.reader.opt_zmatrix(PROG, OUT_STR)
print(ENE)
print(ZMA)
