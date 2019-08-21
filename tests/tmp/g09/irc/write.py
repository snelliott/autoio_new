""" irc readers
"""

import elstruct.writer


def test__irc_writer():
    """ writes an irc log file from Gaussian
        writes the information to files
    """
    basis = '6-31g'
    geom = (('O', (0.0, 0.0, -0.110)),
            ('H', (0.0, -1.635, 0.876)),
            ('H', (-0.0, 1.635, 0.876)))
    mult = 1
    charge = 0
    orb_restricted = True
    prog = 'g09'
    method = 'b3lyp'
    irc_direction = 'reverse'
    job_options = ('CALCALL', 'STEPSIZE=3', 'MAXPOINTS=10')

    irc_str = elstruct.writer.irc(
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
        corr_options=(),
        gen_lines=(),
        job_options=job_options,
        frozen_coordinates=(),
        irc_direction=irc_direction)

    print(irc_str)


if __name__ == '__main__':
    test__irc_writer()
