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
    mult = 1
    charge = 0
    orb_restricted = True
    prog = 'molpro'

    method = 'casscf'
    casscf_options = [
        elstruct.option.specify(elstruct.Option.Scf.MAXITER_, 40),
        elstruct.option.specify(elstruct.Option.Casscf.OCC_, 12),
        elstruct.option.specify(elstruct.Option.Casscf.CLOSED_, 10),
        elstruct.option.specify(elstruct.Option.Casscf.WFN_, 14, 1, 2, 0),
    ]

    guess_str = elstruct.writer.energy(
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
        casscf_options=casscf_options,
        corr_options=(),
        gen_lines=())
    guess_str += '\n\n'
    guess_lines = guess_str.splitlines()[2:]

    method = 'caspt2c'
    casscf_options = [
        elstruct.option.specify(elstruct.Option.Scf.MAXITER_, 40),
        elstruct.option.specify(elstruct.Option.Casscf.OCC_, 14),
        elstruct.option.specify(elstruct.Option.Casscf.CLOSED_, 8),
        elstruct.option.specify(elstruct.Option.Casscf.WFN_, 14, 1, 2, 0),
    ]
    corr_options = [
        elstruct.option.specify(elstruct.Option.MRCorr.SHIFT_, 0.25),
    ]

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
        casscf_options=casscf_options,
        corr_options=corr_options,
        gen_lines=guess_lines)

    print(ene_str)


if __name__ == '__main__':
    test__mr_writer()
