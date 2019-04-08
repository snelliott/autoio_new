""" molpro writer module """
import os
import automol
import elstruct.par
from elstruct import pclass
from elstruct.writer._molpro import par

# set the path to the template files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


def method_list():
    """ list of available electronic structure methods
    """
    return par.METHODS


def basis_list():
    """ list of available electronic structure basis sets
    """
    return par.BASES


# def energy(method, basis, geom, mult, charge,
#            # molecule options
#            mol_options=(),
#            # machine options
#            memory=1, comment='', machine_options=(),
#            # theory options
#            orb_restricted=None, scf_options=(), corr_options=()):
#     """ energy input string
#     """
#     job_key = par.JobKey.ENERGY
#     _fillvalue_dictionary(
#         job_key=job_key, method=method, basis=basis, geom=geom, mult=mult,
#         charge=charge, orb_restricted=orb_restricted,
#         mol_options=mol_options,
#         memory=memory, comment=comment, machine_options=machine_options,
#         scf_options=scf_options, corr_options=corr_options,
#     )
#     # inp_str = template.read_and_fill(TEMPLATE_DIR, 'all.mako', fill_dct)
#     # return inp_str
#
#
# # helper functions
# def _fillvalue_dictionary(job_key, method, basis, geom, mult, charge,
#                           orb_restricted, mol_options, memory, comment,
#                           machine_options, scf_options, corr_options,
#                           job_options=(), frozen_coordinates=()):
#     assert method in par.METHODS
#     assert basis in par.BASES
#
#     molpro_scf_meth = _scf_method(mult, orb_restricted)
#     molpro_corr_meth = _correlation_method(method)
#     geom_str, _ = _geometry_strings(geom)
#     print(molpro_scf_meth)
#     print(molpro_corr_meth)
#     print(geom_str)


def _geometry_strings(geom):
    if automol.geom.is_valid(geom):
        geom_str = automol.geom.string(geom)
        zmat_val_str = ''
    elif automol.zmatrix.is_valid(geom):
        raise NotImplementedError
    else:
        raise ValueError("Invalid geometry value:\n{}".format(geom))

    return geom_str, zmat_val_str


def _scf_method(mult, orb_restricted):
    orb_restricted = (mult == 1) if orb_restricted is None else orb_restricted

    # for now, orbital restriction is really only for open-shell hartree-fock
    if orb_restricted is False and mult == 1:
        raise NotImplementedError

    reference = (par.MolproReference.RHF if orb_restricted else
                 par.MolproReference.UHF)

    return reference


def _correlation_method(method):
    if method in pclass.values(elstruct.par.Method.Corr):
        ret = par.MOLPRO_METHOD_DCT[method]
    else:
        ret = ''
    return ret


if __name__ == '__main__':
    METHOD = 'mp2'
    BASIS = 'sto-3g'
    GEOM = (('O', (0.0, 0.0, -0.110)),
            ('H', (0.0, -1.635, 0.876)),
            ('H', (-0.0, 1.635, 0.876)))
    CHARGE = 0
    MULT = 1
    # ORB_RESTRICTED = False

    # energy(
    #     method=METHOD,
    #     basis=BASIS,
    #     geom=GEOM,
    #     mult=MULT,
    #     charge=CHARGE)
    #     # orb_restricted=ORB_RESTRICTED)
