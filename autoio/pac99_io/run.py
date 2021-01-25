"""
"""

def run_pac(formula, nasa_path):
    """
    Run pac99 for a given species name (formula)
    https://www.grc.nasa.gov/WWW/CEAWeb/readme_pac99.htm
    requires formula+'i97' and new.groups files
    """

    # Run pac99
    # Set file names for pac99
    i97_file = os.path.join(nasa_path, formula + '.i97')
    newgroups_file = os.path.join(nasa_path, 'new.groups')
    newgroups_ref = os.path.join(CUR_PATH, 'new.groups')

    # Copy new.groups file from thermo src dir to run dir
    shutil.copyfile(newgroups_ref, newgroups_file)

    # Check for the existance of pac99 files
    assert os.path.exists(i97_file)
    assert os.path.exists(newgroups_file)

    # Run pac99
    proc = subprocess.Popen('pac99', stdin=subprocess.PIPE)
    proc.communicate(bytes(formula, 'utf-8'))

    # Check to see if pac99 does not have error message
    with open(os.path.join(nasa_path, formula+'.o97'), 'r') as pac99_file:
        pac99_out_str = pac99_file.read()
    if 'INSUFFICIENT DATA' in pac99_out_str:
        print('*ERROR: PAC99 fit failed, maybe increase temperature ranges?')
        sys.exit()
    else:
        # Read the pac99 polynomial
        with open(os.path.join(nasa_path, formula+'.c97'), 'r') as pac99_file:
            pac99_str = pac99_file.read()
        if not pac99_str:
            print('No polynomial produced from PAC99 fits, check for errors')
            sys.exit()


def thermo_paths(spc_dct_i, run_prefix, idx):
    """ Set up the path for saving the pf input and output.
        Placed in a MESSPF, NASA dirs high in run filesys.
    """

    # Get the formula and inchi key
    spc_info = mechanalyzer.inf.spc.from_dct(spc_dct_i)
    spc_formula = automol.inchi.formula_string(spc_info[0])
    ich_key = automol.inchi.inchi_key(spc_info[0])
    print(spc_info[0])

    # PF
    bld_locs = ['PF', idx]
    bld_save_fs = autofile.fs.build(run_prefix)
    bld_save_fs[-1].create(bld_locs)
    bld_path = bld_save_fs[-1].path(bld_locs)
    print(bld_path, spc_formula, ich_key)
    spc_pf_path = os.path.join(bld_path, spc_formula, ich_key)

    # NASA polynomials
    bld_locs = ['NASA', idx]
    bld_save_fs = autofile.fs.build(run_prefix)
    bld_save_fs[-1].create(bld_locs)
    bld_path = bld_save_fs[-1].path(bld_locs)
    spc_nasa_path = os.path.join(bld_path, spc_formula, ich_key)

    return spc_pf_path, spc_nasa_path

