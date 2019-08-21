""" irc readers
"""

import elstruct.writer


def test__mr_writer():
    """ writes an energy file for multiref method in molpro
        writes the information to files
    """
    basis = '6-31g'
    geom = (('O', (0.0, 0.0, -0.110)),
            ('H', (0.0, -1.635, 0.876)),
            ('H', (-0.0, 1.635, 0.876)))
    geom_int = (
    (('H', (None, None, None), (None, None, None)),
     ('O', (0, None, None), ('R1', None, None)),
     ('C', (1, 0, None), ('R2', 'A2', None)),
     ('H', (2, 1, 0), ('R3', 'A3', 'D3')),
     ('H', (2, 1, 0), ('R3', 'A3', 'D4')),
     ('H', (2, 1, 0), ('R3', 'A3', 'D5'))),
    {'R1': 1.70075351,
     'R2': 2.64561657, 'A2': 1.74532925,
     'R3': 2.07869873, 'A3': 1.83259571,
     'D3': 1.04719755, 'D4': -1.04719755, 'D5': 3.1415926})
    mult = 1
    charge = 0
    orb_restricted = True
    prog = 'cfour2'
    method = 'ccsd(t)'

    ene_str = elstruct.writer.energy(
        geom,
        charge,
        mult,
        method,
        basis,
        prog,
        mol_options=(),
        memory=1,
        comment='',
        machine_options=(),
        orb_restricted=orb_restricted,
        scf_options=(),
        casscf_options=(),
        corr_options=(),
        gen_lines=())
    print(ene_str)

    ene_str = elstruct.writer.gradient(
        geom,
        charge,
        mult,
        method,
        basis,
        prog,
        mol_options=(),
        memory=1,
        comment='',
        machine_options=(),
        orb_restricted=orb_restricted,
        scf_options=(),
        casscf_options=(),
        corr_options=(),
        gen_lines=())
    print(ene_str)

    ene_str = elstruct.writer.hessian(
        geom_int,
        charge,
        mult,
        method,
        basis,
        prog,
        mol_options=(),
        memory=1,
        comment='',
        machine_options=(),
        orb_restricted=orb_restricted,
        scf_options=(),
        casscf_options=(),
        corr_options=(),
        gen_lines=())
    print(ene_str)

    ene_str = elstruct.writer.optimization(
        geom_int,
        charge,
        mult,
        method,
        basis,
        prog,
        mol_options=(),
        memory=1,
        comment='',
        machine_options=(),
        orb_restricted=orb_restricted,
        scf_options=(),
        casscf_options=(),
        corr_options=(),
        gen_lines=())
    print(ene_str)

    ene_str = elstruct.writer.optimization(
        geom_int,
        charge,
        mult,
        method,
        basis,
        prog,
        mol_options=(),
        memory=1,
        comment='',
        machine_options=(),
        orb_restricted=orb_restricted,
        scf_options=(),
        casscf_options=(),
        corr_options=(),
        gen_lines=(),
        saddle=True,
        frozen_coordinates=('R3', 'D3',),)
    print(ene_str)

if __name__ == '__main__':
    test__mr_writer()
