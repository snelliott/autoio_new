"""
  Tests the varecof_io.writer functions
"""

import os
from ioformat import pathtools
import varecof_io


PATH = os.path.dirname(os.path.realpath(__file__))
DAT_PATH = os.path.join(PATH, 'data')

OUT_STR = pathtools.read_file(DAT_PATH, 'divsur.txt')


def test__divsur_frag_geoms_reader():
    """ tests varecof_io.reader.divsur.frag_geoms_divsur_frame
    """
    frag_geoms = varecof_io.reader.divsur.frag_geoms_divsur_frame(
        OUT_STR)
    print(frag_geoms)


if __name__ == '__main__':
    test__divsur_frag_geoms_reader()
