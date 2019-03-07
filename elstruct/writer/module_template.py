""" empty functions defining the function signatures for each program module
"""


def method_list():
    """ _ """
    raise NotImplementedError


def basis_list():
    """ _ """
    raise NotImplementedError


def energy(method, basis, geom, mult, charge,
           # molecule options
           mol_options=(),
           # machine options
           memory=1, comment='', machine_options=(),
           # theory options
           scf_options=(), corr_options=()):
    """ _ """

    raise NotImplementedError(
        method, basis, geom, mult, charge,
        mol_options,
        memory, comment, machine_options,
        corr_options, scf_options,
    )


def gradient(method, basis, geom, mult, charge,
             # molecule options
             mol_options=(),
             # machine options
             memory=1, comment='', machine_options=(),
             # theory options
             scf_options=(), corr_options=()):
    """ _ """

    raise NotImplementedError(
        method, basis, geom, mult, charge,
        mol_options,
        memory, comment, machine_options,
        corr_options, scf_options,
    )


def hessian(method, basis, geom, mult, charge,
            # molecule options
            mol_options=(),
            # machine options
            memory=1, comment='', machine_options=(),
            # theory options
            scf_options=(), corr_options=()):
    """ _ """

    raise NotImplementedError(
        method, basis, geom, mult, charge,
        mol_options,
        memory, comment, machine_options,
        corr_options, scf_options,
    )


def optimization(method, basis, geom, mult, charge,
                 # molecule options
                 mol_options=(),
                 # machine options
                 memory=1, comment='', machine_options=(),
                 # theory options
                 scf_options=(), corr_options=(),
                 # molecule/optimization options
                 opt_options=()):
    """ _ """

    raise NotImplementedError(
        method, basis, geom, mult,
        charge, mol_options,
        memory, comment, machine_options,
        corr_options, scf_options,
        opt_options,
    )
