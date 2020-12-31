""" elstruct.writer._psi4 parameters
"""
import elstruct.par
import elstruct.option


class Reference():
    """ _ """
    RHF = 'rhf'
    UHF = 'uhf'
    ROHF = 'rohf'
    RKS = 'rks'
    UKS = 'uks'


PSI4_OPTION_EVAL_DCT = {
    elstruct.option.name(elstruct.par.Option.Scf.MAXITER_):
    lambda osp: 'set scf maxiter {}'.format(*elstruct.option.values(osp)),
    elstruct.option.name(elstruct.par.Option.Scf.DIIS_):
    lambda osp: 'set scf diis {}'.format(*elstruct.option.values(osp)),
    elstruct.option.name(elstruct.par.Option.Scf.Guess.CORE):
    lambda osp: 'set scf guess core',
    elstruct.option.name(elstruct.par.Option.Scf.Guess.HUCKEL):
    lambda osp: 'set scf guess huckel',
    elstruct.option.name(elstruct.par.Option.Opt.MAXITER_):
    lambda osp: 'set geom_maxiter {}'.format(*elstruct.option.values(osp)),
    elstruct.option.name(elstruct.par.Option.Opt.Coord.CARTESIAN):
    lambda osp: 'set opt_coordinates cartesian',
    elstruct.option.name(elstruct.par.Option.Opt.Coord.ZMATRIX):
    lambda osp: 'set opt_coordinates internal',
    elstruct.option.name(elstruct.par.Option.Opt.Coord.REDUNDANT):
    lambda osp: 'set opt_coordinates redundant',
}
OPTION_NAMES = tuple(sorted(PSI4_OPTION_EVAL_DCT.keys()))
