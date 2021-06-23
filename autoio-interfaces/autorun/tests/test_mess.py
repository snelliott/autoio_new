""" tests projrot (maybe others)
"""

import os
import tempfile
import numpy
import automol
from ioformat import pathtools
import autorun


PATH = os.path.dirname(os.path.realpath(__file__))
DAT_PATH = os.path.join(PATH, 'data')

GEO = automol.geom.from_string(
    pathtools.read_file(DAT_PATH, 'c2h5oh.xyz'))
MESS_ROT_STR = pathtools.read_file(DAT_PATH, 'c2h5oh.mrot')

MESS_INP_STR = pathtools.read_file(DAT_PATH, 'mess_rate.inp')
MESS_AUX = {
    'mess_rotd1.dat': pathtools.read_file(DAT_PATH, 'mess_rotd1.dat'),
    'mess_rotd2.dat': pathtools.read_file(DAT_PATH, 'mess_rotd2.dat')
}


def test__torsion():
    """ test autorun.mess.torsions
        test autorun.mess.direct
    """

    ref_tors_freqs = (263.39, 320.923)
    ref_tors_zpves = (0.0005850015264154265, 0.0006727675639040085)

    with tempfile.TemporaryDirectory(dir=PATH) as run_dir:

        script_str = autorun.SCRIPT_DCT['messpf']

        tors_freqs, tors_zpves = autorun.mess.torsions(
            script_str, run_dir, GEO, MESS_ROT_STR)

        assert numpy.allclose(tors_freqs, ref_tors_freqs)
        assert numpy.allclose(tors_zpves, ref_tors_zpves)


def test__lump():
    """ test autorun.mess.well_lumped_input_file
    """

    # with tempfile.TemporaryDirectory(dir=PATH) as run_dir:
    run_dir = tempfile.mkdtemp()
    print(run_dir)
    script_str = autorun.SCRIPT_DCT['messrate']

    pressure = 1.01324  # not finding pressure/temp?
    temp = 600
    lump_str = autorun.mess.well_lumped_input_file(
        script_str, run_dir, pressure, temp, MESS_INP_STR,
        aux_dct=MESS_AUX)
    print('LUMP_STR')
    print(lump_str)


test__lump()
