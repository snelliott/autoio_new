""" test elstruct.writer
"""
import os
import tempfile
import subprocess
from elstruct import writer


PROGRAM_TEST_COMMAND_DCT = {
    'psi4': ('psi4',)
}


def test__programs():
    """ test writer.programs
    """
    assert writer.programs() == ('psi4',)


def test__energy_programs():
    """ test writer.energy_programs
    """
    assert writer.energy_programs() == ('psi4',)


def test__method_list():
    """ test writer.method_list
    """
    for prog in writer.energy_programs():
        methods = writer.method_list(prog)
        assert methods  # make sure it isn't empty
        print((prog, methods))


def test__basis_list():
    """ test writer.basis_list
    """
    for prog in writer.energy_programs():
        bases = writer.basis_list(prog)
        assert bases  # make sure it isn't empty
        print((prog, bases))


def test__energy_input_string():
    """ test elstruct energy writers
    """
    basis = 'sto-3g'
    geom = (('O', (0., 0., 0.)),
            ('H', (0., 2., 2.)),
            ('H', (0., 2., -2.)))
    mult = 1

    for prog in writer.energy_programs():
        for method in writer.method_list(prog):
            print(prog, method)
            inp_str = writer.energy_input_string(
                prog=prog, method=method, basis=basis, geom=geom,
                mult=mult, scf_options=''
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


if __name__ == '__main__':
    # test__programs()
    # test__method_list()
    # test__basis_list()
    test__energy_input_string()
