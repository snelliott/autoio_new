"""
 tests chemkin_io.writer.transport.properties
"""

from chemkin_io.writer.transport import properties as writer


SPC_TRANS_DCT = {
    'O2': {'shape_idx': 1,
           'epsilon': 107.4,
           'sigma': 3.458,
           'dipole_moment': 0.00,
           'polarizability': 1.600,
           'zrot': 3.800
           }
}

TRANS_STR = """! THEORETICAL TRANSPORT PROPERTIES
!
! (1) Shape, index denotes atom (0), linear molec. (1), nonlinear molec. (2);
! (2) Epsilon, the Lennard-Jones well depth, in K;
! (3) Sigma, the Lennard-Jones collision diameter, in Angstrom;
! (4) Mu, total dipole moment, in Debye;
! (5) Alpha, mean static polarizability, in Angstrom^3; and
! (6) Z_rot, rotational relaxation collision number at 298 K.
! Species           Shape     Epsilon   Sigma      Mu   Alpha   Z_Rot
O2                      1     154.525   1.830   0.000   0.237   3.800
"""


def test__transport_write():
    """ Tests the transport writer
    """
    trans_str = writer(SPC_TRANS_DCT)
    assert trans_str == TRANS_STR
