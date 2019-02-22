""" test elstruct.reader.run/write pipelines
"""
import os
import tempfile
import subprocess
import elstruct
import automol


PROGRAM_TEST_COMMAND_DCT = {
    'psi4': ('psi4',)
}


def test__energy():
    """ test elstruct energy writes and reads
    """
    basis = 'sto-3g'
    geom = (('O', (0., 0., 0.)),
            ('H', (0., 2., 2.)),
            ('H', (0., 2., -2.)))
    mult = 1
    charge = 0

    for prog in elstruct.writer.programs():
        assert prog in elstruct.reader.programs()
        for method in elstruct.writer.method_list(prog):
            print(prog, method)
            inp_str = elstruct.writer.energy_input_string(
                prog=prog, method=method, basis=basis, geom=geom,
                mult=mult, charge=charge, scf_options=''
            )

            # if we have an exectuable test command, try running it
            if prog in PROGRAM_TEST_COMMAND_DCT:
                tmp_dir = tempfile.mkdtemp()
                print(tmp_dir)

                inp_file_path = os.path.join(tmp_dir, 'input.dat')
                with open(inp_file_path, 'w') as inp_file_obj:
                    inp_file_obj.write(inp_str)

                argv = list(PROGRAM_TEST_COMMAND_DCT[prog])
                subprocess.check_call(argv, cwd=tmp_dir)

                out_file_path = os.path.join(tmp_dir, 'output.dat')
                with open(out_file_path, 'r') as out_file_obj:
                    out_file_str = out_file_obj.read()

                ene = elstruct.reader.energy(prog, method, out_file_str)
                print(ene)


def test__optimization():
    """ test elstruct optimization writes and reads
    """
    basis = 'sto-3g'
    geom = (('O', (None, None, None), (None, None, None)),
            ('H', (0, None, None), (1.8, None, None)),
            ('H', (0, 1, None), (1.8, 1.75, None)))
    zmat_var_dct = {(1, 0): 'r1', (2, 0): 'r1'}
    mult = 1

    for prog in elstruct.writer.optimization_programs():
        for method in elstruct.writer.method_list(prog):
            print(prog, method)
            inp_str = elstruct.writer.optimization_input_string(
                prog=prog, method=method, basis=basis, geom=geom,
                mult=mult, scf_options='',
                zmat_var_dct=zmat_var_dct
            )

            # if we have an exectuable test command, try running it
            if prog in PROGRAM_TEST_COMMAND_DCT:
                tmp_dir = tempfile.mkdtemp()
                print(tmp_dir)

                inp_file_path = os.path.join(tmp_dir, 'input.dat')
                with open(inp_file_path, 'w') as inp_file_obj:
                    inp_file_obj.write(inp_str)

                argv = list(PROGRAM_TEST_COMMAND_DCT[prog])
                subprocess.check_call(argv, cwd=tmp_dir)

                out_file_path = os.path.join(tmp_dir, 'output.dat')
                with open(out_file_path, 'r') as out_file_obj:
                    out_file_str = out_file_obj.read()

                zmat_geom, zmat_var_dct = (
                    elstruct.reader.optimized_zmatrix_geometry(
                        prog, out_file_str))
                print(zmat_geom)
                print(zmat_var_dct)

                cart_geom = elstruct.reader.optimized_cartesian_geometry(
                    prog, out_file_str)
                print(cart_geom)

                assert automol.geom.is_valid(cart_geom)


if __name__ == '__main__':
    # test__optimization()
    test__energy()
