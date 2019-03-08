""" test elstruct writer/run/reader pipelines
"""
import tempfile
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

            # for programs with no run test, at lest make sure we can generate
            # an input file
            _ = elstruct.writer.energy(
                prog, method, basis, geom,
                mult, charge, scf_options=(),
            )

            # if we have a run script, try running it
            if prog in SCRIPT_STR_DCT:
                script_str = SCRIPT_STR_DCT[prog]
                run_dir = tempfile.mkdtemp()
                _, out_str = elstruct.run.direct(
                    script_str, run_dir, elstruct.writer.energy,
                    prog, method, basis, geom, mult, charge
                )

                assert elstruct.reader.has_normal_exit_message(prog, out_str)

                ene = elstruct.reader.energy(prog, method, out_str)

                print(run_dir)
                print(ene)

                # also check that the convergence error shows up on a failure
                assert not elstruct.reader.has_error_message(
                    prog, elstruct.ERROR.SCF_NOCONV, out_str)

                run_dir = tempfile.mkdtemp()
                with pytest.warns(UserWarning):
                    _, out_str = elstruct.run.direct(
                        script_str, run_dir, elstruct.writer.energy,
                        prog, method, basis, geom, mult, charge,
                        scf_options=(
                            'set scf maxiter 2',
                        )
                    )

                assert not elstruct.reader.has_normal_exit_message(
                    prog, out_str)
                assert elstruct.reader.has_error_message(
                    prog, elstruct.ERROR.SCF_NOCONV, out_str)


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

            # for programs with no run test, at lest make sure we can generate
            # an input file
            _ = elstruct.writer.gradient(
                prog, method, basis, geom,
                mult, charge, scf_options=(),
            )

            # if we have a run script, try running it
            if prog in SCRIPT_STR_DCT:
                script_str = SCRIPT_STR_DCT[prog]
                run_dir = tempfile.mkdtemp()
                _, out_str = elstruct.run.direct(
                    script_str, run_dir, elstruct.writer.gradient,
                    prog, method, basis, geom, mult, charge
                )

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

            # for programs with no run test, at lest make sure we can generate
            # an input file
            _ = elstruct.writer.hessian(
                prog, method, basis, geom, mult, charge
            )

            # if we have a run script, try running it
            if prog in SCRIPT_STR_DCT:
                script_str = SCRIPT_STR_DCT[prog]
                run_dir = tempfile.mkdtemp()
                _, out_str = elstruct.run.direct(
                    script_str, run_dir, elstruct.writer.hessian,
                    prog, method, basis, geom, mult, charge
                )

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
            print()
            print(prog, method)

            # for programs with no run test, at lest make sure we can generate
            # an input file
            _ = elstruct.writer.optimization(
                prog, method, basis, geom, mult, charge, opt_options=(),
            )

            # if we have a run script, try running it
            if prog in SCRIPT_STR_DCT:
                script_str = SCRIPT_STR_DCT[prog]
                run_dir = tempfile.mkdtemp()
                _, out_str = elstruct.run.direct(
                    script_str, run_dir, elstruct.writer.optimization,
                    prog, method, basis, geom, mult, charge, opt_options=()
                )

                assert elstruct.reader.has_normal_exit_message(prog, out_str)

                ene = elstruct.reader.energy(prog, method, out_str)
                zma = elstruct.reader.opt_zmatrix(prog, out_str)
                geo = elstruct.reader.opt_geometry(prog, out_str)

                print(run_dir)
                print(ene)
                print(zma)
                print(geo)

                # also check that the convergence error shows up on a failure
                assert not elstruct.reader.has_error_message(
                    prog, elstruct.ERROR.OPT_NOCONV, out_str)

                with pytest.warns(UserWarning):
                    run_dir = tempfile.mkdtemp()
                    _, out_str = elstruct.run.direct(
                        script_str, run_dir, elstruct.writer.optimization,
                        prog, method, basis, geom, mult, charge,
                        opt_options=(
                            'set geom_maxiter 2',
                        )
                    )

                print(run_dir)
                assert not elstruct.reader.has_normal_exit_message(
                    prog, out_str)
                assert elstruct.reader.has_error_message(
                    prog, elstruct.ERROR.OPT_NOCONV, out_str)


def test__run__robust():
    """ test elstruct.run.robust
    """
    input_writer = elstruct.writer.optimization
    method = 'rhf'
    basis = 'sto-3g'
    geom = ((('O', (None, None, None), (None, None, None)),
             ('H', (0, None, None), ('R1', None, None)),
             ('H', (0, 1, None), ('R2', 'A2', None))),
            {'R1': 1.83114, 'R2': 1.83115, 'A2': 1.81475845})
    mult = 1
    charge = 0
    kwargs = {'comment': '<testing comment line>',
              'scf_options': ('set scf diis false', 'set scf maxiter 15'),
              'opt_options': ('set geom_maxiter 10',)}
    errors = [
        elstruct.ERROR.SCF_NOCONV,
        elstruct.ERROR.OPT_NOCONV,
    ]
    options_mat = [
        [{elstruct.OPTION.SCF.KEY: ('set scf guess huckel',)},
         {elstruct.OPTION.SCF.KEY: ('set scf guess gwh',)},
         {elstruct.OPTION.SCF.KEY: ('set scf diis true',
                                    'set scf guess sad',)}],
        [{elstruct.OPTION.OPT.KEY: ('set opt_coordinates cartesian',)},
         {elstruct.OPTION.OPT.KEY: ('set opt_coordinates internal',)}]
    ]

    for prog in elstruct.writer.optimization_programs():
        if prog in SCRIPT_STR_DCT:
            script_str = SCRIPT_STR_DCT[prog]
            run_dir = tempfile.mkdtemp()
            _, out_str = elstruct.run.robust(
                script_str, run_dir, input_writer,
                prog, method, basis, geom, mult, charge,
                errors=errors, options_mat=options_mat, **kwargs
            )

            assert elstruct.reader.has_normal_exit_message(prog, out_str)

            ene = elstruct.reader.energy(prog, method, out_str)
            zma = elstruct.reader.opt_zmatrix(prog, out_str)
            print(run_dir)
            print(ene)
            print(zma)


if __name__ == '__main__':
    # test__energy()
    # test__energy()
    # test__gradient()
    # test__hessian()
    # test__optimization()
    test__run__robust()
