import automol
import numpy

zma1 = (
    (('C', (None, None, None), (None, None, None)),
     ('O', (0, None, None), ('R1', None, None)),
     ('H', (0, 1, None), ('R2', 'A2', None)),
     ('H', (0, 1, 2), ('R3', 'A3', 'D3')),
     ('X', (3, 0, 1), ('JR4', 'JA4', 'JD4')),
     ('N', (3, 4, 0), ('JR5', 'JA5', 'JD5')),
     ('O', (5, 3, 4), ('R6', 'JA6', 'JD6')),
     ('O', (5, 6, 3), ('R7', 'A7', 'JD7'))),
    {'R1': 2.31422,
     'R2': 2.08191, 'A2': 2.13342,
     'R3': 2.08191, 'A3': 2.13342, 'D3': 3.14159,
     'JR4': 3.78, 'JA4': 1.57, 'JD4': 3.14,
     'JR5': 2.38, 'JA5': 1.53, 'JD5': 3.32,
     'R6': 2.69082, 'JA6': 1.83, 'JD6': 1.39,
     'R7': 2.69082, 'A7': 1.89019, 'JD7': 0.0})


def build_remdummy_shift_lst(zma):
    """ Assess the zma for dummys and build a list to shift values
        derived from zma
    """

    atom_symbols = automol.zmatrix.symbols(zma)
    dummy_idx = []
    for atm_idx, atm in enumerate(atom_symbols):
        if atm == 'X':
            dummy_idx.append(atm_idx)
    remdummy = numpy.zeros(len(zma[0]))
    for dummy in dummy_idx:
        for idx, _ in enumerate(remdummy):
            if dummy < idx:
                remdummy[idx] += 1

    return remdummy

print(build_remdummy_shift_lst(zma1))

