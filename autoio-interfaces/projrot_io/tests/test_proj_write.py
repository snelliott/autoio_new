"""
 tests writing of projrot inumpyut
"""
import os

from ioformat import read_text_file
import projrot_io


PATH = os.path.dirname(os.path.realpath(__file__))
GEO = (('C', (-4.0048955763, -0.3439866053, -0.0021431734)),
       ('O', (-1.3627056155, -0.3412713280, 0.0239463418)),
       ('H', (-4.7435343957, 1.4733340928, 0.7491098889)),
       ('H', (-4.7435373042, -1.9674678465, 1.1075144307)),
       ('H', (-4.6638955748, -0.5501793084, -1.9816675556)),
       ('H', (-0.8648060003, -0.1539639444, 1.8221471090)))
GRAD = ((-4.0048955763, -0.3439866053, -0.0021431734),
        (-1.3627056155, -0.3412713280, 0.0239463418),
        (-4.7435343957, 1.4733340928, 0.7491098889),
        (-4.7435373042, -1.9674678465, 1.1075144307),
        (-4.6638955748, -0.5501793084, -1.9816675556),
        (-0.8648060003, -0.1539639444, 1.8221471090))
HESS = ((0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        (0.0, 0.959, 0.0, 0.0, -0.452, 0.519, 0.0, -0.477, -0.23),
        (0.0, 0.0, 0.371, 0.0, 0.222, -0.555, 0.0, -0.279, -0.128),
        (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        (0.0, -0.479, 0.279, 0.0, 0.455, -0.256, 0.0, -0.017, 0.051),
        (0.0, 0.251, -0.185, 0.0, -0.247, 0.607, 0.0, -0.012, 0.09),
        (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        (0.0, -0.479, -0.279, 0.0, -0.003, -0.263, 0.0, 0.494, 0.279),
        (0.0, -0.251, -0.185, 0.0, 0.025, 0.947, 0.0, 0.292, 0.137))
GEOS = [GEO for i in range(21)]
GRADS = [GRAD for i in range(21)]
HESSES = [HESS for i in range(21)]
AXIS1 = [2, 3]
GROUP1 = [0, 1]
AXIS2 = [4, 5]
GROUP2 = [6, 7, 8, 9, 10, 11]

CART_PROJ = 'cartesian'

# Set info for coord_en
RXN_PATH_COORDS = [
    0.30596, 0.27536, 0.24477, 0.21417, 0.18358,
    0.15298, 0.12238, 0.09179, 0.06119, 0.03060,
    0.00000,
    -0.03060, -0.06119, -0.09178, -0.12237, -0.15296,
    -0.18354, -0.21412, -0.24471, -0.27530, -0.30589]
RXN_PATH_ENERGIES = [
    -0.0046300, 0.0038600, 0.0031100, 0.0024100, 0.0017800,
    -0.0012300, 0.0007800, 0.0004300, 0.0001900, 0.0000400,
    0.0000000,
    -0.0000400, -0.0001500, -0.0003300, -0.0005400, -0.0007800,
    -0.0010300, -0.0013000, -0.0015600, -0.0018300, -0.0020900]
RCT_DISTS = [
    1.31974, 1.30370, 1.28780, 1.27204, 1.25643,
    1.24095, 1.22561, 1.21045, 1.19547, 1.18071,
    1.16640,
    1.15214, 1.13850, 1.12545, 1.11313, 1.10176,
    1.09156, 1.08265, 1.07505, 1.06868, 1.06336]
PRD_DISTS = [
    1.08945, 1.10474, 1.12025, 1.13593, 1.15176,
    1.16770, 1.18375, 1.19987, 1.21609, 1.23238,
    1.24880,
    1.26522, 1.28171, 1.29821, 1.31466, 1.33097,
    1.34701, 1.36265, 1.37782, 1.39250, 1.40671]


def test_rt_projections():
    """ test projrot_io.writer.rpht_input
    """

    inp_str = projrot_io.writer.rpht_input(
        [GEO], [GRAD], [HESS],
        saddle_idx=1,
        rotors_str='',
        coord_proj=CART_PROJ,
        proj_rxn_coord=False)
    assert inp_str == read_text_file(['data'], 'rpht.inp', PATH)


def test_rt_hr_projections():
    """ test projrot_io.writer.rotors_str
        test projrot_io.writer.rpht_inumpyut
    """

    rotors_str = (
        projrot_io.writer.rotors(AXIS1, GROUP1) +
        '\n' +
        projrot_io.writer.rotors(AXIS2, GROUP2)
    )

    inp_str = projrot_io.writer.rpht_input(
        [GEO], [GRAD], [HESS],
        saddle_idx=1,
        rotors_str=rotors_str,
        coord_proj=CART_PROJ,
        proj_rxn_coord=False)
    assert inp_str == read_text_file(['data'], 'rpht_hr.inp', PATH).rstrip()


def test__rotor_dist_cutoffs():
    """ test projrot_io.writer.projection_distance_aux
    """

    dist_cutoff_dct = {
        ('H', 'O'): 2.26767,
        ('H', 'C'): 2.26767
    }

    rotor_dist1_str = projrot_io.writer.projection_distance_aux()
    rotor_dist2_str = projrot_io.writer.projection_distance_aux(
        dist_cutoff_dct=dist_cutoff_dct)

    assert rotor_dist1_str == read_text_file(['data'], 'rotor_dist1.inp', PATH)
    assert rotor_dist2_str == read_text_file(['data'], 'rotor_dist2.inp', PATH)


def test_sct_rpht_input():
    """ test projrot_io.writer.rpht_input
        test projrot_io.writer.rpht_path_coord_en
    """

    inp_str = projrot_io.writer.rpht_input(
        GEOS, GRADS, HESSES,
        saddle_idx=11,
        rotors_str='',
        coord_proj=CART_PROJ,
        proj_rxn_coord=True)
    assert inp_str == read_text_file(['data'], 'rpht_sct.inp', PATH)


def test_sct_coord_en():
    """ test projrot_io.writer.rpht_path_coord_en
    """

    en1_str = projrot_io.writer.rpht_path_coord_en(
        RXN_PATH_COORDS, RXN_PATH_ENERGIES,
        bnd1=(), bnd2=())
    assert en1_str == read_text_file(['data'], 'rpht_en1.inp', PATH)

    en2_str = projrot_io.writer.rpht_path_coord_en(
        RXN_PATH_COORDS, RXN_PATH_ENERGIES,
        bnd1=RCT_DISTS, bnd2=PRD_DISTS)
    assert en2_str == read_text_file(['data'], 'rpht_en2.inp', PATH)


if __name__ == '__main__':
    test_rt_projections()
    test_rt_hr_projections()
    test__rotor_dist_cutoffs()
    test_sct_rpht_input()
    test_sct_coord_en()
