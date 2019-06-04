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
    'g09': None,
    'molpro': None,
}

# SCRIPT_DCT = {
#     'psi4': "#!/usr/bin/env bash\n"
#             "psi4 -i run.inp -o run.out >> stdout.log &> stderr.log",
#     'g09': "#!/usr/bin/env bash\n"
#            "g09 run.inp run.out >> stdout.log &> stderr.log",
#     'molpro': "#!/usr/bin/env bash\n"
#               "molpro run.inp -o run.out >> stdout.log &> stderr.log",
# }


def test__energy():
    """ test the energy pipeline
    """
    basis = '6-31g'
    geom = (('O', (0.0, 0.0, -0.110)),
            ('H', (0.0, -1.635, 0.876)),
            ('H', (-0.0, 1.635, 0.876)))
    mult_vals = [1, 2]
    charge_vals = [0, 1]

    for prog in elstruct.writer.programs():
        for method in elstruct.program_methods(prog):
            for mult, charge in zip(mult_vals, charge_vals):
                for orb_restricted in (
                        elstruct.program_method_orbital_restrictions(
                            prog, method, singlet=(mult == 1))):

                    vals = _test_pipeline(
                        script_str=SCRIPT_DCT[prog],
                        writer=elstruct.writer.energy,
                        readers=(
                            elstruct.reader.energy_(prog, method),
                        ),
                        args=(geom, charge, mult, method, basis, prog),
                        kwargs={'orb_restricted': orb_restricted},
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

    for prog in elstruct.writer.gradient_programs():
        methods = list(elstruct.program_nondft_methods(prog))
        dft_methods = list(elstruct.program_dft_methods(prog))
        if dft_methods:
            methods.append(numpy.random.choice(dft_methods))

        for method in methods:
            for mult, charge in zip(mult_vals, charge_vals):
                for orb_restricted in (
                        elstruct.program_method_orbital_restrictions(
                            prog, method, singlet=(mult == 1))):

                    vals = _test_pipeline(
                        script_str=SCRIPT_DCT[prog],
                        writer=elstruct.writer.gradient,
                        readers=(
                            elstruct.reader.energy_(prog, method),
                            elstruct.reader.gradient_(prog),
                        ),
                        args=(geom, charge, mult, method, basis, prog),
                        kwargs={'orb_restricted': orb_restricted},
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

    for prog in elstruct.writer.hessian_programs():
        methods = list(elstruct.program_nondft_methods(prog))
        dft_methods = list(elstruct.program_dft_methods(prog))
        if dft_methods:
            methods.append(numpy.random.choice(dft_methods))

        for method in methods:
            for mult, charge in zip(mult_vals, charge_vals):
                for orb_restricted in (
                        elstruct.program_method_orbital_restrictions(
                            prog, method, singlet=(mult == 1))):

                    vals = _test_pipeline(
                        script_str=SCRIPT_DCT[prog],
                        writer=elstruct.writer.hessian,
                        readers=(
                            elstruct.reader.energy_(prog, method),
                            elstruct.reader.hessian_(prog),
                        ),
                        args=(geom, charge, mult, method, basis, prog),
                        kwargs={'orb_restricted': orb_restricted},
                    )
                    print(vals)


def test__optimization():
    """ test elstruct optimization writes and reads
    """
    basis = 'sto-3g'
    geom = ((('C', (None, None, None), (None, None, None)),
             ('O', (0, None, None), ('R1', None, None)),
             ('H', (0, 1, None), ('R2', 'A2', None)),
             ('H', (0, 1, 2), ('R3', 'A3', 'D3')),
             ('H', (0, 1, 2), ('R4', 'A4', 'D4')),
             ('H', (1, 0, 2), ('R5', 'A5', 'D5'))),
            {'R1': 2.6, 'R2': 2.0, 'A2': 1.9,
             'R3': 2.0, 'A3': 1.9, 'D3': 2.1,
             'R4': 2.0, 'A4': 1.9, 'D4': 4.1,
             'R5': 1.8, 'A5': 1.8, 'D5': 5.2})
    mult = 1
    charge = 0
    orb_restricted = True
    frozen_coordinates = ('R5', 'A5', 'D3')
    ref_frozen_values = (1.8, 1.8, 2.1)
    for prog in elstruct.writer.optimization_programs():
        methods = list(elstruct.program_nondft_methods(prog))
        dft_methods = list(elstruct.program_dft_methods(prog))
        if dft_methods:
            methods.append(numpy.random.choice(dft_methods))

        for method in methods:
            script_str = SCRIPT_DCT[prog]

            vals = _test_pipeline(
                script_str=script_str,
                writer=elstruct.writer.optimization,
                readers=(
                    elstruct.reader.energy_(prog, method),
                    elstruct.reader.opt_geometry_(prog),
                    elstruct.reader.opt_zmatrix_(prog),
                ),
                args=(geom, charge, mult, method, basis, prog),
                kwargs={'orb_restricted': orb_restricted,
                        'frozen_coordinates':  frozen_coordinates},
                error=elstruct.Error.OPT_NOCONV,
                error_kwargs={'job_options': [
                    elstruct.option.specify(
                        elstruct.Option.Opt.MAXITER_, 2)
                ]},
            )
            print(vals)

            if script_str is not None:
                # check that the frozen coordinates didn't change
                zma = vals[-1]
                val_dct = automol.zmatrix.values(zma)
                frozen_values = tuple(
                    map(val_dct.__getitem__, frozen_coordinates))
                assert numpy.allclose(
                    frozen_values, ref_frozen_values, rtol=1e-4)


def _test_pipeline(script_str, writer, readers,
                   args, kwargs, error=None, error_kwargs=None):
    read_vals = []
    print()
    print(args[1:], writer.__name__)
    prog = args[-1]
    # for programs with no run test, at lest make sure we can generate
    # an input file
    _ = writer(*args, **kwargs)
    if script_str is not None:
        script_str = SCRIPT_DCT[prog]
        run_dir = tempfile.mkdtemp()
        print(run_dir)
        _, out_str = elstruct.run.direct(
            writer, script_str, run_dir, *args, **kwargs)

        assert elstruct.reader.has_normal_exit_message(prog, out_str)

        for reader in readers:
            print(reader.__name__)
            val = reader(out_str)
            read_vals.append(val)

        if error is not None:
            run_dir = tempfile.mkdtemp()
            print(run_dir, '(error run)')
            assert not elstruct.reader.has_error_message(prog, error,
                                                         out_str)

            err_kwargs = kwargs.copy()
            err_kwargs.update(error_kwargs)
            with pytest.warns(UserWarning):
                _, err_out_str = elstruct.run.direct(
                    writer, script_str, run_dir, *args, **err_kwargs)

            assert not elstruct.reader.has_normal_exit_message(
                prog, err_out_str)
            assert elstruct.reader.has_error_message(prog, error,
                                                     err_out_str)
    return read_vals


if __name__ == '__main__':
    # test__energy()
    # test__gradient()
    test__hessian()
    # test__optimization()
