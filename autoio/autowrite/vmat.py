""" V-Matrix writers
"""

from autowrite._mat import matrix_block


def write(symbs, key_mat, name_mat, mat_delim=' '):
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

    vma_str = matrix_block(
        symbs=symbs, key_mat=key_mat, name_mat=name_mat, delim=mat_delim)

    return vma_str
