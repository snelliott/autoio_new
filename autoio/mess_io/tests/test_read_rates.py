"""
 tests rates reader
"""

import mess_io.reader
from _util import read_text_file


OUT_STR = read_text_file(['data'], 'rates.out')

# Set the REACTANT and PRODUCT
REACTANT = 'REACS'
PRODUCT = 'WR'


def test__rates():
    """ tests mess_io.reader.rates functions
    """

    # Read the temperatures from the output
    temps, tunit = mess_io.reader.rates.get_temperatures(OUT_STR)
    print('\nTemperatures:')
    print(temps)
    print(tunit)

    # Read the pressures from the output
    pressures, punit = mess_io.reader.rates.get_pressures(OUT_STR)
    print('\nPressures:')
    print(pressures)
    print(punit)

    # Read the high-pressure rate constants
    highp_rates = mess_io.reader.highp_ks(
        OUT_STR, REACTANT, PRODUCT)
    print('\nHigh-Pressure Rate-Constants:')
    print(highp_rates)

    # Read pressure-dependent rate constants at two pressures
    p1_rates = mess_io.reader.pdep_ks(
        OUT_STR, REACTANT, PRODUCT, pressures[3])
    print('\n{0} {1} Rate-Constants:'.format(pressures[3], punit))
    print(p1_rates)

    p2_rates = mess_io.reader.pdep_ks(
        OUT_STR, REACTANT, PRODUCT, pressures[4])
    print('\n{0} {1} Rate-Constants:'.format(pressures[4], punit))
    print(p2_rates)


if __name__ == '__main__':
    test__rates()
