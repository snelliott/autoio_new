""" z-matrix writers
"""
import numpy


def write(syms, key_mat, name_mat, val_dct, mat_delim=' ', setval_sign='='):
    """ write a z-matrix to a string
    """
    mat_str = matrix_block(syms=syms, key_mat=key_mat, name_mat=name_mat,
                           delim=mat_delim)
    setval_str = setval_block(val_dct=val_dct, setval_sign=setval_sign)
    zma_str = '\n\n'.join((mat_str, setval_str))
    return zma_str


def matrix_block(syms, key_mat, name_mat, delim=' '):
    """ write the .zmat matrix block to a string
    """
    def _line_string(row_idx):
        line_str = '{:<2s} '.format(syms[row_idx])
        keys = key_mat[row_idx]
        names = name_mat[row_idx]
        line_str += delim.join([
            '{:>d}{}{:>5s} '.format(keys[col_idx], delim, names[col_idx])
            for col_idx in range(min(row_idx, 3))])
        return line_str

    natms = len(syms)
    mat_str = '\n'.join([_line_string(row_idx) for row_idx in range(natms)])
    return mat_str


def setval_block(val_dct, setval_sign='='):
    """ write the .zmat setval block to a string
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
