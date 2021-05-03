"""
Functions to read data files
"""

import os
import numpy
from io import StringIO as _StringIO


PATH = os.path.dirname(os.path.realpath(__file__))


def read_text_file(path_lst, file_name, path=PATH):
    """ Read a file
    """
    file_path = os.path.join(path, *path_lst, file_name)
    with open(file_path, 'r') as fobj:
        file_str = fobj.read().rstrip()
    return file_str


def write_text_file(path_lst, file_name, file_str, path=PATH):
    """ Read a file
    """
    file_path = os.path.join(path, *path_lst, file_name)
    with open(file_path, 'w') as fobj:
        file_str = fobj.write(file_str)


def load_numpy_string_file(path_lst, file_name):
    """ Read a file with numpy
    """
    file_str = read_text_file(path_lst, file_name)
    # file_path = os.path.join(PATH, *path_lst, file_name)
    file_str_io = _StringIO(file_str)
    file_lst = numpy.loadtxt(file_str_io)

    return file_lst
