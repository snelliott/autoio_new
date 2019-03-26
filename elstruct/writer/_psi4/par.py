""" elstruct.writer._psi4 parameters
"""
import elstruct.par
import elstruct.option

# method/basis lists, with maps to psi4 names
PSI4_METHOD_DCT = {
    elstruct.par.Method.HF: 'hf',
    elstruct.par.Method.Dft.B3LYP: 'b3lyp',
    elstruct.par.Method.Corr.MP2: 'mp2',
}
METHODS = tuple(sorted(PSI4_METHOD_DCT.keys()))

PSI4_BASIS_DCT = {
    elstruct.par.Basis.STO3G: 'sto-3g',
    elstruct.par.Basis.Pople.P321: '3-21g',
    elstruct.par.Basis.Pople.P631: '6-31g',
    elstruct.par.Basis.Pople.P631S: '6-31g*',
    elstruct.par.Basis.Pople.P631PS: '6-31+g*',
    elstruct.par.Basis.Dunning.D: 'cc-pvdz',
    elstruct.par.Basis.Dunning.T: 'cc-pvtz',
    elstruct.par.Basis.Dunning.Q: 'cc-pvqz',
    elstruct.par.Basis.Dunning.Aug.D: 'aug-cc-pvdz',
}
BASES = tuple(sorted(PSI4_BASIS_DCT.keys()))

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


# mako template keys
class Psi4Reference():
    """ _ """
    RHF = 'rhf'
    UHF = 'uhf'
    ROHF = 'rohf'
    RKS = 'rks'
    UKS = 'uks'


class JobKey():
    """ _ """
    ENERGY = 'energy'
    OPTIMIZATION = 'optimization'
    GRADIENT = 'gradient'
    HESSIAN = 'hessian'


class TemplateKey():
    """ mako template keys """
    COMMENT = 'comment'
    MEMORY = 'memory'
    MACHINE_OPTIONS = 'machine_options'
    MOL_OPTIONS = 'mol_options'
    CHARGE = 'charge'
    MULT = 'mult'
    GEOM = 'geom'
    ZMAT_VALS = 'zmat_vals'
    BASIS = 'basis'
    REFERENCE = 'reference'
    SCF_OPTIONS = 'scf_options'
    CORR_OPTIONS = 'corr_options'
    METHOD = 'method'
    JOB_KEY = 'job_key'
    JOB_OPTIONS = 'job_options'
    FROZEN_DIS_STRS = 'frozen_dis_strs'
    FROZEN_ANG_STRS = 'frozen_ang_strs'
    FROZEN_DIH_STRS = 'frozen_dih_strs'
