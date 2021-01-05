""" z-matrix writers
"""

import numpy


def write(symbs, key_mat, name_mat, val_dct, mat_delim=' ', setval_sign='='):
    """ Writes a Z-matrix to a string.

        :param symbs: atomic symbols of the atoms
        :type symbs: tuple(str)
        :param key_mat: key/index columns of the z-matrix, zero-indexed
        :type key_mat: tuple[tuple[float, float or None, float or None]]
        :param name_mat: coordinate name columns of the z-matrix
        :type name_mat; tuple[tuple[str, str or None, str or None]]
        :param val_dct: values of the Z-matrix coordinates
        :type val_dct: dict[str: float]
        :param mat_delim: delimiter for the columns of the Z-matrix block
        :type mat_delim: str
        :param setval_sign: delimiter for coordinate and value in setval block
        :type setval_sign: str
        :rtype: str
    """

    mat_str = matrix_block(symbs=symbs, key_mat=key_mat, name_mat=name_mat,
                           delim=mat_delim)
    setval_str = setval_block(val_dct=val_dct, setval_sign=setval_sign)
    zma_str = '\n\n'.join((mat_str, setval_str))

    return zma_str


def matrix_block(symbs, key_mat, name_mat, delim=' '):
    """ Write the Z-matrix block, where atoms and coordinates are defined,
        to a string.

        :param symbs: atomic symbols of the atoms
        :type symbs: tuple(str)
        :param key_mat: key/index columns of the z-matrix, zero-indexed
        :type key_mat: tuple[tuple[float, float or None, float or None]]
        :param name_mat: coordinate name columns of the z-matrix
        :type name_mat; tuple[tuple[str, str or None, str or None]]
        :param delim: delimiter for the columns of the Z-matrix block
        :type delim: str
        :rtype: str
    """

    def _line_string(row_idx):
        line_str = '{:<2s} '.format(symbs[row_idx])
        keys = key_mat[row_idx]
        names = name_mat[row_idx]
        line_str += delim.join([
            '{:>d}{}{:>5s} '.format(keys[col_idx], delim, names[col_idx])
            for col_idx in range(min(row_idx, 3))])
        return line_str

    natms = len(symbs)
    mat_str = '\n'.join([_line_string(row_idx) for row_idx in range(natms)])

    return mat_str


def setval_block(val_dct, setval_sign='='):
    """ Write the setval block, where values of the coordinates are assigned,
        to a string.

        :param val_dct: values of the Z-matrix coordinates
        :type val_dct: dict[str: float]
        :param setval_sign: delimiter for coordinate and value in setval block
        :type setval_sign: str
        :rtype: str
    """

    char_dct = {'R': 0, 'A': 1, 'D': 2}

    def _sort_priority(arg):
        """ return a sort priority value for z-matrix variable names
        """
        name, _ = arg
        char, num = name[0], name[1:]
        char_val = char_dct[char] if char in char_dct else 99
        num_val = int(num) if num.isdigit() else numpy.inf
        return (char_val, num_val)

    items = sorted(val_dct.items(), key=_sort_priority)

    setval_str = '\n'.join([
        '{:<5s}{}{:>11.6f}'.format(name, setval_sign, val)
        for name, val in items])

    return setval_str
