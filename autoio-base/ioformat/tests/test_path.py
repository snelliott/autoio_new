"""
aa
"""

import tempfile
import ioformat


FILE_NAME = 'tmp.dat'
FILE_STR = (
    '  ## Gradient (Symmetry 0) ##\n'
    '  Irrep: 1 Size: 3 x 3\n'
    '\n'
    '            1         2         3\n'
    '\n'
    '    1     0.000     0.000     0.997\n'
    '    2     0.000    -0.749    -0.488\n'
    '    3    -0.000     0.749    -0.488\n')


def test__pathtools():
    """ test ioformat.pathtools.current_path
        test ioformat.pathtools.prepare_path
        test ioformat.pathtools.go_to
        test ioformat.pathtools.write_file
    """

    # Build tmp dir and paths
    cur_path = ioformat.pathtools.current_path()
    tmp_dir = tempfile.mkdtemp()
    tmp_path = ioformat.pathtools.prepare_path((cur_path, tmp_dir), make=True)

    # Enter tmp dir and write/read files
    ioformat.pathtools.go_to(tmp_path)
    ioformat.pathtools.write_file(FILE_STR, tmp_path, FILE_NAME)
    file_str = ioformat.pathtools.read_file(tmp_path, FILE_NAME)
    assert file_str == FILE_STR
