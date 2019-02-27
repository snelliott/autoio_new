""" empty functions defining the function signatures for each program module
"""


def method_list():
    """ list of available electronic structure methods
    """
    raise NotImplementedError


def basis_list():
    """ list of available electronic structure basis sets
    """
    raise NotImplementedError


def energy(method, basis, geom, mult, charge,
           # molecule options
           mol_options='',
           # machine options
           memory=1, comment='', machine_options='',
           # theory options
           scf_options='', corr_options=''):
    """ energy input string

    :param method: the electronic structure energy/wavefunction Ansatz
    :type method: str
    :param basis: the basis set
    :type basis: str
    :param geom: cartesian or z-matrix geometry
    :type geom: tuple
    :param mult: spin multiplicity
    :type mult: int
    :param charge: molecular charge
    :type charge: int
    :param mol_options: options for the molecule block
    :type mol_options: str
    ;param memory: memory in GB
    :type memory: int
    :param comment: a comment string to be placed at the top of the file
    :type comment: str
    :param machine_options: machine directives (num procs, num threads, etc.)
    :type machine_options: str
    :param scf_options: scf method directives
    :type scf_options: str
    :param corr_options: correlation method directives
    :type corr_options: str
    """

    raise NotImplementedError(
        method, basis, geom, mult, charge,
        mol_options,
        memory, comment, machine_options,
        corr_options, scf_options,
    )


def optimization(method, basis, geom, mult, charge,
                 # molecule options
                 mol_options='',
                 # machine options
                 memory=1, comment='', machine_options='',
                 # theory options
                 scf_options='', corr_options='',
                 # molecule/optimization options
                 opt_options=''):
    """ optimization input string

    :param method: the electronic structure energy/wavefunction Ansatz
    :type method: str
    :param basis: the basis set
    :type basis: str
    :param geom: cartesian or z-matrix geometry
    :type geom: tuple
    :param mult: spin multiplicity
    :type mult: int
    :param charge: molecular charge
    :type charge: int
    :param mol_options: options for the molecule block
    :type mol_options: str
    :param memory: memory in GB
    :type memory: int
    :param comment: a comment string to be placed at the top of the file
    :type comment: str
    :param machine_options: machine directives (num procs, num threads, etc.)
    :type machine_options: str
    :param scf_options: scf method directives
    :type scf_options: str
    :param corr_options: correlation method directives
    :type corr_options: str
    :param opt_options: geometry optimization routine directives
    :type opt_options: str
    """

    raise NotImplementedError(
        method, basis, geom, mult,
        charge, mol_options,
        memory, comment, machine_options,
        corr_options, scf_options,
        opt_options,
    )
