""" Tests the writing of the energy transfer section
"""

import onedmin_io


def test__input_file():
    """ test onedmin_io.writer.input_file
    """

    ranseed = 28384920
    nsamp = 10
    target_xyz_name = 'target.xyz'
    bath_xyz_name = 'bath.xyz'
    smin = 2.0
    smax = 5.0

    inp_str = onedmin_io.writer.input_file(
        ranseed, nsamp, smin, smax,
        target_xyz_name, bath_xyz_name)
    print(inp_str)


if __name__ == '__main__':
    test__input_file()
