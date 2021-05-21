""" Read the merged wells from the auxiliary file
"""

def merged_wells(mess_aux_str):
    """ Parse the auxiliary MESS output file string for all of the groups
        of wells which merged from a Master Equation simulation.

        :param mess_aux_str: string for the auxiliary file
        :type mess_aux_str: str
        :rtype: tuple(tuple(str))
    """

    # Get the lines
    mess_lines = mess_aux_str.splitlines()

    # Read the block of text that has all of the species
    merge_well_lines = []
    for i, line in enumerate(mess_lines):
        if 'number of species =' in line:
            merge_well_lines.append(mess_lines[i+1])

    # Parse the merged wells
    merged_well_lst = ()
    for line in merge_well_lines:
        merged_well_lst += (tuple(line.strip().split()),)

    return merged_well_lst
