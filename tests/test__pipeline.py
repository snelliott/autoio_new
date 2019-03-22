""" test elstruct writer/run/reader pipelines
"""
import tempfile
import pytest
import numpy
import automol
import elstruct


SCRIPT_DCT = {
    'psi4': "#!/usr/bin/env bash\n"
            "psi4 -i run.inp -o run.out >> stdout.log &> stderr.log",
}


def test__energy():
    """ test the energy pipeline
    """
    basis = 'sto-3g'
    geom = (('O', (0.0, 0.0, -0.110)),
            ('H', (0.0, -1.635, 0.876)),
            ('H', (-0.0, 1.635, 0.876)))
    mult_vals = [1, 2]
    charge_vals = [0, 1]

    for prog in elstruct.writer.programs():
        for method in elstruct.writer.method_list(prog):
            for mult, charge in zip(mult_vals, charge_vals):
                if (mult != 1 and method not in
                        elstruct.pclass.values(elstruct.par.Method.Dft)):
                    orb_restricted_vals = [False, True]
                else:
                    orb_restricted_vals = [True] if mult == 1 else [False]

                for orb_restricted in orb_restricted_vals:
                    vals = _test_pipeline(
                        script_str=SCRIPT_DCT[prog],
                        prog=prog,
                        method=method,
                        writer=elstruct.writer.energy,
                        readers=(
                            elstruct.reader.energy_(prog, method,
                                                    orb_restricted),
                        ),
                        args=(basis, geom, mult, charge, orb_restricted),
                        kwargs={},
                        error=elstruct.Error.SCF_NOCONV,
                        error_kwargs={'scf_options': [
                            elstruct.option.specify(
                                elstruct.Option.Scf.MAXITER_, 2)
                        ]},
                    )
                    print(vals)


def test__gradient():
    """ test the gradient pipeline
    """
    basis = 'sto-3g'
    geom = (('O', (0.0, 0.0, -0.110)),
            ('H', (0.0, -1.635, 0.876)),
            ('H', (-0.0, 1.635, 0.876)))
    mult_vals = [1, 2]
    charge_vals = [0, 1]

    for prog in elstruct.writer.programs():
        for method in elstruct.writer.method_list(prog):
            for mult, charge in zip(mult_vals, charge_vals):
                if (mult != 1 and method not in
                        elstruct.pclass.values(elstruct.par.Method.Dft)):
                    orb_restricted_vals = [False, True]
                else:
                    orb_restricted_vals = [True] if mult == 1 else [False]

                for orb_restricted in orb_restricted_vals:
                    vals = _test_pipeline(
                        script_str=SCRIPT_DCT[prog],
                        prog=prog,
                        method=method,
                        writer=elstruct.writer.gradient,
                        readers=(
                            elstruct.reader.energy_(prog, method,
                                                    orb_restricted),
                            elstruct.reader.gradient_(prog),
                        ),
                        args=(basis, geom, mult, charge, orb_restricted),
                        kwargs={},
                    )
                    print(vals)


def test__hessian():
    """ test the hessian pipeline
    """
    basis = 'sto-3g'
    geom = (('O', (0.0, 0.0, -0.110)),
            ('H', (0.0, -1.635, 0.876)),
            ('H', (-0.0, 1.635, 0.876)))
    mult_vals = [1, 2]
    charge_vals = [0, 1]

    for prog in elstruct.writer.programs():
        for method in elstruct.writer.method_list(prog):
            for mult, charge in zip(mult_vals, charge_vals):
                if (mult != 1 and method not in
                        elstruct.pclass.values(elstruct.par.Method.Dft)):
                    orb_restricted_vals = [False, True]
                else:
                    orb_restricted_vals = [True] if mult == 1 else [False]

                for orb_restricted in orb_restricted_vals:
                    vals = _test_pipeline(
                        script_str=SCRIPT_DCT[prog],
                        prog=prog,
                        method=method,
                        writer=elstruct.writer.hessian,
                        readers=(
                            elstruct.reader.energy_(prog, method,
                                                    orb_restricted),
                            elstruct.reader.hessian_(prog),
                        ),
                        args=(basis, geom, mult, charge, orb_restricted),
                        kwargs={},
                    )
                    print(vals)


def test__optimization():
    """ test elstruct optimization writes and reads
    """
    method = 'hf'
    basis = 'sto-3g'
    geom = ((('O', (None, None, None), (None, None, None)),
             ('O', (0, None, None), ('R1', None, None)),
             ('H', (0, 1, None), ('R2', 'A2', None)),
             ('H', (1, 0, 2), ('R2', 'A2', 'D3'))),
            {'R1': 2.74776, 'R2': 1.84451, 'A2': 1.68900, 'D3': 2.25788})
    mult = 1
    charge = 0
    orb_restricted = True
    frozen_coordinates = ('R2', 'A2', 'D3',)
    ref_frozen_values = (1.84451, 1.68900, 2.25788,)
    for prog in elstruct.writer.optimization_programs():
        for method in elstruct.writer.method_list(prog):
            vals = _test_pipeline(
                script_str=SCRIPT_DCT[prog],
                prog=prog,
                method=method,
                writer=elstruct.writer.optimization,
                readers=(elstruct.reader.energy_(prog, method,
                                                 orb_restricted),
                         elstruct.reader.opt_zmatrix_(prog),
                         elstruct.reader.opt_geometry_(prog),),
                args=(basis, geom, mult, charge, orb_restricted),
                kwargs={'frozen_coordinates': frozen_coordinates},
                error=elstruct.Error.OPT_NOCONV,
                error_kwargs={'opt_options': [
                    elstruct.option.specify(
                        elstruct.Option.Opt.MAXITER_, 2)
                ]},
            )
            print(vals)

            # check that the frozen coordinates didn't change
            zma = vals[1]
            val_dct = automol.zmatrix.values(zma)
            frozen_values = tuple(map(val_dct.__getitem__, frozen_coordinates))
            print(frozen_values)
            assert numpy.allclose(frozen_values, ref_frozen_values)


def test__run__robust():
    """ test elstruct.run.robust
    """
    input_writer = elstruct.writer.optimization
    method = 'hf'
    basis = 'sto-3g'
    geom = ((('O', (None, None, None), (None, None, None)),
             ('H', (0, None, None), ('R1', None, None)),
             ('H', (0, 1, None), ('R2', 'A2', None))),
            {'R1': 1.83114, 'R2': 1.83115, 'A2': 1.81475845})
    mult = 1
    charge = 0
    orb_restricted = True
    kwargs = {'comment': '<testing comment line>',
              'scf_options': (
                  elstruct.option.specify(elstruct.Option.Scf.DIIS_, True),
                  elstruct.option.specify(elstruct.Option.Scf.MAXITER_, 15),),
              'opt_options': (
                  elstruct.option.specify(elstruct.Option.Scf.MAXITER_, 10),)}
    errors = [
        elstruct.Error.SCF_NOCONV,
        elstruct.Error.OPT_NOCONV,
    ]
    options_mat = [
        [{'scf_options': (elstruct.Option.Scf.Guess.CORE,)},
         {'scf_options': (elstruct.Option.Scf.Guess.HUCKEL,)},
         {'scf_options': (
             elstruct.option.specify(elstruct.Option.Scf.DIIS_, True),
             elstruct.Option.Scf.Guess.HUCKEL,)}],
        [{'opt_options': (elstruct.Option.Opt.Coord.CARTESIAN,)},
         {'opt_options': (elstruct.Option.Opt.Coord.ZMATRIX,)},
         {'opt_options': (elstruct.Option.Opt.Coord.REDUNDANT,)}]
    ]

    for prog in elstruct.writer.optimization_programs():
        if prog in SCRIPT_DCT:
            script_str = SCRIPT_DCT[prog]
            run_dir = tempfile.mkdtemp()
            print(run_dir)
            _, out_str = elstruct.run.robust(
                script_str, run_dir, input_writer,
                prog, method, basis, geom, mult, charge, orb_restricted,
                errors=errors, options_mat=options_mat, **kwargs
            )

            assert elstruct.reader.has_normal_exit_message(prog, out_str)

            ene = elstruct.reader.energy(prog, method, orb_restricted, out_str)
            zma = elstruct.reader.opt_zmatrix(prog, out_str)
            print(run_dir)
            print(ene)
            print(zma)


def _test_pipeline(script_str, prog, method, writer, readers,
                   args, kwargs, error=None, error_kwargs=None):
    read_vals = []
    print()
    print(prog, method, writer.__name__)
    # for programs with no run test, at lest make sure we can generate
    # an input file
    _ = writer(prog, method, *args, **kwargs)
    if script_str is not None:
        script_str = SCRIPT_DCT[prog]
        run_dir = tempfile.mkdtemp()
        print(run_dir)
        _, out_str = elstruct.run.direct(
            script_str, run_dir, writer,
            prog, method, *args, **kwargs
        )

        assert elstruct.reader.has_normal_exit_message(prog, out_str)

        for reader in readers:
            print(reader.__name__)
            val = reader(out_str)
            read_vals.append(val)

        if error is not None:
            assert not elstruct.reader.has_error_message(prog, error,
                                                         out_str)

            run_dir = tempfile.mkdtemp()
            err_kwargs = kwargs.copy()
            err_kwargs.update(error_kwargs)
            print(run_dir, '(error run)')
            with pytest.warns(UserWarning):
                _, err_out_str = elstruct.run.direct(
                    script_str, run_dir, writer,
                    prog, method, *args, **err_kwargs
                )

            assert not elstruct.reader.has_normal_exit_message(
                prog, err_out_str)
            assert elstruct.reader.has_error_message(prog, error,
                                                     err_out_str)
    return read_vals


if __name__ == '__main__':
    # test__energy()
    # test__gradient()
    # test__hessian()
    # test__optimization()
    test__run__robust()
