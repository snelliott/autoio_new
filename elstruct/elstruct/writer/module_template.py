""" empty functions defining the function signatures for each program module
"""


def energy(geo, charge, mult, method, basis,
           # molecule options
           mol_options=(),
           # machine options
           memory=1, comment='', machine_options=(),
           # theory options
           orb_restricted=None,
           scf_options=(), casscf_options=(), corr_options=(),
           # generic options
           gen_lines=None):
    """ _ """

    raise NotImplementedError(
        geo, charge, mult, method, basis,
        mol_options,
        memory, comment, machine_options,
        scf_options, casscf_options, corr_options,
        gen_lines
    )


def gradient(geo, charge, mult, method, basis,
             # molecule options
             mol_options=(),
             # machine options
             memory=1, comment='', machine_options=(),
             # theory options
             orb_restricted=None,
             scf_options=(), casscf_options=(), corr_options=(),
             # generic options
             gen_lines=None,
             # job options
             job_options=()):
    """ _ """

    raise NotImplementedError(
        geo, charge, mult, method, basis,
        mol_options,
        memory, comment, machine_options,
        scf_options, casscf_options, corr_options,
        gen_lines,
        job_options,
    )


def hessian(geo, charge, mult, method, basis,
            # molecule options
            mol_options=(),
            # machine options
            memory=1, comment='', machine_options=(),
            # theory options
            orb_restricted=None,
            scf_options=(), casscf_options=(), corr_options=(),
            # generic options
            gen_lines=None,
            # job options
            job_options=()):
    """ _ """

    raise NotImplementedError(
        geo, charge, mult, method, basis,
        mol_options,
        memory, comment, machine_options,
        scf_options, casscf_options, corr_options,
        gen_lines,
        job_options,
    )


def vpt2(geo, charge, mult, method, basis,
         # molecule options
         mol_options=(),
         # machine options
         memory=1, comment='', machine_options=(),
         # theory options
         orb_restricted=None,
         scf_options=(), casscf_options=(), corr_options=(),
         # generic options
         gen_lines=None,
         # job options
         job_options=()):
    """ _ """

    raise NotImplementedError(
        geo, charge, mult, method, basis,
        mol_options,
        memory, comment, machine_options,
        scf_options, casscf_options, corr_options,
        gen_lines,
        job_options,
    )


def molec_properties(geo, charge, mult, method, basis,
                     # molecule options
                     mol_options=(),
                     # machine options
                     memory=1, comment='', machine_options=(),
                     # theory options
                     orb_restricted=None,
                     scf_options=(), casscf_options=(), corr_options=(),
                     # generic options
                     gen_lines=None,
                     # job options
                     job_options=()):
    """ _ """

    raise NotImplementedError(
        geo, charge, mult, method, basis,
        mol_options,
        memory, comment, machine_options,
        scf_options, casscf_options, corr_options,
        gen_lines,
        job_options,
    )


def irc(geo, charge, mult, method, basis,
        # molecule options
        mol_options=(),
        # machine options
        memory=1, comment='', machine_options=(),
        # theory options
        orb_restricted=None,
        scf_options=(), casscf_options=(), corr_options=(),
        # generic options
        gen_lines=None,
        # job options
        job_options=(), frozen_coordinates=()):
    """ _ """

    raise NotImplementedError(
        geo, charge, mult, method, basis,
        mol_options,
        memory, comment, machine_options,
        scf_options, casscf_options, corr_options,
        gen_lines,
        job_options, frozen_coordinates
    )


def optimization(geo, charge, mult, method, basis,
                 # molecule options
                 mol_options=(),
                 # machine options
                 memory=1, comment='', machine_options=(),
                 # theory options
                 orb_restricted=None,
                 scf_options=(), casscf_options=(), corr_options=(),
                 # generic options
                 gen_lines=None,
                 # job options
                 job_options=(), frozen_coordinates=(), saddle=False):
    """ _ """

    raise NotImplementedError(
        geo, charge, mult, method, basis,
        mol_options,
        memory, comment, machine_options,
        scf_options, casscf_options, corr_options,
        gen_lines,
        job_options, frozen_coordinates, saddle
    )
