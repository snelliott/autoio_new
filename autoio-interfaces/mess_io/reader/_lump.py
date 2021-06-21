""" Read the merged wells from the auxiliary file
"""

import numpy
from phydat import phycon


def merged_wells(mess_aux_str, pressure, temp):
    """ Parse the auxiliary MESS output file string for all of the groups
        of wells which merged from a Master Equation simulation.

        :param mess_aux_str: string for the auxiliary file
        :type mess_aux_str: str
        :rtype: tuple(tuple(str))
    """

    # Get the lines
    mess_lines = mess_aux_str.splitlines()

    # Parses number of wells and lines they appear on for second loop
    # Done for each set of wells at each T and P
    merged_well_lines = []
    for i, line in enumerate(mess_lines):
        if 'number of species =' in line:
            cond_line = mess_lines[i-1].strip().split()
            well_pressure = float(cond_line[2]) * phycon.BAR2ATM
            well_temp = float(cond_line[-2])
            if (numpy.isclose(pressure, well_pressure) and
               numpy.isclose(temp, well_temp)):
                nspc = int(line.strip().split()[-1])
                merged_well_lines.append((nspc, i))

    # Find all the lines in the block to grab the wells
    merged_well_lst = ()
    for nspc, line_idx in merged_well_lines:
        for idx in range(nspc):
            well_line = mess_lines[line_idx+1+idx*2]
            well_names = well_line.strip().split()
            if len(well_names) > 1:
                merged_well_lst += (tuple(well_names),)

    return merged_well_lst
