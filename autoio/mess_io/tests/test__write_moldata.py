""" Tests the writing of the energy transfer section
"""

import mess_io.writer
from _util import read_text_file

# Core Data
GEO1 = (
    ('C', (-1.4283035320563338, 0.013425343735546437, -0.030302158896694683)),
    ('C', (1.4283027358735494, -0.013425597530894248, 0.0303022919384165)),
    ('H', (-2.1972722614281355, -0.19229727219177065, 1.8778380427620682)),
    ('H', (-2.121310184939721, 1.792702413487708, -0.8231106338374065)),
    ('H', (-2.1448124562913287, -1.5396513482615042, -1.191852168914227)),
    ('H', (2.1448121742707795, 1.539654946791746, 1.1918517388178247)),
    ('H', (2.1972712765396953, 0.1922944277301287, -1.8778395029874426)),
    ('H', (2.121312248031497, -1.7927029137609576, 0.8231123911174519)))
GEO2 = (
    ('O', (-2.4257421043, 6.0797867203, 0.0000000000)),
    ('H', (-0.8184039622, 5.1215269111, 0.0000000000)))
SYM_FACTOR1 = 3.0
SYM_FACTOR2 = 1.0
INTERP_EMAX = 1500
POT_SURF_FILE = 'pot_surf.dat'
FLUX_FILE = 'flux.dat'
STOICH = 'C2O1H7'
POT_PREFACTOR = 12.0
POT_EXP = 4.0
TSTLVL = 'ej'

# Rotor Data
HR_GROUP = (6, 7, 8, 9, 10, 11)
HR_AXIS = (1, 2, 3)
HR_SYMMETRY = 1.0
HR_ID = 'D5'
UMBR_GROUP = (4, 5, 6)
UMBR_PLANE = (4, 5, 6)
UMBR_REF = 4
POTENTIAL = (0.00, 2.91, 9.06, 12.63, 9.97, 3.51,
             0.03, 3.49, 9.96, 12.63, 9.08, 2.93)

# Tunnel Data
IMAG_FREQ = 2000.0
WELL_DEPTH1 = 10.0
WELL_DEPTH2 = 20.0
CUTOFF_ENE = 3000.0
TUNNEL_FILE = 'tunnel.dat'



def test__core_rigidrotor_writer():
    """ core test
    """

    core_rigrot1_str = mess_io.writer.mol_data.core_rigidrotor(
        GEO1, SYM_FACTOR1)

    core_rigrot2_str = mess_io.writer.mol_data.core_rigidrotor(
        GEO1, SYM_FACTOR1,
        interp_emax=INTERP_EMAX)


def test__core_multirotor_writer():
    """ core test
    """

    # Set the base values needed for each of the core sections
    sym_factor = 1.000
    geom = (('O', (1.911401284, 0.16134481659, -0.05448080419)),
            ('N', (4.435924209, 0.16134481659, -0.05448080419)),
            ('N', (6.537299661, 0.16134481659, -0.05448080419)))
    pot_surf_file = 'surf.dat'

    # Write a string for the internal rotor
    group = [11, 10, 9, 8, 7, 6]
    axis = [3, 2, 1]
    symmetry = 1
    rotor_int_str = mess_io.writer.mol_data.rotor_internal(
        group=group,
        axis=axis,
        symmetry=symmetry,
        rotor_id='CH3',
        mass_exp_size=5, pot_exp_size=5,
        hmin=13, hmax=101,
        grid_size=100)

    # Use the writer to create a string for each of the core sections
    core_multirotor_str = mess_io.writer.mol_data.core_multirotor(
        geom=geom,
        sym_factor=sym_factor,
        pot_surf_file=pot_surf_file,
        int_rot_str=rotor_int_str,
        interp_emax=100,
        quant_lvl_emax=9)

    # Print the core string
    print(core_multirotor_str)


def test__core_phasespace_writer():
    """ core test
    """

    # Use the writer to create a string for each of the core sections
    core_phasespace1_str = mess_io.writer.mol_data.core_phasespace(
        GEO1, GEO2, SYM_FACTOR2, STOICH)

    core_phasespace2_str = mess_io.writer.mol_data.core_phasespace(
        GEO1, GEO2, SYM_FACTOR2, STOICH,
        pot_prefactor=POT_PREFACTOR,
        pot_exp=POT_EXP,
        tstlvl=TSTLVL)


def test__core_rotd_writer():
    """ core test
    """

    core_rotd_str = mess_io.writer.mol_data.core_rotd(
        SYM_FACTOR1, FLUX_FILE, STOICH)


def test__rotor_hindered_writer():
    """ hr test
    """

    rot_hind1_str = mess_io.writer.mol_data.rotor_hindered(
        HR_GROUP, HR_AXIS, HR_SYMMETRY, POTENTIAL,
        remdummy=None,
        geom=None,
        use_quantum_weight=False)
    
    rot_hind2_str = mess_io.writer.mol_data.rotor_hindered(
        HR_GROUP, HR_AXIS, HR_SYMMETRY, POTENTIAL,
        remdummy=None,
        geom=None,
        use_quantum_weight=False)


    # Need tests for other keywords being on

    # Print the hindered rotor section string
    print(rot_hind_str)


def test__rotor_internal_writer():
    """ hr test
    """

    # Set the keywords internal rotor section
    group = [11, 10, 9, 8, 7, 6]
    axis = [3, 2, 1]
    symmetry = 1

    # Use the writer to create a string for the molecule section
    rotor_int_str = mess_io.writer.mol_data.rotor_internal(
        group=group,
        axis=axis,
        symmetry=symmetry,
        rotor_id='CH3',
        mass_exp_size=5, pot_exp_size=5,
        hmin=13, hmax=101,
        grid_size=100)

    # Print the internal rotor string
    print(rotor_int_str)


def test__umbrella_writer():
    """ umbrella test
    """

    # Use the writer to create a string for the molecule section
    umbrella1_str = mess_io.writer.mol_data.umbrella_mode(
        group=UMBR_GROUP,
        plane=UMBR_PLANE,
        ref_atom=UMBR_REF,
        potential=POTENTIAL,
        remdummy=None,
        geom=None)
    umbrella2_str = mess_io.writer.mol_data.umbrella_mode(
        group=UMBR_GROUP,
        plane=UMBR_PLANE,
        ref_atom=UMBR_REF,
        potential=POTENTIAL,
        remdummy=None,
        geo=GEO1)

    # Need tests for other keywords being on

    # Print the hindered rotor section string
    print(umbrella_str)


def test__tunnel_eckart_writer():
    """ tunnel test
    """

    tunnel_eckart_str = mess_io.writer.mol_data.tunnel_eckart(
        IMAG_FREQ, WELL_DEPTH1, WELL_DEPTH2)

    with open('tunnel_eckart.inp', 'w') as f:
        f.write(tunnel_eckart_str)


def test__tunnel_sct_writer():
    """ tunnel test
    """

    # Use the writer to create a string for each of the tunnel sections
    tunnel_sct1_str = mess_io.writer.mol_data.tunnel_sct(
        IMAG_FREQ, TUNNEL_FILE)
    tunnel_sct2_str = mess_io.writer.mol_data.tunnel_sct(
        IMAG_FREQ, TUNNEL_FILE, cutoff_energy=CUTOFF_ENERGY)

    with open('tunnel_sct1.inp', 'w') as f:
        f.write(tunnel_sct1_str)
    with open('tunnel_sct2.inp', 'w') as f:
        f.write(tunnel_sct2_str)


if __name__ == '__main__':
    test__core_rigidrotor_writer()
    test__core_multirotor_writer()
    test__core_phasespace_writer()
    test__core_rotd_writer()
    test__rotor_hindered_writer()
    test__rotor_internal_writer()
    test__umbrella_writer()
    test__tunnel_eckart_writer()
    test__tunnel_sct_writer()
