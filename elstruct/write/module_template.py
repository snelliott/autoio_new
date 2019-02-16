""" empty functions defining the function signatures for each write module
"""


def method_list():
    """ list of available electronic structure methods
    """
    raise NotImplementedError


def basis_list():
    """ list of available electronic structure basis sets
    """
    raise NotImplementedError


def energy_input_string(method, basis, geom, charge, mult,
                        # machine options
                        memory=1, comment='', machine_options='',
                        # theory options
                        scf_options='', corr_options='',
                        # molecule/optimization options
                        zmat_var_dct=None):
    """ energy input string

    :param method: the electronic structure energy/wavefunction Ansatz
    :type method: str
    :param basis: the basis set
    :type basis: str
    :param geom: cartesian or z-matrix internal coordinates
    :type geom: tuple
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
    :param zmat_var_dct: a dictionary of z-matrix variable names, keyed by
        zero-index coordinates; something like this {(0, 1, 3, 4): 'd1', ...};
    """

    raise NotImplementedError(
        method, basis, geom, charge, mult,
        memory, comment, machine_options, corr_options, scf_options,
        zmat_var_dct
    )


def optimization_input_string(method, basis, geom, charge, mult,
                              # machine options
                              memory=1, comment='', machine_options='',
                              # theory options
                              scf_options='', corr_options='',
                              # molecule/optimization options
                              opt_options='', zmat_var_dct=None):
    """ optimization input string

    :param method: the electronic structure energy/wavefunction Ansatz
    :type method: str
    :param basis: the basis set
    :type basis: str
    :param geom: cartesian or z-matrix internal coordinates
    :type geom: tuple
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
    :param opt_options: geometry optimization routine directives
    :type opt_options: str
    :param zmat_var_dct: a dictionary of z-matrix variable names, keyed by
        zero-index coordinates; something like this {(0, 1, 3, 4): 'd1', ...};
    """

    raise NotImplementedError(
        method, basis, geom, charge, mult,
        memory, comment, machine_options, corr_options, scf_options,
        opt_options, zmat_var_dct
    )
