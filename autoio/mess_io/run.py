"""
"""

def direct():
    """
    """

    # Write the MESS file
    if not os.path.exists(mess_path):
        os.makedirs(mess_path)
    print('\n\nWriting MESS input file...')
    print(' - Path: {}'.format(mess_path))
    with open(os.path.join(mess_path, filename), 'w') as mess_file:
        mess_file.write(mess_inp_str)

    # Write all of the data files needed
    if dat_str_dct:
        print('Writing the MESS data files...')
    for fname, fstring in dat_str_dct.items():
        # dat_path = os.path.join(mess_path, fname)
        if fstring:
            data_file_path = os.path.join(mess_path, fname)
            print(' - Writing file: {}'.format(data_file_path))
            with open(data_file_path, 'w') as file_obj:
                file_obj.write(fstring)
    # print(' - WARNING: File will be overwriten.')
    # print('No additional MESS input file will be written.')


def mess_tors_zpes(tors_geo, hind_rot_str, tors_save_path,
                   script_str=DEFAULT_SCRIPT_DCT['messpf']):
    """ Calculate the frequencies and ZPVES of the hindered rotors
        create a messpf input and run messpf to get tors_freqs and tors_zpes
    """

    # Set up the filesys
    bld_fs, bld_locs = filesys.build.build_fs(
        tors_save_path, 'PF', locs_idx=None)
    bld_fs[-1].create(bld_locs)
    pf_path = bld_fs[-1].path(bld_locs)

    pf_path = os.path.join(pf_path, str(random.randint(0,12345678)))
    if not os.path.exists(pf_path):
        os.mkdir(pf_path)

    print('Run path for MESSPF:')
    print(pf_path)

    # Write the MESSPF input file
    global_pf_str = mess_io.writer.global_pf(
        temperatures=[100.0, 200.0, 300.0, 400.0, 500],
        rel_temp_inc=0.001,
        atom_dist_min=0.6)
    dat_str = mess_io.writer.molecule(
        core=mess_io.writer.core_rigidrotor(tors_geo, 1.0),
        freqs=[1000.0],
        elec_levels=[[0.0, 1.0]],
        hind_rot=hind_rot_str,
    )
    spc_str = mess_io.writer.species(
        spc_label='Tmp',
        spc_data=dat_str,
        zero_energy=0.0
    )
    pf_inp_str = '\n'.join([global_pf_str, spc_str]) + '\n'

    with open(os.path.join(pf_path, 'pf.inp'), 'w') as pf_file:
        pf_file.write(pf_inp_str)

    # Run MESSPF
    run_script(script_str, pf_path)

    # Obtain the torsional zpes and freqs from the MESS output
    with open(os.path.join(pf_path, 'pf.log'), 'r') as mess_file:
        output_string = mess_file.read()

    tors_zpes = mess_io.reader.tors.zpves(output_string)
    # tors_freqs = mess_io.reader.tors.freqs(output_string)
    tors_freqs = mess_io.reader.grid_min_freqs(output_string)

    return tors_zpes, tors_freqs
