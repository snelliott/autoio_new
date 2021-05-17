"""
  Handle the generation of paths as well, moving between them
  and interacting with files that may exist at the paths.
"""

import os
from ioformat._format import remove_comment_lines
from ioformat._format import (
    remove_whitespace_from_string as remove_whitespace_)


def current_path():
    """ Obtain the path of the current working path.
    """
    return os.getcwd()


def go_to(path):
    """ Move to the directory that exists at a specified path.

        :param path: path of directory to move to
        :type path: str
    """
    os.chdir(path)


def prepare_path(path_lst, make=False):
    """ Build a full path from a list of strings that define parts of the
        path, and if requested, make a directory at the path.

        :param path_lst: list of strings which, when combined, define path
        :type path_lst: tuple(str)
        :param make: paramter to control making a directory at the path
        :type make: bool
        :rtype: str
    """

    path_lst = [path.lstrip('/') for path in path_lst]

    path = os.path.join('/', *path_lst)
    if make:
        os.makedirs(path)

    return path


def write_file(string, path, file_name):
    """ Write a given string in a file with specified prefix path
        and name.

        :param string: string to write to file
        :type string: str
        :param path: path of directory where file will be written
        :type path: str
        :param file_name: name of file to be written
        :type file_name: str
    """

    fname = os.path.join(path, file_name)
    with open(fname, 'w', errors='ignore') as file_obj:
        file_obj.write(string)


def read_file(path, file_name, remove_comments=None, remove_whitespace=False):
    """ Read a file with specified prefix path
        and name into a string.

        :param path: path of directory where file will be read
        :type path: str
        :param file_name: name of file to be read
        :type file_name: str
        :rtype: str
    """

    fname = os.path.join(path, file_name)
    if os.path.exists(fname):
        with open(fname, 'r', errors='ignore') as file_obj:
            file_str = file_obj.read()
            if remove_comments is not None:
                file_str = remove_comment_lines(file_str, remove_comments)
            if remove_whitespace:
                file_str = remove_whitespace_(file_str)
    else:
        file_str = None

    return file_str
