""" test the writing of the global keyword section for reactions and messpf
"""

import os
import numpy
import pandas
from ioformat import read_text_file
import mess_io.writer


PATH = os.path.dirname(os.path.realpath(__file__))
TEMPS = (100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0)
PRESSURES = (0.01, 0.1, 1.0, 10.0, 100.0)
TEMP_STEP = 50
NTEMPS = 40
REL_TEMP_INC = 0.002
ATOM_DIST_MIN = 1.05
EXCESS_ENE_TEMP = 10000.0
WELL_EXTEND = 20000.0

# For messpf output
FORMULA = 'CH4O'
THM_TEMPS = numpy.array([
    100., 200., 300., 400., 500., 600., 700., 800., 900., 1000.,
    1100., 1200., 1300., 1400., 1500., 1600., 1700., 1800., 1900., 2000.,
    2100., 2200., 2300., 2400., 2500., 2600., 2700., 2800., 2900., 3000.,
    298.2
])
DATA = numpy.array([
    [60.1983, 0.0302761, -0.000290427, 125.642, 6.26152],
    [62.3581, 0.0163207, -6.51731e-05, 130.404, 7.79248],
    [63.7557, 0.0123154, -2.28447e-05, 134.037, 10.5982],
    [64.9053, 0.0109421, -6.74453e-06, 137.677, 15.2508],
    [65.9811, 0.010705, 1.21039e-06, 141.754, 21.8742],
    [67.0664, 0.0110813, 5.9895e-06, 146.486, 30.7096],
    [68.2106, 0.011859, 9.42064e-06, 152.044, 42.1657],
    [69.4485, 0.0129453, 1.22352e-05, 158.587, 56.7204],
    [70.8085, 0.014296, 1.47438e-05, 166.278, 74.8681],
    [72.3157, 0.0158886, 1.70879e-05, 175.279, 97.1045],
    [73.9938, 0.0177105, 1.93376e-05, 185.754, 123.924],
    [75.8652, 0.0197543, 2.15298e-05, 197.865, 155.822],
    [77.9519, 0.0220153, 2.36856e-05, 211.779, 193.291],
    [80.2754, 0.0244906, 2.58173e-05, 227.657, 236.825],
    [82.8571, 0.0271782, 2.79324e-05, 245.665, 286.916],
    [85.7181, 0.0300767, 3.00358e-05, 265.967, 344.056],
    [88.8794, 0.033185, 3.21303e-05, 288.727, 408.737],
    [92.3621, 0.0365025, 3.4218e-05, 314.109, 481.447],
    [96.1869, 0.0400285, 3.63002e-05, 342.276, 562.677],
    [100.375, 0.0437624, 3.83778e-05, 373.392, 652.913],
    [104.946, 0.0477039, 4.04514e-05, 407.622, 752.643],
    [109.922, 0.0518526, 4.25216e-05, 445.127, 862.354],
    [115.324, 0.0562081, 4.45887e-05, 486.072, 982.53],
    [121.171, 0.0607702, 4.6653e-05, 530.619, 1113.66],
    [127.485, 0.0655386, 4.87146e-05, 578.931, 1256.22],
    [134.285, 0.0705131, 5.07739e-05, 631.171, 1410.71],
    [141.594, 0.0756933, 5.2831e-05, 687.501, 1577.6],
    [149.431, 0.0810792, 5.4886e-05, 748.084, 1757.37],
    [157.817, 0.0866705, 5.6939e-05, 813.082, 1950.52],
    [166.772, 0.0924669, 5.89903e-05, 882.657, 2157.52],
    [63.7335, 0.0123569, -2.32761e-05, 133.973, 10.5319]
])
THM_VALS = pandas.DataFrame(
    data=DATA,
    index=THM_TEMPS,
    columns=('logq', 'dq_dt', 'd2q_dt2', 'svals', 'cpvals')
)


def test__global_rates_input():
    """ test mess_io.writer.global_rates_input
    """

    glob1_str = mess_io.writer.global_rates_input(
        TEMPS, PRESSURES)
    glob2_str = mess_io.writer.global_rates_input(
        TEMPS, PRESSURES,
        excess_ene_temp=EXCESS_ENE_TEMP,
        well_extend=WELL_EXTEND)

    assert glob1_str == read_text_file(['data', 'inp'], 'glob_rxn1.inp', PATH)
    assert glob2_str == read_text_file(['data', 'inp'], 'glob_rxn2.inp', PATH)


def test__global_pf_input():
    """ tests writing the section to a file for messpf
    """

    glob1_str = mess_io.writer.global_pf_input(
        temperatures=TEMPS)
    glob2_str = mess_io.writer.global_pf_input(
        temperatures=())
    glob3_str = mess_io.writer.global_pf_input(
        temperatures=(),
        temp_step=TEMP_STEP,
        ntemps=NTEMPS,
        rel_temp_inc=REL_TEMP_INC,
        atom_dist_min=ATOM_DIST_MIN)

    assert glob1_str == read_text_file(
        ['data', 'inp'], 'glob_pf1.inp', PATH, strip=True)
    assert glob2_str == read_text_file(
        ['data', 'inp'], 'glob_pf2.inp', PATH, strip=True)
    assert glob3_str == read_text_file(
        ['data', 'inp'], 'glob_pf3.inp', PATH, strip=True)


def test__full_str():
    """ test mess_io.writer.messrates_inp_str
        test mess_io.writer.messpf_inp_str
    """

    glob_keys_str = '<FAKE GLOB KEYS STR>'
    glob_etrans_str = '<FAKE ETRANS STR>'
    rxn_chan_str = '<FAKE REACTION CHANNEL STR>'
    pf_str = '<FAKE PF CHANNEL STR>'

    rates_str = mess_io.writer.messrates_inp_str(
        glob_keys_str, glob_etrans_str, rxn_chan_str)
    pf_str = mess_io.writer.messpf_inp_str(
        glob_keys_str, pf_str)

    assert rates_str == read_text_file(['data', 'inp'], 'full_rates.inp', PATH)
    assert pf_str == read_text_file(['data', 'inp'], 'full_pf.inp', PATH)


def test__pf_output():
    """ test mess_io.writer.pf_output
    """

    pf1_str = mess_io.writer.pf_output(
        FORMULA, THM_TEMPS,
        THM_VALS['logq'].values,
        THM_VALS['dq_dt'].values,
        THM_VALS['d2q_dt2'].values)

    pf2_str = mess_io.writer.pf_output(
        FORMULA, THM_TEMPS,
        THM_VALS['logq'].values,
        THM_VALS['dq_dt'].values,
        THM_VALS['d2q_dt2'].values,
        svals=THM_VALS['svals'].values,
        cpvals=THM_VALS['cpvals'].values)

    assert pf1_str == read_text_file(['data', 'out'], 'pf.dat2', PATH)
    assert pf2_str == read_text_file(['data', 'out'], 'pf.dat3', PATH)
