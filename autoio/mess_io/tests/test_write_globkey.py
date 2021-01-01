""" test the writing of the global keyword section for reactions and messpf
"""

import mess_io.writer
from _util import read_text_file


TEMPS = (100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0)
PRESSURES = (0.01, 0.1, 1.0, 10.0, 100.0)
TEMP_STEP = 50
NTEMPS = 40
REL_TEMP_INC = 0.002
ATOM_DIST_MIN = 1.05
EXCESS_ENE_TEMP = 10000.0
WELL_EXTEND = 20000.0


def test__global_reaction():
    """ test mess_io.writer.global_reaction
    """

    glob_rxn1_str = mess_io.writer.global_reaction(
        TEMPS, PRESSURES)
    glob_rxn2_str = mess_io.writer.global_reaction(
        TEMPS, PRESSURES,
        excess_ene_temp=EXCESS_ENE_TEMP,
        well_extend=WELL_EXTEND)

    assert glob_rxn1_str == read_text_file(['data', 'inp'], 'glob_rxn1.inp')
    assert glob_rxn2_str == read_text_file(['data', 'inp'], 'glob_rxn2.inp')


def test__global_pf():
    """ tests writing the section to a file for messpf
    """

    glob_pf1_str = mess_io.writer.global_pf(
        temperatures=TEMPS)
    glob_pf2_str = mess_io.writer.global_pf(
        temperatures=())
    glob_pf3_str = mess_io.writer.global_pf(
        temperatures=(),
        temp_step=TEMP_STEP,
        ntemps=NTEMPS,
        rel_temp_inc=REL_TEMP_INC,
        atom_dist_min=ATOM_DIST_MIN)

    assert glob_pf1_str == read_text_file(['data', 'inp'], 'glob_pf1.inp')
    assert glob_pf2_str == read_text_file(['data', 'inp'], 'glob_pf2.inp')
    assert glob_pf3_str == read_text_file(['data', 'inp'], 'glob_pf3.inp')


def test__full_str():
    """ test mess_io.writer.messrates_inp_str
        test mess_io.writer.messpf_inp_str
    """

    glob_rxn_str = read_text_file(['data', 'inp'], 'glob_pf1.inp')
    glob_pf_str = read_text_file(['data', 'inp'], 'glob_pf1.inp')
    glob_etrans_str = read_text_file(['data', 'inp'], 'glob_etrans.inp')
    rxn_chan_str = '<FAKE REACTION CHANNEL_STR>'
    pf_str = '<FAKE PF CHANNEL_STR>'

    rates_inp_str = mess_io.writer.messrates_inp_str(
        glob_rxn_str, glob_etrans_str, rxn_chan_str)
    pf_inp_str = mess_io.writer.messpf_inp_str(
        glob_pf_str, pf_str)

    assert rates_inp_str == read_text_file(['data', 'inp'], 'full_rates.inp')
    assert pf_inp_str == read_text_file(['data', 'inp'], 'full_pf.inp')


if __name__ == '__main__':
    test__global_reaction()
    test__global_pf()
    test__full_str()
