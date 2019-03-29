""" elstruct.writer._g09 parameters
"""
import elstruct.par
from elstruct import Option
from elstruct import option

# method/basis lists, with maps to gaussian names
G09_METHOD_DCT = {
    elstruct.par.Method.HF: 'hf',
    elstruct.par.Method.Corr.MP2: 'mp2',
    elstruct.par.Method.Dft.B3LYP: 'b3lyp',
    elstruct.par.Method.Dft.WB97XD: 'wb97xd',
}
METHODS = tuple(sorted(G09_METHOD_DCT.keys()))

G09_BASIS_DCT = {
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
BASES = tuple(sorted(G09_BASIS_DCT.keys()))

G09_OPTION_EVAL_DCT = {
    option.name(Option.Scf.MAXITER_):
    lambda osp: 'MaxCycle={}'.format(*option.values(osp)),
    option.name(Option.Scf.DIIS_):
    lambda osp: ('DIIS' if option.values(osp)[0] else 'NoDIIS'),
    option.name(Option.Scf.Guess.CORE):
    lambda osp: 'Core',
    option.name(Option.Scf.Guess.HUCKEL):
    lambda osp: 'Huckel',
    option.name(Option.Opt.MAXITER_):
    lambda osp: 'MaxCycle={}'.format(*option.values(osp)),
    # don't do this -- it breaks z-matrix reading
    # option.name(Option.Opt.Coord.CARTESIAN):
    # lambda osp: 'Cartesian',
    option.name(Option.Opt.Coord.ZMATRIX):
    lambda osp: 'Z-matrix',
    option.name(Option.Opt.Coord.REDUNDANT):
    lambda osp: 'Redundant',
}
OPTION_NAMES = tuple(sorted(G09_OPTION_EVAL_DCT.keys()))


# mako template keys
class G09Reference():
    """ _ """
    RHF = 'rhf'
    UHF = 'uhf'
    ROHF = 'rohf'


class JobKey():
    """ _ """
    ENERGY = 'energy'
    OPTIMIZATION = 'optimization'
    GRADIENT = 'gradient'
    HESSIAN = 'hessian'


class TemplateKey():
    """ mako template keys """
    # machine
    MEMORY = 'memory'
    MACHINE_OPTIONS = 'machine_options'
    # theoretical method
    REFERENCE = 'reference'
    METHOD = 'method'
    BASIS = 'basis'
    SCF_OPTIONS = 'scf_options'
    SCF_GUESS_OPTIONS = 'scf_guess_options'
    # molecule / state
    MOL_OPTIONS = 'mol_options'
    COMMENT = 'comment'
    CHARGE = 'charge'
    MULT = 'mult'
    GEOM = 'geom'
    ZMAT_VAR_VALS = 'zmat_var_vals'
    ZMAT_CONST_VALS = 'zmat_const_vals'
    # job
    JOB_KEY = 'job_key'
    JOB_OPTIONS = 'job_options'
