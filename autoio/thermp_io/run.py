""" Runner
"""

def run_thermp(pf_path, thermp_path,
               thermp_file_name='thermp.dat', pf_file_name='pf.dat'):
    """
    Runs thermp.exe
    Requires thermp input file to be present
    partition function (pf) output file and
    """

    # Set full paths to files
    thermp_file = os.path.join(thermp_path, thermp_file_name)
    pf_outfile = os.path.join(pf_path, pf_file_name)

    # Copy MESSPF output file to THERMP run dir and rename to pf.dat
    pf_datfile = os.path.join(thermp_path, 'pf.dat')
    try:
        shutil.copyfile(pf_outfile, pf_datfile)
    except shutil.SameFileError:
        pass

    # Check for the existance of ThermP input and PF output
    assert os.path.exists(thermp_file), 'ThermP file does not exist'
    assert os.path.exists(pf_outfile), 'PF file does not exist'

    # Run thermp
    subprocess.check_call(['thermp', thermp_file])
