""" mako template keys
"""

# machine
MEMORY = 'memory'
MACHINE_OPTIONS = 'machine_options'

# theoretical method
SCF_METHOD = 'scf_method'
BASIS = 'basis'
SCF_OPTIONS = 'scf_options'


# molecule / state
MOL_OPTIONS = 'mol_options'
COMMENT = 'comment'
CHARGE = 'charge'
MULTIPLICITY = 'mult'
GEOMETRY = 'geom'
ZMATRIX_VARIABLE_VALUES = 'zmat_var_vals'
ZMATRIX_CONSTANT_VALUES = 'zmat_const_vals'

# job
JOB_KEY = 'job_key'
OPT_OPTIONS = 'opt_options'


class JobKeys():
    """ _ """
    OPT = 'optimization'
    GRAD = 'gradient'
    HESS = 'hessian'
