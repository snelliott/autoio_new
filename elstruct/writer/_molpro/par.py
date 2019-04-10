""" elstruct.writer._g09 parameters
"""
from elstruct import Option
from elstruct import option


MOLPRO_OPTION_EVAL_DCT = {
    option.name(Option.Scf.MAXITER_):
    lambda osp: 'maxit={}'.format(*option.values(osp)),
    option.name(Option.Scf.DIIS_):
    lambda osp: ('iptyp=diis' if option.values(osp)[0] else 'iptyp=none'),
}
OPTION_NAMES = tuple(sorted(MOLPRO_OPTION_EVAL_DCT.keys()))
