def core_writer():
    """
    """
    keyword in input is FROZEN_CORE=ON which is the default (i.e. always put this in
    unless the all_electron option is given

def relativistic_energy():
    """ Read a relativistic energy
    """

    # 'relativistic' for MVD1
    methods = app.one_of_these(['DPT', 'MVD2', 'relativistic'])

    ptt = (
        'Total energy with' +
        app.SPACE +
        methods +
        app.SPACE +
        'correction:' +
        app.SPACES +
        app.capturing(app.FLOAT) +
        app.SPACES +
        'Hartree'
    )

    cap = apf.capture(ptt, output_str)
    val = float(cap) if cap is not None else None

    return val


def diagonal_born_oppenheimer_correction(output_str):
    """ DBOC
    """

    ptt = (
        'The total diagonal Born-Oppenheimer correction (DBOC) is:' +
        app.SPACES +
        app.capturing(app.FLOAT) +
        app.SPACES +
        'a.u.'
    )

    cap = apf.capture(ptt, output_str)
    val = float(cap) if cap is not None else None

    return val
