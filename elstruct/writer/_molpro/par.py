""" elstruct.writer._molpro parameters
"""
import elstruct.par
import elstruct.option

# method/basis lists, with maps to molpro names
MOLPRO_METHOD_DCT = {
    elstruct.par.Method.HF: 'hf',
    elstruct.par.Method.Corr.MP2: 'mp2',
}
METHODS = tuple(sorted(MOLPRO_METHOD_DCT.keys()))

MOLPRO_BASIS_DCT = {
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
BASES = tuple(sorted(MOLPRO_BASIS_DCT.keys()))


# mako template keys
class MolproReference():
    """ _ """
    RHF = 'rhf'
    UHF = 'uhf'


class JobKey():
    """ _ """
    ENERGY = 'energy'
    OPTIMIZATION = 'optimization'
    GRADIENT = 'gradient'
    HESSIAN = 'hessian'


class TemplateKey():
    """ mako template keys """
    COMMENT = 'comment'
    MEMORY_MW = 'memory_mw'
    MACHINE_OPTIONS = 'machine_options'
    MOL_OPTIONS = 'mol_options'
    GEOM = 'geom'
    CHARGE = 'charge'
    SPIN = 'spin'
    BASIS = 'basis'
    REFERENCE = 'reference'
    SCF_OPTIONS = 'scf_options'
    CORR_OPTIONS = 'corr_options'
    METHOD = 'method'
