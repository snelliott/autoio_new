""" elstruct parameters
"""

from elstruct import pclass
from elstruct import option


def standard_case(name):
    """ Reformat name in standard lowercase capitalization.

        :param name: name to reformat
        :type name: str
        :rtype: str
    """
    return name.lower()


class Module():
    """ elstruct module names """
    WRITER = 'writer'
    READER = 'reader'


class Program():
    """ Programs supported in elstruct """
    CFOUR2 = 'cfour2'
    GAUSSIAN09 = 'gaussian09'
    GAUSSIAN16 = 'gaussian16'
    MOLPRO2015 = 'molpro2015'
    MRCC2018 = 'mrcc2018'
    NWCHEM6 = 'nwchem6'
    ORCA4 = 'orca4'
    PSI4 = 'psi4'
    QCHEM5 = 'qchem5'


def programs():
    """ List all electronic structure backend programs that are supported.
    """
    return pclass.all_values(Program)


def is_program(prog):
    """ Asssess if a program is supported as a backend program.

        :param prog: name of program to test
        :type prog: str
        :rtype: bool
    """
    return standard_case(prog) in programs()


class Reference():
    """ References for density functional and wavefunction methods. """
    RHF = 'rhf'
    UHF = 'uhf'
    ROHF = 'rohf'
    RKS = 'rks'
    UKS = 'uks'


class Method():
    """ Program specific names for various electronic structure methods
        as well as their references.

        (name, {program: singlet name,
                         multiplet name,
                         singlet orb modes,
                         multiplet orb modes})
    """

    HF = ('hf',
          {Program.CFOUR2: (
              'rhf', 'hf',
              ('R',), ('U', 'R')),
           Program.GAUSSIAN09: (
               'hf', 'hf',
               ('R',), ('U', 'R')),
           Program.GAUSSIAN16: (
               'hf', 'hf',
               ('R',), ('U', 'R')),
           Program.MOLPRO2015: (
               'hf', 'hf',
               ('R',), ('U', 'R')),
           Program.MRCC2018: (
               'hf', 'hf',
               ('R',), ('U', 'R')),
           Program.ORCA4: (
               'hf', 'uhf',
               ('R',), ('U', 'R')),
           Program.PSI4: (
               'hf', 'uhf',
               ('R',), ('U', 'R'))})
    DF_HF = ('df-hf',
             {Program.PSI4: (
                 'hf', 'uhf',
                 ('R',), ('U', 'R'))})

    class Corr():
        """ Correlated method names """
        MP2 = ('mp2',
               {Program.CFOUR2: (
                   'mp2', 'mp2',
                   ('R',), ('U', 'R')),
                Program.GAUSSIAN09: (
                    'mp2', 'mp2',
                    ('R',), ('U', 'R')),
                Program.GAUSSIAN16: (
                    'mp2', 'mp2',
                    ('R',), ('U', 'R')),
                Program.MOLPRO2015: (
                    'mp2', 'ump2',
                    ('R',), ('U', 'R')),
                Program.MRCC2018: (
                    'mp2', 'mp2',
                    ('R',), ('U', 'R')),
                Program.ORCA4: (
                    'mp2', 'mp2',
                    ('R',), ('U', 'R')),
                Program.PSI4: (
                    'mp2', 'mp2',
                    ('R',), ('U', 'R'))})
        # DF_MP2 = ('df-mp2',
        #           {Program.PSI4: (
        #            'mp2', 'mp2',
        #            ('R',), ('U', 'R'))})
        CCSD = ('ccsd',
                {Program.CFOUR2: (
                    'ccsd', 'ccsd',
                    ('R',), ('U', 'R',)),
                 # Program.PSI4: (
                 #    'ccsd', 'ccsd',
                 #    ('R',), ('U', 'R',)),
                 Program.MOLPRO2015: (
                     'ccsd', 'uccsd',
                     ('R',), ('R', 'R'))})
        CCSD_T = ('ccsd(t)',
                  {Program.CFOUR2: (
                      'ccsd(t)', 'ccsd(t)',
                      ('R',), ('R',)),
                   Program.MOLPRO2015: (
                       'ccsd(t)', 'uccsd(t)',
                       ('R',), ('R',)),
                   Program.MRCC2018: (
                       'ccsd(t)', 'ccsd(t)',
                       ('R',), ('R', 'R'))})
        # Program.PSI4: (
        #  'ccsd(t)', 'ccsd(t)',
        #  ('R',), ('U', 'R'))})
        CCSDT = ('ccsdt',
                 {Program.MOLPRO2015: (
                     'mrcc,method=ccsdt', 'mrcc,method=ccsdt',
                     ('R',), ('U', 'R')),
                  Program.MRCC2018: (
                      'ccsdt', 'ccsdt',
                      ('R',), ('R', 'R'))})
        CCSDT_Q = ('ccsdt(q)',
                   {Program.MOLPRO2015: (
                       'mrcc,method=ccsdt(q)', 'mrcc,method=ccsdt(q)',
                       ('R',), ('U', 'R')),
                    Program.MRCC2018: (
                        'ccsdt(q)', 'ccsdt(q)',
                        ('R',), ('R', 'R'))})
        CCSD_T_F12 = ('ccsd(t)-f12',
                      {Program.MOLPRO2015: (
                          'ccsd(t)-f12', 'uccsd(t)-f12',
                          ('R',), ('R',))})

    class MultiRef():
        """ Multireference electronic structure methods
        """
        CASSCF = ('casscf',
                  {Program.MOLPRO2015: (
                      'casscf', 'casscf',
                      ('R',), ('R', 'R'))})
        CASPT2 = ('caspt2',
                  {Program.MOLPRO2015: (
                      'rs2', 'rs2',
                      ('R',), ('R', 'R'))})
        CASPT2I = ('caspt2i',
                   {Program.MOLPRO2015: (
                       'rs2', 'rs2',
                       ('R',), ('R', 'R'))})
        CASPT2C = ('caspt2c',
                   {Program.MOLPRO2015: (
                       'rs2c', 'rs2c',
                       ('R',), ('R', 'R'))})
        MRCISDQ = ('mrcisd_q',
                   {Program.MOLPRO2015: (
                       'mrci', 'mrci',
                       ('R',), ('R', 'R'))})

    class Dft():
        """ Density functional theory method names """
        B3LYP = ('b3lyp',
                 {Program.PSI4: (
                     'B3LYP', 'B3LYP',
                     ('R',), ('U',)),
                  Program.GAUSSIAN09: (
                      'b3lyp', 'b3lyp',
                      ('R',), ('U',)),
                  Program.GAUSSIAN16: (
                      'b3lyp', 'b3lyp',
                      ('R',), ('U',))})
        DF_B3LYP = ('df-b3lyp',
                    {Program.PSI4: (
                        'B3LYP', 'B3LYP',
                        ('R',), ('U',))})
        WB97XD = ('wb97xd',
                  {Program.PSI4: (
                      'WB97X-D', 'WB97X-D',
                      ('R',), ('U',)),
                   Program.GAUSSIAN09: (
                       'wb97xd', 'wb97xd',
                       ('R',), ('U',)),
                   Program.GAUSSIAN16: (
                       'wb97xd', 'wb97xd',
                       ('R',), ('U',))})
        M062X = ('m062x',
                 {Program.PSI4: (
                     'M06-2X', 'M06-2X',
                     ('R',), ('U',)),
                  Program.GAUSSIAN09: (
                      'm062x', 'm062x',
                      ('R',), ('U',)),
                  Program.GAUSSIAN16: (
                      'm062x', 'm062x',
                      ('R',), ('U',))})
        B2PLYPD3 = ('b2plypd3',
                    {Program.GAUSSIAN09: (
                        'b2plypd3', 'b2plypd3',
                        ('R',), ('U',)),
                     Program.GAUSSIAN16: (
                         'b2plypd3', 'b2plypd3',
                         ('R',), ('U',))})

    @classmethod
    def contains(cls, name):
        """ Assess if provided method is a part of this class.

            :param cls: class object
            :type cls: obj
            :param name: name of method
            :type name: str
        """

        name = standard_case(name)
        names = [row[0] for row in pclass.all_values(cls)]

        return name in names

    @classmethod
    def is_correlated(cls, name):
        """ Assess if a method is a single-reference correlated method.

            :param cls: class object
            :type cls: obj
            :param name: name of method
            :type name: str
        """

        name = standard_case(name)
        corr_names = [row[0] for row in pclass.all_values(cls.Corr)]

        return name in corr_names

    @classmethod
    def is_multiref(cls, name):
        """ Assess if a method is a multi-reference correlated method.

            :param cls: class object
            :type cls: obj
            :param name: name of method
            :type name: str
        """

        name = standard_case(name)
        multiref_names = [row[0] for row in pclass.all_values(cls.MultiRef)]

        return name in multiref_names

    @classmethod
    def is_casscf(cls, name):
        """ Assess if a method is CASSCF.

            :param cls: class object
            :type cls: obj
            :param name: name of method
            :type name: str
        """
        return standard_case(name) == 'casscf'

    @classmethod
    def is_standard_dft(cls, name):
        """ Assess if a method corresponds to a density functional
            currently defined in elstruct.

            :param cls: class object
            :type cls: obj
            :param name: name of method
            :type name: str
        """

        name = standard_case(name)
        dft_names = [row[0] for row in pclass.all_values(cls.Dft)]

        return name in dft_names

    @staticmethod
    def is_nonstandard_dft(name):
        """ Assess if a method corresponds to a user-defined
            density functional (indicated by 'dft:<name>').

            :param name: name of method
            :type name: str
        """
        return name.lower().startswith('dft:')

    @classmethod
    def is_dft(cls, name):
        """ Assess if a method corresponds to a density functional
            (either standard or non-standard).
        """
        return cls.is_standard_dft(name) or cls.is_nonstandard_dft(name)

    @classmethod
    def nonstandard_dft_name(cls, name):
        """ Extract the name of a non-standard density functional
            (indicated by 'dft:<name>').

            :param cls: class object
            :type cls: obj
            :param name: name of method
            :type name: str
        """
        assert cls.is_nonstandard_dft(name)
        return name[4:]

    @staticmethod
    def is_density_fitting(name):
        """ Assess if a method is `density-fitting` variant.

            :param cls: class object
            :type cls: obj
            :param name: name of method
            :type name: str
        """
        return 'df-' in standard_case(name)


def program_methods_info(prog):
    """ List methods available for a given program, with their information.

        :param prog: electronic structure program name
        :type prog: str
        :rtype: dict[str: str]
    """
    prog = standard_case(prog)
    return {row[0]: row[1][prog] for row in pclass.all_values(Method)
            if prog in row[1]}


def program_methods(prog):
    """ List methods available for a given program.

        :param prog: electronic structure program name
        :type prog: str
        :rtype: tuple(str)
    """
    return tuple(sorted(program_methods_info(prog)))


def program_dft_methods(prog):
    """ List density functional theory methods available for a given program.

        :param prog: electronic structure program name
        :type prog: str
        :rtype: tuple(str)
    """
    prog_methods = program_methods(prog)
    return tuple(method for method in prog_methods
                 if Method.is_standard_dft(method))


def program_nondft_methods(prog):
    """ List Hartree-Fock wavefunction methods available for a given program.

        :param prog: electronic structure program name
        :type prog: str
        :rtype: tuple(str)
    """
    prog_methods = program_methods(prog)
    return tuple(method for method in prog_methods
                 if not Method.is_standard_dft(method))


def program_method_name(prog, method, singlet=True):
    """ Obtain the name of a given method specific to the program provided.

        :param prog: electronic structure program name
        :type prog: str
        :param method: electronic structure method name
        :type method: str
        :param singlet: Parameter specifying name for singlet species
        :type singlet: bool
        :rtype: tuple(str)
    """

    prog = standard_case(prog)

    if Method.is_nonstandard_dft(method):
        method = Method.nonstandard_dft_name(method)
    else:
        method = standard_case(method)
        prog_method_dct = program_methods_info(prog)
        assert method in prog_method_dct
        name = (prog_method_dct[method][0] if singlet else
                prog_method_dct[method][1])
        method = method if name is None else name

    return method


def program_method_orbital_types(prog, method, singlet):
    """ Obtain the available orbital modes of a given method
        specific to the program provided.

        :param prog: electronic structure program name
        :type prog: str
        :param method: electronic structure method name
        :type method: str
        :param singlet: Parameter specifying name for singlet species
        :type singlet: bool
        :rtype: tuple(str)
    """

    prog = standard_case(prog)
    method = standard_case(method)
    prog_method_dct = program_methods_info(prog)
    assert method in prog_method_dct
    orb_types = (prog_method_dct[method][2] if singlet else
                 prog_method_dct[method][3])

    return orb_types


def is_program_method(prog, method):
    """ Assess if the given method is valid for the specific program.

        :param prog: electronic structure program name
        :type prog: str
        :param method: electronic structure method name
        :type method: str
    """

    prog = standard_case(prog)
    method = standard_case(method)

    return method in program_methods(prog)


def is_program_method_orbital_type(prog, method, singlet, orb_type):
    """ is this a valid method for this program?
    """
    prog = standard_case(prog)
    method = standard_case(method)
    assert isinstance(singlet, bool)
    return orb_type in program_method_orbital_types(prog, method, singlet)


class Basis():
    """ Electronic structure basis sets, defined internally in elstruct,
        as well as dictionary that maps the name of the basis set into the
        name for all of the implemented electronic structure programs.

        (name, {program: name})
    """

    STO3G = ('sto-3g', {Program.CFOUR2: None,
                        Program.GAUSSIAN09: None,
                        Program.GAUSSIAN16: None,
                        Program.MOLPRO2015: None,
                        Program.MRCC2018: None,
                        Program.NWCHEM6: None,
                        Program.ORCA4: None,
                        Program.PSI4: None})

    class Pople:
        """ Pople basis sets """
        P321 = ('3-21g', {Program.CFOUR2: None,
                          Program.GAUSSIAN09: None,
                          Program.GAUSSIAN16: None,
                          Program.MOLPRO2015: None,
                          Program.MRCC2018: None,
                          Program.NWCHEM6: None,
                          Program.ORCA4: None,
                          Program.PSI4: None})
        P321S = ('3-21g*', {Program.PSI4: None})
        P631 = ('6-31g', {Program.CFOUR2: None,
                          Program.GAUSSIAN09: None,
                          Program.GAUSSIAN16: None,
                          Program.MOLPRO2015: None,
                          Program.MRCC2018: None,
                          Program.NWCHEM6: None,
                          Program.ORCA4: None,
                          Program.PSI4: None})
        P631S = ('6-31g*', {Program.CFOUR2: None,
                            Program.GAUSSIAN09: None,
                            Program.GAUSSIAN16: None,
                            Program.MOLPRO2015: None,
                            Program.MRCC2018: None,
                            Program.NWCHEM6: None,
                            Program.ORCA4: None,
                            Program.PSI4: None})
        P6311SS = ('6-311g**', {Program.CFOUR2: None,
                                Program.GAUSSIAN09: None,
                                Program.GAUSSIAN16: None,
                                Program.MOLPRO2015: None,
                                Program.MRCC2018: None,
                                Program.NWCHEM6: None,
                                Program.ORCA4: None,
                                Program.PSI4: None})
        P631PS = ('6-31+g*', {Program.CFOUR2: None,
                              Program.GAUSSIAN09: None,
                              Program.GAUSSIAN16: None,
                              Program.MOLPRO2015: None,
                              Program.MRCC2018: None,
                              Program.NWCHEM6: None,
                              Program.ORCA4: None,
                              Program.PSI4: None})

    class Dunning():
        """ Dunning basis sets """
        D = ('cc-pvdz', {Program.CFOUR2: None,
                         Program.GAUSSIAN09: None,
                         Program.GAUSSIAN16: None,
                         Program.MOLPRO2015: None,
                         Program.MRCC2018: None,
                         Program.NWCHEM6: None,
                         Program.ORCA4: None,
                         Program.PSI4: None})
        T = ('cc-pvtz', {Program.CFOUR2: None,
                         Program.GAUSSIAN09: None,
                         Program.GAUSSIAN16: None,
                         Program.MOLPRO2015: None,
                         Program.MRCC2018: None,
                         Program.NWCHEM6: None,
                         Program.ORCA4: None,
                         Program.PSI4: None})
        Q = ('cc-pvqz', {Program.CFOUR2: None,
                         Program.GAUSSIAN09: None,
                         Program.GAUSSIAN16: None,
                         Program.MOLPRO2015: None,
                         Program.MRCC2018: None,
                         Program.NWCHEM6: None,
                         Program.ORCA4: None,
                         Program.PSI4: None})
        P = ('cc-pv5z', {Program.CFOUR2: None,
                         Program.GAUSSIAN09: None,
                         Program.GAUSSIAN16: None,
                         Program.MOLPRO2015: None,
                         Program.MRCC2018: None,
                         Program.NWCHEM6: None,
                         Program.ORCA4: None,
                         Program.PSI4: None})

        class Aug():
            """ Augmented Dunning basis sets """
            AD = ('aug-cc-pvdz', {Program.CFOUR2: None,
                                  Program.GAUSSIAN09: None,
                                  Program.GAUSSIAN16: None,
                                  Program.MOLPRO2015: None,
                                  Program.MRCC2018: None,
                                  Program.NWCHEM6: None,
                                  Program.ORCA4: None,
                                  Program.PSI4: None})
            AT = ('aug-cc-pvtz', {Program.CFOUR2: None,
                                  Program.GAUSSIAN09: None,
                                  Program.GAUSSIAN16: None,
                                  Program.MOLPRO2015: None,
                                  Program.MRCC2018: None,
                                  Program.NWCHEM6: None,
                                  Program.ORCA4: None,
                                  Program.PSI4: None})
            AQ = ('aug-cc-pvqz', {Program.CFOUR2: None,
                                  Program.GAUSSIAN09: None,
                                  Program.GAUSSIAN16: None,
                                  Program.MOLPRO2015: None,
                                  Program.MRCC2018: None,
                                  Program.NWCHEM6: None,
                                  Program.ORCA4: None,
                                  Program.PSI4: None})
            A5 = ('aug-cc-pv5z', {Program.CFOUR2: None,
                                  Program.GAUSSIAN09: None,
                                  Program.GAUSSIAN16: None,
                                  Program.MOLPRO2015: None,
                                  Program.MRCC2018: None,
                                  Program.NWCHEM6: None,
                                  Program.ORCA4: None,
                                  Program.PSI4: None})

        class F12():
            """ Dunning F12 basis sets """
            DF = ('cc-pvdz-f12', {Program.MOLPRO2015: None})
            TF = ('cc-pvtz-f12', {Program.MOLPRO2015: None})
            QF = ('cc-pvqz-f12', {Program.MOLPRO2015: None})

    @classmethod
    def contains(cls, name):
        """ Assess if provided basis set is a part of this class.

            :param cls: class object
            :type cls: obj
            :param name: name of basis set
            :type name: str
        """
        name = standard_case(name)
        names = [row[0] for row in pclass.all_values(cls)]
        return name in names

    is_standard_basis = contains

    @staticmethod
    def is_nonstandard_basis(name):
        """ Assess if a basis set corresponds to user-defined
            basis set (indicated by 'basis:<name>').

            :param name: name of basis set
            :type name: str
        """
        return name.lower().startswith('basis:')

    @classmethod
    def nonstandard_basis_name(cls, name):
        """ Extract the aname of non-standard basis set
            (indicated by 'basis:<name>').
        """
        assert cls.is_nonstandard_basis(name)
        return name[6:]


def program_bases(prog):
    """ List basis sets available for a given program.

        :param prog: electronic structure program name
        :type prog: str
        :rtype: dict[str: str]
    """
    prog = standard_case(prog)
    return {row[0]: row[1][prog] for row in pclass.all_values(Basis)
            if prog in row[1]}


def program_basis_name(prog, basis):
    """ Obtain the name of a given basis set specific to the program provided.

        :param prog: electronic structure program name
        :type prog: str
        :param basis: electronic structure basis set
        :type basis: str
    """

    prog = standard_case(prog)

    if Basis.is_nonstandard_basis(basis):
        basis = Basis.nonstandard_basis_name(basis)
    else:
        basis = standard_case(basis)
        prog_bases = program_bases(prog)
        assert basis in prog_bases
        name = prog_bases[basis]
        basis = basis if name is None else name

    return basis


def is_program_basis(prog, basis):
    """ Assess if the given basis set is valid for the specific program.

        :param prog: electronic structure program name
        :type prog: str
        :param basis: electronic structure basis set
        :type basis: str
    """

    prog = standard_case(prog)
    basis = standard_case(basis)

    return basis in program_bases(prog)


class Job():
    """ Names of electronic structure jobs whose input (output)
        can be written (read).
    """

    ENERGY = 'energy'
    GRADIENT = 'gradient'
    HESSIAN = 'hessian'
    OPTIMIZATION = 'optimization'
    VPT2 = 'vpt2'
    IRCF = 'ircf'
    IRCR = 'ircr'
    MOLPROP = 'molecular_properties'

    @classmethod
    def contains(cls, name):
        """ Assess if provided method is a part of this class.

            :param cls: class object
            :type cls: obj
            :param name: name of job
            :type name: str
        """

        name = standard_case(name)
        names = pclass.all_values(cls)
        # names = [row for row in pclass.all_values(cls)]

        return name in names


class Error():
    """ Types of error messages that can be found in electronic structure
        program output files.
    """
    SCF_NOCONV = 'scf_noconv'
    CC_NOCONV = 'cc_noconv'
    OPT_NOCONV = 'opt_noconv'
    IRC_NOCONV = 'irc_noconv'
    SYMM_NOFIND = 'symm_nofind'


class Success():
    """ Types of sucess errors that can be found in electronic structure
        program output files.
    """
    SCF_CONV = 'scf_conv'
    CC_CONV = 'cc_conv'
    OPT_CONV = 'opt_conv'
    IRC_CONV = 'irc_conv'


class Option():
    """ Option values for the electronic structure program writer module
    """

    class Mol():
        """ Options for molecules """
        NOSYMM_ = option.create('no_symmetry')

    class Scf():
        """ SCF options (passed to `scf_options`) """
        MAXITER_ = option.create('scf_maxiter', ['num'])
        DIIS_ = option.create('scf_diis', ['bool'])

        class Guess():
            """ Initial SCF guess generation methods """
            CORE = option.create('scf_guess_core')
            HUCKEL = option.create('scf_guess_huckel')
            MIX = option.create('scf_guess_mix')

    class Casscf():
        """ CASSCF options to set active space (passed to `casscf_options`) """
        OCC_ = option.create('casscf_occ', ['num'])
        CLOSED_ = option.create('casscf_closed', ['num'])
        WFN_ = option.create(
            'casscf_wavefunction',
            ['nelec', 'sym', 'spin', 'charge', 'nstates'])

    class Corr():
        """ Options for correlated methods"""
        ALL_ELEC_ = option.create('all_electron')

    class MRCorr():
        """ Correlated multiref method options (passed to `corr_options`) """
        SHIFT_ = option.create('level_shift', ['num'])

    class Opt():
        """ Optimization options (passed to `job_options`) """
        MAXITER_ = option.create('opt_maxiter', ['num'])

        class Coord():
            """ Corrdinate system to perform optimization in """
            CARTESIAN = option.create('opt_coord_cartesian')
            ZMATRIX = option.create('opt_coord_zmatrix')
            REDUNDANT = option.create('opt_coord_redundant')
