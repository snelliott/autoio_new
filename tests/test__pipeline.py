""" test elstruct writer/run/reader pipelines
"""
import pytest
import elstruct


SCRIPT_STR_DCT = {
    'psi4': "#!/usr/bin/env bash\npsi4 >> stdout.log &> stderr.log"
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
            print()
            print(prog, method)
            inp_str = elstruct.writer.energy(
                prog=prog, method=method, basis=basis, geom=geom,
                mult=mult, charge=charge, scf_options=(),
            )

            # if we have a run script, try running it
            if prog in SCRIPT_STR_DCT:
                out_str = elstruct.run(SCRIPT_STR_DCT[prog], inp_str)

                assert elstruct.reader.has_normal_exit_message(
                    prog, out_str)

                ene = elstruct.reader.energy(prog, method, out_str)

                print(ene)

                # also check that the convergence error shows up on a failure
                assert not elstruct.reader.has_scf_nonconvergence_message(
                    prog, out_str)
                inp_str = elstruct.writer.energy(
                    prog=prog, method=method, basis=basis, geom=geom,
                    mult=mult, charge=charge, scf_options=(
                        'set scf maxiter 2',
                    ),
                )

                with pytest.warns(UserWarning):
                    out_str = elstruct.run(SCRIPT_STR_DCT[prog], inp_str)

                assert not elstruct.reader.has_normal_exit_message(
                    prog, out_str)
                assert elstruct.reader.has_scf_nonconvergence_message(
                    prog, out_str)


def test__gradient():
    """ test elstruct gradient writes and reads
    """
    basis = 'sto-3g'
    geom = (('O', (0., 0., 0.)),
            ('H', (0., 2., 2.)),
            ('H', (0., 2., -2.)))
    mult = 1
    charge = 0

    for prog in elstruct.writer.gradient_programs():
        assert prog in elstruct.reader.gradient_programs()
        for method in elstruct.writer.method_list(prog):
            print()
            print(prog, method)
            inp_str = elstruct.writer.gradient(
                prog=prog, method=method, basis=basis, geom=geom,
                mult=mult, charge=charge, scf_options=()
            )

            # if we have a run script, try running it
            if prog in SCRIPT_STR_DCT:
                out_str, tmp_dir = elstruct.run(SCRIPT_STR_DCT[prog], inp_str,
                                                return_path=True)

                print(tmp_dir)
                assert elstruct.reader.has_normal_exit_message(prog, out_str)

                ene = elstruct.reader.energy(prog, method, out_str)
                grad = elstruct.reader.gradient(prog, out_str)

                print(ene)
                print(grad)


def test__hessian():
    """ test elstruct hessian writes and reads
    """
    basis = 'sto-3g'
    geom = (('O', (0., 0., 0.)),
            ('H', (0., 2., 2.)),
            ('H', (0., 2., -2.)))
    mult = 1
    charge = 0

    for prog in elstruct.writer.hessian_programs():
        for method in elstruct.writer.method_list(prog):
            print()
            print(prog, method)
            inp_str = elstruct.writer.hessian(
                prog=prog, method=method, basis=basis, geom=geom,
                mult=mult, charge=charge, scf_options=(),
            )

            # if we have a run script, try running it
            if prog in SCRIPT_STR_DCT:
                out_str, tmp_dir = elstruct.run(SCRIPT_STR_DCT[prog], inp_str,
                                                return_path=True)

                print(tmp_dir)
                assert elstruct.reader.has_normal_exit_message(prog, out_str)

                ene = elstruct.reader.energy(prog, method, out_str)
                grad = elstruct.reader.gradient(prog, out_str)
                hess = elstruct.reader.hessian(prog, out_str)

                print(ene)
                print(grad)
                print(hess)


def test__optimization():
    """ test elstruct optimization writes and reads
    """
    basis = 'sto-3g'
    geom = ((('O', (None, None, None), (None, None, None)),
             ('H', (0, None, None), ('R1', None, None)),
             ('H', (0, 1, None), ('R2', 'A2', None))),
            {'R1': 1.83114, 'R2': 1.83115, 'A2': 1.81475845})
    mult = 1
    charge = 0

    for prog in elstruct.writer.optimization_programs():
        for method in elstruct.writer.method_list(prog):
            print(prog, method)
            inp_str = elstruct.writer.optimization(
                prog=prog, method=method, basis=basis, geom=geom,
                mult=mult, charge=charge, scf_options=(),
            )

            # if we have a run script, try running it
            if prog in SCRIPT_STR_DCT:
                out_str, tmp_dir = elstruct.run(SCRIPT_STR_DCT[prog], inp_str,
                                                return_path=True)

                assert elstruct.reader.has_normal_exit_message(prog, out_str)

                ene = elstruct.reader.energy(prog, method, out_str)

                zma = elstruct.reader.opt_zmatrix(prog, out_str)

                geo = elstruct.reader.opt_geometry(prog, out_str)

                print(tmp_dir)
                print(ene)
                print(zma)
                print(geo)

                # also check that the convergence error shows up on a failure
                assert not elstruct.reader.has_opt_nonconvergence_message(
                    prog, out_str)
                inp_str = elstruct.writer.optimization(
                    prog=prog, method=method, basis=basis, geom=geom,
                    mult=mult, charge=charge, opt_options=(
                        'set geom_maxiter 2',
                    ),
                )

                with pytest.warns(UserWarning):
                    out_str, tmp_dir = elstruct.run(SCRIPT_STR_DCT[prog],
                                                    inp_str, return_path=True)

                print(tmp_dir)
                assert not elstruct.reader.has_normal_exit_message(
                    prog, out_str)
                assert elstruct.reader.has_opt_nonconvergence_message(
                    prog, out_str)


if __name__ == '__main__':
    # test__gradient()
    # test__hessian()
    # test__energy()
    test__optimization()
