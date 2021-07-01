""" elstruct.writer._molpro2015 parameters
"""

from elstruct import Option
from elstruct import option
import elstruct.par


REF_DCT = {
    elstruct.par.Reference.RHF: 'rhf',
    elstruct.par.Reference.UHF: 'uhf'
}


class MultiReference():
    """ _ """
    CASSCF = 'casscf'
    CASPT2 = 'rs2'
    CASPT2I = 'rs2'
    CASPT2C = 'rs2c'
    MRCI_Q = 'mrci'


OPTION_EVAL_DCT = {
    elstruct.option.name(elstruct.par.Option.Mol.NOSYMM_):
    'nosym',
    option.name(Option.Scf.MAXITER_):
    lambda osp: 'maxit={}'.format(*option.values(osp)),
    option.name(Option.Scf.DIIS_):
    lambda osp: ('iptyp=diis' if option.values(osp)[0] else 'iptyp=none'),
    option.name(Option.Casscf.OCC_):
    lambda osp: 'occ,{}'.format(*option.values(osp)),
    option.name(Option.Casscf.CLOSED_):
    lambda osp: 'closed,{}'.format(*option.values(osp)),
    option.name(Option.Casscf.WFN_):
    lambda osp: 'wf,{},{},{},{};state,{}'.format(*option.values(osp)),
    option.name(Option.MRCorr.SHIFT_):
    lambda osp: 'shift={}'.format(*option.values(osp)),
    option.name(Option.Opt.MAXITER_):
    lambda osp: 'maxit={}'.format(*option.values(osp)),
    elstruct.option.name(Option.Corr.ALL_ELEC_):
    'core',
}


def set_method_and_options(method, mods, corr_options):  # , gen_lines):
    """ Set corr options based on the method
    """

    if mods[elstruct.par.Method.ModPrefix.ALL_ELEC[0]]:
        allelec_opt = elstruct.option.name(Option.Corr.ALL_ELEC_)
        if allelec_opt not in corr_options:
            corr_options += (allelec_opt,)

    # if rel:
    # corr_options, scf_options = ['cwrelativistic'] -> 'expec,rel,darwin
    # {method;
    #  expec,rel,darwin,massv}
    # molpro2 add gen_lines_2: 'dkroll=1'
    # dkroll=1
    # {method}

    return method, corr_options, method
