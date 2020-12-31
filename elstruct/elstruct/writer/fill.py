"""
   Useful functions used for all the program writers
"""


import automol
import autowrite as aw
import elstruct


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
    CHARGE = 'charge'
    MULT = 'mult'
    GEOM = 'geom'
    ZMAT_VAR_VALS = 'zmat_var_vals'
    ZMAT_CONST_VALS = 'zmat_const_vals'
    # job
    COMMENT = 'comment'
    JOB_KEY = 'job_key'
    JOB_OPTIONS = 'job_options'
    GEN_LINES = 'gen_lines'


def _geometry_strings(geo, frozen_coordinates):
    """ Build the string for the input geometry

        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
        :param frozen_coordinates: only with z-matrix geometries; list of
            coordinate names to freeze
        :type fozen_coordinates: tuple[str]
        :rtype: (str, str)
    """

    if automol.geom.is_valid(geo):
        geo_str = automol.geom.string(geo)
        zmat_vval_str = ''
        zmat_cval_str = ''
    elif automol.zmatrix.is_valid(geo):
        zma = geo
        symbs = automol.zmatrix.symbols(zma)
        key_mat = automol.zmatrix.key_matrix(zma, shift=1)
        name_mat = automol.zmatrix.name_matrix(zma)
        val_dct = automol.zmatrix.values(zma, angstrom=True, degree=True)
        geo_str = aw.zmatrix.matrix_block(symbs, key_mat, name_mat)

        vval_dct = {key: val for key, val in val_dct.items()
                    if key not in frozen_coordinates}
        cval_dct = {key: val for key, val in val_dct.items()
                    if key in frozen_coordinates}

        zmat_vval_str = aw.zmatrix.setval_block(
            vval_dct, setval_sign=' ').strip()
        zmat_cval_str = aw.zmatrix.setval_block(
            cval_dct, setval_sign=' ').strip()
    else:
        raise ValueError("Invalid geometry value:\n{0}".format(geo))

    return geo_str, zmat_vval_str, zmat_cval_str


def _name_mat(zma, frozen_coordinates, job_key):
    """ Build the name matrix for a Z-Matrix data structure:

        :param zma: cartesian or z-matrix geometry
        :type zma: tuple
        :param frozen_coordinates: only with z-matrix geometries; list of
            coordinate names to freeze
        :type fozen_coordinates: tuple[str]
        :param job_key: job contained in the inpit file
        :type job_key: str
    """
    if job_key == 'optimization':
        name_mat = [
            [name+'*'
             if name is not None and name not in frozen_coordinates else name
             for name in row]
            for row in automol.zmatrix.name_matrix(zma)]
    else:
        name_mat = automol.zmatrix.name_matrix(zma)

    return name_mat


def _reference(method, mult, orb_restricted):
    if elstruct.par.Method.is_dft(method):
        reference = ''
    elif mult != 1:
        reference = (GAUSSIAN09Reference.ROHF
                     if orb_restricted else GAUSSIAN09Reference.UHF)
    else:
        assert mult == 1 and orb_restricted is True
        reference = GAUSSIAN09Reference.RHF
    return reference


def _intercept_scf_guess_option(scf_opts):
    guess_opts = []
    ret_scf_opts = []
    for opt in scf_opts:
        if (elstruct.option.is_valid(opt) and opt in
                elstruct.pclass.values(elstruct.par.Option.Scf.Guess)):
            guess_opts.append(opt)
        else:
            ret_scf_opts.append(opt)
    return guess_opts, ret_scf_opts


def _evaluate_options(opts, opt_eval_dct):
    opts = list(opts)
    for idx, opt in enumerate(opts):
        if elstruct.option.is_valid(opt):
            name = elstruct.option.name(opt)
            assert name in elstruct.par.OPTION_NAMES
            opts[idx] = opt_eval_dct[name](opt)
    return tuple(opts)
