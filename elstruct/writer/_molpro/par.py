""" elstruct.writer._molpro parameters
"""
from elstruct import Option
from elstruct import option


MOLPRO_OPTION_EVAL_DCT = {
    option.name(Option.Scf.MAXITER_):
    lambda osp: 'maxit={}'.format(*option.values(osp)),
    option.name(Option.Scf.DIIS_):
    lambda osp: ('iptyp=diis' if option.values(osp)[0] else 'iptyp=none'),
    option.name(Option.Casscf.OCC_):
    lambda osp: 'occ,{}'.format(*option.values(osp)),
    option.name(Option.Casscf.CLOSED_):
    lambda osp: 'closed,{}'.format(*option.values(osp)),
    option.name(Option.Casscf.WFN_):
    lambda osp: 'wf,{},{},{},{}'.format(*option.values(osp)),
    option.name(Option.MRCorr.SHIFT_):
    lambda osp: 'shift={}'.format(*option.values(osp)),
    option.name(Option.Opt.MAXITER_):
    lambda osp: 'maxit={}'.format(*option.values(osp)),
}
OPTION_NAMES = tuple(sorted(MOLPRO_OPTION_EVAL_DCT.keys()))
