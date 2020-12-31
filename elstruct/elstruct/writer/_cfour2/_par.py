""" elstruct.writer._cfour2 parameters
"""

from elstruct import Option
from elstruct import option


class Reference():
    """ _ """
    RHF = 'rhf'
    UHF = 'uhf'


CFOUR2_OPTION_EVAL_DCT = {
    option.name(Option.Scf.MAXITER_):
    lambda osp: 'SCF_MAXCYC={}'.format(*option.values(osp)),
    option.name(Option.Opt.MAXITER_):
    lambda osp: 'GEO_MAXCYC={}'.format(*option.values(osp)),
}
OPTION_NAMES = tuple(sorted(CFOUR2_OPTION_EVAL_DCT.keys()))
