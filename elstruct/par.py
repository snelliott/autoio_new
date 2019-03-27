""" elstruct parameters
"""
from elstruct import pclass
from elstruct import option


class Program():
    """ Programs to be called """
    PSI4 = 'psi4'
    G09 = 'g09'


class Module():
    """ elstruct module names """
    WRITER = 'writer'
    READER = 'reader'


class Basis():
    """ electronic structure basis sets """
    STO3G = 'sto-3g'

    class Pople:
        """ Pople basis sets """
        P321 = '3-21g'
        P631 = '6-31g'
        P631S = '6-31g*'
        P631PS = '6-31+g*'

    class Dunning():
        """ Dunning basis sets """
        D = 'cc-pvdz'
        T = 'cc-pvtz'
        Q = 'cc-pvqz'

        class Aug():
            """ augmented Dunning basis sets """
            D = 'aug-cc-pvdz'


class Method():
    """ electronic structure methods """
    HF = 'hf'

    class Dft():
        """ DFT method names """
        B3LYP = 'b3lyp'

    class Corr():
        """ correlated method names """
        MP2 = 'mp2'

    @classmethod
    def is_dft(cls, method):
        """ is this a DFT method?
        """
        method = method.lower()
        assert method in pclass.all_values(cls)
        return method in pclass.all_values(cls.Dft)


class Job():
    """ The type of job
    """
    ENERGY = 'energy'
    GRADIENT = 'gradient'
    HESSIAN = 'hessian'
    OPTIMIZATION = 'optimization'


class Error():
    """ Job errors
    """
    SCF_NOCONV = 'scf_noconv'
    OPT_NOCONV = 'opt_noconv'


class Option():
    """ Writer option values
    """

    class Scf():
        """ SCF options (passed to `scf_options`) """
        MAXITER_ = option.create('scf_maxiter', ['num'])
        DIIS_ = option.create('scf_diis', ['bool'])

        class Guess():
            """ _ """
            CORE = option.create('scf_guess_core')
            HUCKEL = option.create('scf_guess_huckel')

    class Opt():
        """ optimization options (passed to `job_options`) """
        MAXITER_ = option.create('opt_maxiter', ['num'])

        class Coord():
            """ optimization coordinate system """
            CARTESIAN = option.create('opt_coord_cartesian')
            ZMATRIX = option.create('opt_coord_zmatrix')
            REDUNDANT = option.create('opt_coord_redundant')
