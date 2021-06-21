""" test ioformat.pathtools
"""

import tempfile
import numpy
import ioformat


# Generic/Text file
FILE_NAME = 'tmp_file.dat'
FILE_STR = (
    '  ## Gradient (Symmetry 0) ##\n'
    '  Irrep: 1 Size: 3 x 3\n'
    '\n'
    '            1         2         3\n'
    '\n'
    '    1     0.000     0.000     0.997\n'
    '    2     0.000    -0.749    -0.488\n'
    '    3    -0.000     0.749    -0.488\n')

# NumPy file
NP_NAME = 'tmp_numpy.dat'
NP_ARR = numpy.array(
    ((-4.0048955763, -0.3439866053, -0.0021431734),
     (-1.3627056155, -0.3412713280, 0.0239463418),
     (-4.7435343957, 1.4733340928, 0.7491098889),
     (-4.7435373042, -1.9674678465, 1.1075144307),
     (-4.6638955748, -0.5501793084, -1.9816675556),
     (-0.8648060003, -0.1539639444, 1.8221471090)))

# JSON file
JSON_NAME = 'tmp_json.dat'
JSON_DCT = {
    'a': 1,
    'b': {
        'ba': 10
    },
    'c': {
        'ca': {
            'caa': 100
        }
    }
}


def test__pathtools():
    """ test ioformat.pathtools.current_path
        test ioformat.pathtools.prepare_path
        test ioformat.pathtools.go_to
        test ioformat.pathtools.write_file
        test ioformat.pathtools.read_file
        test ioformat.pathtools.write_numpy_file
        test ioformat.pathtools.read_numpy_file
        test ioformat.pathtools.write_json_file
        test ioformat.pathtools.read_json_file
    """

    # Build tmp dir and paths
    cur_path = ioformat.pathtools.current_path()
    tmp_dir = tempfile.mkdtemp()
    tmp_path = ioformat.pathtools.prepare_path((cur_path, tmp_dir), make=True)

    # Enter tmp dir and write/read text files
    ioformat.pathtools.go_to(tmp_path)
    ioformat.pathtools.write_file(FILE_STR, tmp_path, FILE_NAME)
    ioformat.pathtools.go_to(cur_path)
    file_str = ioformat.pathtools.read_file(tmp_path, FILE_NAME)
    assert file_str == FILE_STR
    ioformat.pathtools.go_to(cur_path)

    # Write/read numpy files
    ioformat.pathtools.go_to(tmp_path)
    ioformat.pathtools.write_numpy_file(NP_ARR, tmp_path, NP_NAME)
    ioformat.pathtools.go_to(cur_path)
    arr = ioformat.pathtools.read_numpy_file(tmp_path, NP_NAME)
    assert numpy.allclose(NP_ARR, arr)

    # Enter tmp dir and write/read json files
    ioformat.pathtools.go_to(tmp_path)
    ioformat.pathtools.write_json_file(JSON_DCT, tmp_path, JSON_NAME)
    ioformat.pathtools.go_to(cur_path)
    dct = ioformat.pathtools.read_json_file(tmp_path, JSON_NAME)
    assert JSON_DCT == dct
