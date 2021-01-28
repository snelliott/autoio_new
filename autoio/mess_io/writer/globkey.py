"""
Writes the full sections of a MESS input file
"""

import os
from ioformat import build_mako_str
from ioformat import indent
from ioformat import remove_trail_whitespace
from mess_io.writer._sec import rxnchan_header_str
from mess_io.writer.mol_data import core_rigidrotor
from mess_io.writer.spc import molecule
from mess_io.writer.rxnchan import species
from phydat import phycon


# OBTAIN THE PATH TO THE DIRECTORY CONTAINING THE TEMPLATES #
SRC_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(SRC_PATH, 'templates')
SECTION_PATH = os.path.join(TEMPLATE_PATH, 'sections')


# Write the full input file strings
def messrates_inp_str(globkey_str, energy_trans_str, rxn_chan_str):
    """ Combine various MESS strings together to combined MESS rates
    """

    rxn_chan_header_str = rxnchan_header_str()
    mess_inp_str = '\n'.join(
        [globkey_str,
         '!',
         '!',
         # '! == MESS MODEL ==',
         'Model',
         '!',
         energy_trans_str,
         rxn_chan_header_str,
         rxn_chan_str,
         '\nEnd\n']
    )
    mess_inp_str = remove_trail_whitespace(mess_inp_str)

    return mess_inp_str


def messpf_inp_str(globkey_str, spc_str):
    """ Combine various MESS strings together to combined MESSPF
    """
    return '\n'.join([globkey_str, spc_str]) + '\n'
    

def messhr_inp_str(geo, hind_rot_str):
    """ Special MESS input string to calculate frequencies and ZPVEs
        for hindered rotors
    """

    global_pf_str = global_pf(
        temperatures=[100.0, 200.0, 300.0, 400.0, 500],
        rel_temp_inc=0.001,
        atom_dist_min=0.6)
    dat_str = molecule(
        core=mess_io.writer.core_rigidrotor(tors_geo, 1.0),
        freqs=[1000.0],
        elec_levels=[[0.0, 1.0]],
        hind_rot=hind_rot_str,
    )
    spc_str = species(
        spc_label='Tmp',
        spc_data=dat_str,
        zero_energy=0.0
    )

    return messpf_inp_str(globkey_str, spc_str)


def messhr_inp_str(geo, hind_rot_str):
    """ Special MESS input string to calculate frequencies and ZPVEs
        for hindered rotors
    """

    global_pf_str = global_pf(
        temperatures=[100.0, 200.0, 300.0, 400.0, 500],
        rel_temp_inc=0.001,
        atom_dist_min=0.6)
    dat_str = molecule(
        core=core_rigidrotor(geo, 1.0),
        freqs=[1000.0],
        elec_levels=[[0.0, 1.0]],
        hind_rot=hind_rot_str,
    )
    spc_str = species(
        spc_label='Tmp',
        spc_data=dat_str,
        zero_ene=0.0
    )

    return messpf_inp_str(global_pf_str, spc_str)


# Write individual sections of the input file
def global_reaction(temperatures, pressures,
                    excess_ene_temp=None, well_extend=None):
    """ Writes the global keywords section of the MESS input file by
        formatting input information into strings a filling Mako template.

        :param temperatures: List of temperatures (in K)
        :type temperatures: float
        :param pressures: List of pressures (in atm)
        :type pressures: float
        :return global_str: String for section
        :rtype: string
    """

    # Format temperature and pressure lists
    temperature_list = '  '.join(str(val) for val in temperatures)
    pressure_list = '  '.join(str(val) for val in pressures)

    # Format the other keywords as needed
    if excess_ene_temp is not None:
        assert isinstance(excess_ene_temp, float), (
            'ExcessEnergyOverTemperature value must be a float'
        )
        excess_ene_temp_str = '{0:.2f}'.format(excess_ene_temp)
    else:
        excess_ene_temp_str = None
    if well_extend is not None:
        assert isinstance(well_extend, float), (
            'WellExtension value must be a float'
        )
        well_extend_str = '{0:.2f}'.format(well_extend)
    else:
        well_extend_str = None

    # Create dictionary to fill template
    globrxn_keys = {
        'temperatures': temperature_list,
        'pressures': pressure_list,
        'excess_ene_temp': excess_ene_temp_str,
        'well_extend': well_extend_str,
    }

    return build_mako_str(
        template_file_name='global_reaction.mako',
        template_src_path=SECTION_PATH,
        template_keys=globrxn_keys)


def global_pf(temperatures=(),
              temp_step=100, ntemps=30,
              rel_temp_inc=0.001, atom_dist_min=1.13384):
    """ Writes the global keywords section of the MESS input file by
        formatting input information into strings a filling Mako template.

        :param temperatures: List of temperatures (in K)
        :type temperatures: list(float)
        :param temp_step: temperature step (in K)
        :type temp_step: float
        :param ntemps: number of temperature values on grid
        :type ntemps: int
        :param rel_temp_inc: increment for temps
        :type rel_temp_inc: float
        :param atom_dist_min: cutoff for atom distances (Bohr)
        :type atom_dist_min: float
        :return global_pf_str: string for section
        :rtype: string
    """

    if temperatures:
        temperature_list = '  '.join(str(val) for val in temperatures)
        temp_step = None
        ntemps = None
    else:
        temperature_list = ''

    # Convert the atom distance minimum
    atom_dist_min = '{0:.2f}'.format(atom_dist_min * phycon.BOHR2ANG)

    # Create dictionary to fill template
    globpf_keys = {
        'temperatures': temperature_list,
        'temp_step': temp_step,
        'ntemps': ntemps,
        'rel_temp_inc': rel_temp_inc,
        'atom_dist_min': atom_dist_min
    }

    return build_mako_str(
        template_file_name='global_pf.mako',
        template_src_path=SECTION_PATH,
        template_keys=globpf_keys)


def global_energy_transfer(edown_str, collid_freq_str):
    """ Writes the global energy transfer section of the MESS input file by
        formatting input information into strings a filling Mako template.

        :param edown_str: String for the energy down parameters
        :type edown_str: str
        :param collid_freq_str: String for the collisional freq parameters
        :type collid_freq_str: str
        :rtype: str
    """

    edown_str = indent(edown_str, 2)
    collid_freq_str = indent(collid_freq_str, 2)

    # Create dictionary to fill template
    glob_etrans_keys = {
        'edown_str': edown_str,
        'collid_freq_str': collid_freq_str
    }

    return build_mako_str(
        template_file_name='global_etrans.mako',
        template_src_path=SECTION_PATH,
        template_keys=glob_etrans_keys)
