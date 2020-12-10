""" test the writing of the energy transfer section
"""

import os
import mess_io


PATH = os.path.dirname(os.path.realpath(__file__))
# STR_PATH = os.path.join(PATH, 'data', 'srings')
STR_PATH = os.path.join(PATH, 'data')


def _read_str(str_name):
    with open(os.path.join(STR_PATH, str_name), 'r') as datfile:
        output_string = datfile.read()
    return output_string


def test__energy_trans_writer():
    """ tests writing the section to a file
    """

    # Use the writer to create a string for the energy transfer section
    edown_str = mess_io.writer.energy_down(
        exp_factor=150.0,
        exp_power=50.0,
        exp_cutoff=80.0
    )
    collid_str = mess_io.writer.collision_frequency(
        eps1=100.0,
        eps2=200.0,
        sig1=10.0,
        sig2=20.0,
        mass1=15.0,
        mass2=25.0)

    # Print the energy transfer section string
    print(edown_str)
    # print(collid_str)
    with open(os.path.join(STR_PATH, 'edown'), 'w') as datfile:
        datfile.write(edown_str)


if __name__ == '__main__':
    test__energy_trans_writer()
