""" irc readers
"""

import elstruct.writer


def test__mr_writer():
    """ writes an energy file for multiref method in molpro
        writes the information to files
    """
    basis = '6-31g'
    geom = (('O', (0.0, 0.0, -0.110)),
            ('H', (0.0, -1.635, 0.876)))
    mult = 2
    charge = 0
    orb_restricted = False
    prog = 'molpro2015'

    method = 'ccsdt(q)'

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


if __name__ == '__main__':
    test__mr_writer()
