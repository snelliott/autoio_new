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
    FROZEN_DIS_STRS = 'frozen_dis_strs'
    FROZEN_ANG_STRS = 'frozen_ang_strs'
    FROZEN_DIH_STRS = 'frozen_dih_strs'
    # job
    COMMENT = 'comment'
    JOB_KEY = 'job_key'
    JOB_OPTIONS = 'job_options'
    GEN_LINES = 'gen_lines'
    GEN_LINES_1 = 'gen_lines_1'
    GEN_LINES_2 = 'gen_lines_2'
    GEN_LINES_3 = 'gen_lines_3'
    # theoretical method
    BASIS = 'basis'
    SCF_METHOD = 'scf_method'
    SCF_OPTIONS = 'scf_options'
    ISMULTIREF = 'ismultiref'
    CASSCF_OPTIONS = 'casscf_options'
    CORR_METHOD = 'corr_method'
    CORR_OPTIONS = 'corr_options'


# Format strings
def geometry_strings(geo, frozen_coordinates):
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
    elif geo in ('GEOMETRY', 'GEOMETRY_HERE'):
        geo_str = geo
        zmat_vval_str = ''
    else:
        raise ValueError("Invalid geometry value:\n{0}".format(geo))

    return geo_str, zmat_vval_str, zmat_cval_str


def _name_mat(zma, frozen_coordinates, job_key):
    """ Build the name matrix for a Z-Matrix data structure:

        used for cfour optimizations

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


def build_gen_lines(gen_lines, line1=None, line2=None, line3=None):
    """ Set three lines for writing in various blocks of files.
        Function either grabs lines from the dictionary and if nothing
        present, then uses value provided by function
    """

    if gen_lines is not None:
        gen_lines_1 = '\n'.join(gen_lines[1]) if 1 in gen_lines else ''
        gen_lines_2 = '\n'.join(gen_lines[2]) if 2 in gen_lines else ''
        gen_lines_3 = '\n'.join(gen_lines[3]) if 3 in gen_lines else ''
    else:
        gen_lines_1 = ''
        gen_lines_2 = ''
        gen_lines_3 = ''

    if not gen_lines_1:
        gen_lines_1 = line1 if line1 is not None else ''
    if not gen_lines_2:
        gen_lines_2 = line2 if line2 is not None else ''
    if not gen_lines_3:
        gen_lines_3 = line3 if line3 is not None else ''

    return gen_lines_1, gen_lines_2, gen_lines_3


def _geometry_strings(geo):
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
        zmat_val_str = ''
    elif automol.zmatrix.is_valid(geo):
        zma = geo
        symbs = automol.zmatrix.symbols(zma)
        key_mat = automol.zmatrix.key_matrix(zma, shift=1)
        name_mat = automol.zmatrix.name_matrix(zma)
        val_dct = automol.zmatrix.values(zma, angstrom=True, degree=True)

        geo_str = aw.zmatrix.matrix_block(symbs, key_mat, name_mat, delim=', ')
        zmat_val_str = aw.zmatrix.setval_block(val_dct)
    elif geo in ('GEOMETRY', 'GEOMETRY_HERE'):
        geo_str = geo
        zmat_val_str = ''
    else:
        raise ValueError("Invalid geometry value:\n{}".format(geo))

    return geo_str, zmat_val_str





def set_reference(prog, prog_ref_dct, method, mult, orb_restrited):
    if elstruct.par.Method.is_dft(method):
        if prog in (par.Program.GAUSSIAN09, par.Program.GAUSSIAN16):
            reference = ''
        else:
            reference = (Reference.RKS if orb_restricted else
                         Reference.UKS)
    elif mult != 1:
        reference = (Reference.ROHF if orb_restricted else
                     Reference.UHF)
    else:
        assert mult == 1 and orb_restricted is True
        reference = Reference.RHF

    return prog_ref_dct[reference]


def evaluate_options(opts, opt_eval_dct):
    opts = list(opts)
    for idx, opt in enumerate(opts):
        if elstruct.option.is_valid(opt):
            name = elstruct.option.name(opt)
            assert name in elstruct.par.OPTION_NAMES
            opts[idx] = opt_eval_dct[name](opt)
    return tuple(opts)


# Program specific?
# gaussian, orca
def intercept_scf_guess_option(scf_opts):
    guess_opts = []
    ret_scf_opts = []
    for opt in scf_opts:
        if (elstruct.option.is_valid(opt) and opt in
                elstruct.pclass.values(elstruct.par.Option.Scf.Guess)):
            guess_opts.append(opt)
        else:
            ret_scf_opts.append(opt)
    return guess_opts, ret_scf_opts


# molpro
def set_method(method, singlet):
    # Check if MultiReference Method; then check if casscf
    if elstruct.par.Method.is_multiref(method):
        ismultiref = True
        if elstruct.par.Method.is_casscf(method):
            corr_method = ''
        else:
            corr_method = elstruct.par.program_method_name(
                PROG, method, singlet)
    # Set methods if single reference
    else:
        ismultiref = False
        if elstruct.par.Method.is_correlated(method):
            corr_method = elstruct.par.program_method_name(
                PROG, method, singlet)
        else:
            corr_method = ''

    return corr_method, ismultiref

