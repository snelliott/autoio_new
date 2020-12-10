""" elstruct.writer._mrcc2018 parameters
"""
from elstruct import Option
from elstruct import option


MRCC2018_OPTION_EVAL_DCT = {
    option.name(Option.Scf.MAXITER_):
    lambda osp: 'scfmaxit={}'.format(*option.values(osp)),
    option.name(Option.Opt.MAXITER_):
    lambda osp: 'optmaxit'.format(*option.values(osp)),
}
OPTION_NAMES = tuple(sorted(MRCC2018_OPTION_EVAL_DCT.keys()))
