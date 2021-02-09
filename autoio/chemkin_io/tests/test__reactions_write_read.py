from chemkin_io.writer.mechanism import reactions_block as writer
from chemkin_io.parser.reaction import param_dct as parser
import numpy as np

ARRHENIUS_RXN_PARAM_DCT = {(('H', 'O2'), ('OH', 'O')):
                           [[1E+15, 0.00, 25000], None, None, None, None, None, None]}

LINDEMANN_RXN_PARAM_DCT = {(('H', 'O2'), ('OH', 'O')):
                           [[1E+15, 0.00, 25000], [1E+15, 0.00, 25000], None, None, None,
                               {'AR': 1.4, 'N2': 1.7}, '(+M)']}

TROE_RXN_PARAM_DCT = {(('H', 'O2'), ('OH', 'O')):
                           [[1E+15, 0.00, 25000], [1E+15, 0.00, 25000], [0.95, 1E-30, 8000], None, None, None, '(+M)']}

CHEBYSHEV_RXN_PARAM_DCT = {(('H', 'O2'), ('OH', 'O')):
                [[1E+15, 0.00, 25000], None, None, {'t_limits': [500.0, 2000.0],
                    'p_limits': [0.03, 100.0], 'alpha_elm': np.array([
                    [-1.620e+01, -1.183e-01, -5.423e-02, -1.476e-02],
                    [ 2.578e+00,  1.614e-01,  7.359e-02,  1.880e-02],
                    [ 1.068e-01, -7.235e-02, -2.733e-02, -3.778e-03],
                    [ 3.955e-02,  1.207e-02,  3.402e-04, -2.695e-03],
                    [ 8.557e-03,  4.345e-03,  3.670e-03,  1.608e-03],
                    [ 8.599e-04, -1.758e-03, -7.502e-04,  7.396e-07]]),
                    'a_units': 'moles'}, None, None, '(+M)']}

PLOG_RXN_PARAM_DCT = {(('H', 'O2'), ('OH', 'O')):
                           [[1E+15, 0.00, 25000], None, None, None,
                               {0.1: [1E+15, 0.00, 25000],
                                1.0: [1E+15, 0.00, 25000],
                                10.0: [1E+15, 0.00, 25000],
                                100.0: [1E+15, 0.00, 25000]},
                                None, None]}

def test__arrhenius():
    """ Tests the Arrhenius reader and writer
    """
    first_str, second_str = _get_strs(ARRHENIUS_RXN_PARAM_DCT)
    assert first_str == second_str


def test__lindemann():
    """ Tests the Lindemann reader and writer
    """
    first_str, second_str = _get_strs(LINDEMANN_RXN_PARAM_DCT)
    assert first_str == second_str


def test__troe():
    """ Tests the Troe reader and writer
    """
    first_str, second_str = _get_strs(TROE_RXN_PARAM_DCT)
    assert first_str == second_str


def test__plog():
    """ Tests the PLOG reader and writer
    """
    first_str, second_str = _get_strs(PLOG_RXN_PARAM_DCT)
    assert first_str == second_str


def test__chebyshev():
    """ Tests the Chebyshev reader and writer
    """
    first_str, second_str = _get_strs(CHEBYSHEV_RXN_PARAM_DCT)
    assert first_str == second_str


def _get_strs(rxn_param_dct):
    """ Gets two strs after passing a rxn_param_dct through the writer and reader
    """
    first_str = writer(rxn_param_dct)
    new_rxn_param_dct = parser(first_str, 'cal/mole', 'moles')
    second_str = writer(new_rxn_param_dct)
    
    return first_str, second_str


if __name__ == '__main__':
    test__arrhenius()
    test__lindemann()
    test__troe()
    test__chebyshev()
    test__plog()

