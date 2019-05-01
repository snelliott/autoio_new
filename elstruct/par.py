""" elstruct parameters
"""
from elstruct import pclass
from elstruct import option


def standard_case(name):
    """ return name with standard capitalization
    """
    return name.lower()


class Module():
    """ elstruct module names """
    WRITER = 'writer'
    READER = 'reader'


class Program():
    """ Programs to be called """
    PSI4 = 'psi4'
    G09 = 'g09'
    MOLPRO = 'molpro'


def programs():
    """ list the available electronic structure backend programs
    """
    return pclass.all_values(Program)


def is_program(prog):
    """ is this a possible backend program?
    """
    prog = standard_case(prog)
    return prog in programs()


class Method():
    """ electronic structure methods

    (name, {program: name,
                     closed shell orb restrictions,
                     open shell orb restrictions})
    """
    HF = ('hf',
          {Program.PSI4: (
              None, None,
              (True,), (False, True)),
           Program.G09: (
               None, None,
               (True,), (False, True)),
           Program.MOLPRO: (
               None, None,
               (True,), (False, True))})

    class Dft():
        """ DFT method names """
        B3LYP = ('b3lyp',
                 {Program.PSI4: (
                     'B3LYP', 'B3LYP',
                     (True,), (False,)),
                  Program.G09: (
                      'b3lyp', 'b3lyp',
                      (True,), (False,))})
        WB97XD = ('wb97xd',
                  {Program.PSI4: (
                      'WB97X-D', 'WB97X-D',
                      (True,), (False,)),
                   Program.G09: (
                       'wb97xd', 'wb97xd',
                       (True,), (False,))})
        M062X = ('m062x',
                 {Program.PSI4: (
                     'M06-2X', 'M06-2X',
                     (True,), (False,)),
                  Program.G09: (
                      'm062x', 'm062x',
                      (True,), (False,))})
        B2PLYPD3 = ('b2plypd3',
                    {Program.G09: (
                        'b2plypd3', 'b2plypd3',
                        (True,), (False,))})

    class Corr():
        """ correlated method names """
        MP2 = ('mp2',
               {Program.PSI4: (
                   None, None,
                   (True,), (False, True)),
                Program.G09: (
                    None, None,
                    (True,), (False, True))})
        CCSD = ('ccsd',
                {Program.MOLPRO: (
                    'ccsd', 'uccsd',
                    (True,), (True,))})
        # CCSDPTF12 = ('ccsd(t)-f12',
        #              {Program.MOLPRO: (
        #                  'ccsd(t)-f12', 'uccsd(t)-f12',
        #                  (True,), (True,))})

    @classmethod
    def contains(cls, name):
        """ does this parametr class contain this value?
        """
        name = standard_case(name)
        names = [row[0] for row in pclass.all_values(cls)]
        return name in names

    @classmethod
    def is_dft(cls, name):
        """ is this a DFT method?
        """
        assert cls.contains(name)
        name = standard_case(name)
        dft_names = [row[0] for row in pclass.all_values(cls.Dft)]
        return name in dft_names

    @classmethod
    def is_correlated(cls, name):
        """ is this a DFT method?
        """
        assert cls.contains(name)
        name = standard_case(name)
        corr_names = [row[0] for row in pclass.all_values(cls.Corr)]
        return name in corr_names


def program_methods_info(prog):
    """ list the methods available for a given program, with their information
    """
    prog = standard_case(prog)
    return {row[0]: row[1][prog] for row in pclass.all_values(Method)
            if prog in row[1]}


def program_methods(prog):
    """ list the methods available for a given program
    """
    return tuple(sorted(program_methods_info(prog)))


def program_dft_methods(prog):
    """ list the DFT methods available for a given program
    """
    prog_methods = program_methods(prog)
    return tuple(method for method in prog_methods
                 if Method.is_dft(method))


def program_nondft_methods(prog):
    """ list the DFT methods available for a given program
    """
    prog_methods = program_methods(prog)
    return tuple(method for method in prog_methods
                 if not Method.is_dft(method))


def program_method_name(prog, method, open_shell=False):
    """ list the name of a method for a given program
    """
    prog = standard_case(prog)
    method = standard_case(method)
    prog_method_dct = program_methods_info(prog)
    assert method in prog_method_dct
    name = (prog_method_dct[method][0] if not open_shell else
            prog_method_dct[method][1])
    return method if name is None else name


def program_method_orbital_restrictions(prog, method, open_shell):
    """ list the possible orbital restrictions for a given method and program
    """
    prog = standard_case(prog)
    method = standard_case(method)
    prog_method_dct = program_methods_info(prog)
    assert method in prog_method_dct
    orb_restrictions = (prog_method_dct[method][2] if not open_shell else
                        prog_method_dct[method][3])
    return orb_restrictions


def is_program_method(prog, method):
    """ is this a valid method for this program?
    """
    prog = standard_case(prog)
    method = standard_case(method)
    return method in program_methods(prog)


def is_program_method_orbital_restriction(prog, method, open_shell,
                                          orb_restricted):
    """ is this a valid method for this program?
    """
    prog = standard_case(prog)
    method = standard_case(method)
    assert isinstance(open_shell, bool)
    return (orb_restricted
            in program_method_orbital_restrictions(prog, method, open_shell))


class Basis():
    """ electronic structure basis sets

    (name, {program: name})
    """
    STO3G = ('sto-3g', {Program.PSI4: None,
                        Program.G09: None,
                        Program.MOLPRO: None})

    class Pople:
        """ Pople basis sets """
        P321 = ('3-21g', {Program.PSI4: None,
                          Program.G09: None,
                          Program.MOLPRO: None})
        P631 = ('6-31g', {Program.PSI4: None,
                          Program.G09: None,
                          Program.MOLPRO: None})
        P631S = ('6-31g*', {Program.PSI4: None,
                            Program.G09: None,
                            Program.MOLPRO: None})
        P631PS = ('6-31+g*', {Program.PSI4: None,
                              Program.G09: None,
                              Program.MOLPRO: None})

    class Dunning():
        """ Dunning basis sets """
        D = ('cc-pvdz', {Program.PSI4: None,
                         Program.G09: None,
                         Program.MOLPRO: None})
        T = ('cc-pvtz', {Program.PSI4: None,
                         Program.G09: None,
                         Program.MOLPRO: None})
        Q = ('cc-pvqz', {Program.PSI4: None,
                         Program.G09: None,
                         Program.MOLPRO: None})

        class Aug():
            """ augmented Dunning basis sets """
            D = ('aug-cc-pvdz', {Program.PSI4: None,
                                 Program.G09: None,
                                 Program.MOLPRO: None})

    @classmethod
    def contains(cls, name):
        """ does this parametr class contain this value?
        """
        name = standard_case(name)
        names = [row[0] for row in pclass.all_values(cls)]
        return name in names


def program_bases(prog):
    """ list the methods available for a given program
    """
    prog = standard_case(prog)
    return {row[0]: row[1][prog] for row in pclass.all_values(Basis)
            if prog in row[1]}


def program_basis_name(prog, basis):
    """ list the name of a basis for a given program
    """
    prog = standard_case(prog)
    basis = standard_case(basis)
    prog_bases = program_bases(prog)
    assert basis in prog_bases
    name = prog_bases[basis]
    return basis if name is None else name


def is_program_basis(prog, basis):
    """ is this a valid basis for this program?
    """
    prog = standard_case(prog)
    basis = standard_case(basis)
    return basis in program_bases(prog)


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
