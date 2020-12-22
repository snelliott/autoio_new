"""
  Handle moving about paths
"""

import os


def current_path():
    """ get original working directory
    """
    return os.getcwd()


def go_to(path):
    """ change directory to path and return the original working directory
    """
    os.chdir(path)


def prepare_path(path_lst, make=False):
    """ change directory to starting path, return chemkin path
    """

    path_lst = [path.lstrip('/') for path in path_lst]

    print('pathlst', path_lst)
    print('pathlst', *path_lst)
    path = os.path.join('/', *path_lst)
    print(path)
    if make:
        os.makedirs(path)

    return path


def write_file(string, path, file_name=''):
    """ Open a file and read it as a string
    """

    fname = os.path.join(path, file_name)
    with open(fname, 'w', errors='ignore') as file_obj:
        file_obj.write(string)


def read_file(path, file_name=''):
    """ Open a file and read it as a string
    """

    fname = os.path.join(path, file_name)
    with open(fname, 'r', errors='ignore') as file_obj:
        file_str = file_obj.read()

    return file_str
