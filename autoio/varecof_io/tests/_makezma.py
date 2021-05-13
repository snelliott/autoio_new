""" make zmas
"""

import automol

rxn_smis_lst = [
    'C[CH2]',
    '[H]',
    '[OH]',
    '[CH3]',
    'CC',
    'CCO',
    'CCC'
]
for i, smi in enumerate(rxn_smis_lst):
    zma = automol.geom.zmatrix(
        automol.inchi.geometry(automol.smiles.inchi(smi)))
    print()
    print(smi)
    print(zma)
