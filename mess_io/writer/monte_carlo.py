"""
Writes MESS input for a monte carlo partition function calculation
"""

import os
from mess_io.writer import util
from ioformat import build_mako_str
from ioformat import remove_trail_whitespace
from ioformat import indent


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')
SECTION_PATH = os.path.join(TEMPLATE_PATH, 'sections')
MONTE_CARLO_PATH = os.path.join(SECTION_PATH, 'monte_carlo')


def mc_species(geom, sym_factor, elec_levels,
               flux_mode_str, data_file_name,
               ground_energy, reference_energy=None,
               freqs=(), use_cm_shift=False):
    """ Writes a monte carlo species section

        :param core: `MonteCarlo` section string in MESS format
        :type core: str
        :param sym_factor: symmetry factor of species
        :type sym_factor: float
        :param elec_levels: energy and degeneracy of atom's electronic states
        :type elec_levels: list(float)
        :param flux_mode_str: MESS-format `FluxionalMode` sections for rotors
        :type flux_mode_str: str
        :param data_file_name: Name of data file w/ enes, geos, grads, hessians 
        :type data_file_name: str
        :param ground_energy: energy relative to reference (kcal.mol-1)
        :type ground_energy: float
        :param freqs: vibrational frequencies (cm-1)
        :type freqs: list(float)
        :param use_cm_chift: signal to include a CM shift
        :type use_cm_shift: bool
        :rtype: str
    """

    # Format the molecule specification section
    atom_list = util.molec_spec_format(geom)

    # Build a formatted frequencies and elec levels string
    nlevels, levels = util.elec_levels_format(elec_levels)
    levels = indent(levels, 2)
    if freqs:
        nfreqs, freqs = util.freqs_format(freqs)
        no_qc_corr = True
    else:
        nfreqs = 0

    # Indent various strings string if needed
    flux_mode_str = util.indent(flux_mode_str, 4)

    # Create dictionary to fill template
    monte_carlo_keys = {
        'atom_list': atom_list,
        'sym_factor': sym_factor,
        'flux_mode_str': flux_mode_str,
        'data_file_name': data_file_name,
        'reference_energy': reference_energy,
        'ground_energy': ground_energy,
        'nlevels': nlevels,
        'levels': levels,
        'nfreqs': nfreqs,
        'freqs': freqs,
        'use_cm_shift': use_cm_shift
    }

    return build_mako_str(
        template_file_name='monte_carlo.mako',
        template_src_path=MONTE_CARLO_PATH,
        template_keys=monte_carlo_keys)


def mc_data(geos, enes, grads=(), hessians=()):
    """ Writes the string for an auxliary data file required for
        Monte Carlo calculations in MESS that contains the
        geometries, energies, gradients, and Hessians obtained
        from Monte Carlo sampling of the fluxional modes.

        :param geos: geometries from sampling
        :type geos: list
        :param enes: energies from energies
        :type enes: list(float)
        :param grads: gradients from sampling
        :type grads: list
        :param hessians: Hessians from sampling
        :type hessians: list
        :rtype: str
    """

    if not grads and not hessians:
        assert len(geos) == len(enes)
    elif grads or hessians:
        assert grads and hessians
        assert len(geos) == len(enes) == len(grads) == len(hessians)

    dat_str = ''
    for idx, _ in enumerate(geos):
        # Set the sampling point index
        idx_str = str(idx+1)
        # Build string with data for all points
        dat_str += 'Sampling point'+idx_str+'\n'
        dat_str += 'Energy'+'\n'
        dat_str += enes[idx]+'\n'
        geo_str = 'Geometry'+'\n'
        geo_str += geos[idx]+'\n'
         geo_str = remove_trail_whitespace(geo_str)
        dat_str += geo_str
        if grads:
            dat_str += 'Gradient'+'\n'
            dat_str += grads[idx]
        if hessians:
            dat_str += 'Hessian'+'\n'
            dat_str += hessians[idx]+'\n'

    # Format string as needed
    if not grads and not hessians:
        dat_str = remove_trail_whitespace(dat_str)

    # if not grads and not hessians:
    dat_str = '\n' + dat_str

    return dat_str

 
def fluxional_mode(atom_indices, span=360.0):
    """ Writes the string that defines the `FluxionalMode` section for a
        single fluxional mode (torsion) of a species for a MESS input file by
        formatting input information into strings a filling Mako template.

        :param atom_idxs: idxs of atoms involved in fluxional mode
        :type atom_indices: list(int)
        :param span: range from 0.0 to value that mode was sampled over (deg.)
        :type span: float
        :rtype: str
    """

    # Format the aotm indices string
     atom_indices = util.format_flux_mode_indices(atom_indices)

    # Create dictionary to fill template
    flux_mode_keys = {
        'atom_indices': atom_indices,
        'span': span,
    }

    return build_mako_str(
        template_file_name='fluxional_mode.mako',
        template_src_path=MONTE_CARLO_PATH,
        template_keys=flux_mode_keys)
