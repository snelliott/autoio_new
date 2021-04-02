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
         '\nEnd  ! Mod2\n']
    )
    mess_inp_str = remove_trail_whitespace(mess_inp_str)

    return mess_inp_str


def messpf_inp_str(globkey_str, spc_str):
    """ Combine various MESS strings together to combined MESSPF
    """
    return '\n'.join([globkey_str, spc_str]) + '\n'


# Write individual sections of the input file
def global_reaction(temperatures, pressures,
                    excess_ene_temp=None, well_extend='auto'):
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
        if well_extend != 'auto':
            assert isinstance(well_extend, float), (
                'WellExtension value must be a float'
            )
            well_extend_str = '{0:.2f}'.format(well_extend)
        else:
            well_extend_str = ''
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


# Write data to output file formats if you want to make a formatted output file
def pf_output(formula_str, temps, logq, dq_dt, d2q_dt2):
    """ Writes partition function data into a string that is formatted like the
        output file 
    """

    mess_out_str = 'Natural log of the partition function '
    mess_out_str += 'and its derivatives:\n'
    mess_out_str += ' T, K            {}'.format(formula_str)
    for temp, _logq, dq1, dq2 in zip(temps, logq, dq_dt, d2q_dt2):
        mess_out_str += '\n'
        mess_out_str += '{0:>8.6f}    '.format(temp)
        mess_out_str += '{0:>8.6f}    '.format(_logq)
        mess_out_str += '{0:>8.6f}    '.format(dq1)
        mess_out_str += '{0:>8.6f}    '.format(dq2)

    return mess_out_str
