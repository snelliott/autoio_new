""" test elcarro
"""
import tempfile
import elstruct
import elcarro
import elcarro.optsmat as optsmat

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


def test__feedback_optimization():
    """ test elcarro.feedback_optimization
    """
    method = 'hf'
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
    # ref_frozen_values = (1.8, 1.8, 2.1)

    for prog in elstruct.writer.optimization_programs():
        script_str = SCRIPT_DCT[prog]
        if script_str is not None:
            run_dir = tempfile.mkdtemp()
            print(prog, run_dir)
            elcarro.feedback_optimization(
                script_str, run_dir,
                geom, charge, mult, method, basis, prog,
                orb_restricted=orb_restricted,
                frozen_coordinates=frozen_coordinates,
                job_options=[
                    elstruct.option.specify(elstruct.Option.Opt.MAXITER_, 4)],
            )


def test__optsmat():
    """ test optsmat.current_kwargs
    """
    kwargs_dct = {'comment': '<testing comment line>',
                  'scf_options': ('set scf diis false', 'set scf maxiter 15'),
                  'job_options': ('set geom_maxiter 10',)}
    ref_opts_mat = [
        [{'scf_options': ('set scf guess huckel',)},
         {'scf_options': ('set scf guess gwh',)},
         {'scf_options': ('set scf diis true', 'set scf guess sad',)}],
        [{'job_options': ('set opt_coordinates cartesian',)},
         {'job_options': ('set opt_coordinates internal',)}]
    ]

    assert optsmat.updated_kwargs(kwargs_dct, ref_opts_mat) == {
        'comment': '<testing comment line>',
        'scf_options': ('set scf diis false', 'set scf maxiter 15',
                        'set scf guess huckel'),
        'job_options': ('set geom_maxiter 10', 'set opt_coordinates cartesian')
    }

    opts_mat = optsmat.advance(0, ref_opts_mat)
    assert optsmat.updated_kwargs(kwargs_dct, opts_mat) == {
        'comment': '<testing comment line>',
        'scf_options': ('set scf diis false', 'set scf maxiter 15',
                        'set scf guess gwh'),
        'job_options': ('set geom_maxiter 10', 'set opt_coordinates cartesian')
    }

    opts_mat = optsmat.advance(1, opts_mat)
    assert optsmat.updated_kwargs(kwargs_dct, opts_mat) == {
        'comment': '<testing comment line>',
        'scf_options': ('set scf diis false', 'set scf maxiter 15',
                        'set scf guess gwh'),
        'job_options': ('set geom_maxiter 10', 'set opt_coordinates internal')
    }

    assert not optsmat.is_exhausted(opts_mat)
    opts_mat = optsmat.advance(1, opts_mat)
    assert optsmat.is_exhausted(opts_mat)


def test__robust_run():
    """ test elcarro.robust_run
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
    kwargs = {'comment': '<testing comment line>',
              'scf_options': (
                  elstruct.option.specify(elstruct.Option.Scf.DIIS_, False),
                  elstruct.option.specify(elstruct.Option.Scf.MAXITER_, 10),),
              'job_options': (
                  elstruct.option.specify(elstruct.Option.Opt.MAXITER_, 2),)}
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
        [{'job_options': (elstruct.Option.Opt.Coord.ZMATRIX,)},
         {'job_options': (
             elstruct.option.specify(elstruct.Option.Opt.MAXITER_, 10),
             elstruct.Option.Opt.Coord.ZMATRIX,)}],
    ]

    for prog in elstruct.writer.optimization_programs():
        print()
        print(prog, method)
        if prog in SCRIPT_DCT:
            script_str = SCRIPT_DCT[prog]
            if script_str is not None:
                run_dir = tempfile.mkdtemp()
                print(run_dir)
                _, out_str = elcarro.robust_run(
                    input_writer, script_str, run_dir,
                    geom, charge, mult, method, basis, prog,
                    errors=errors, options_mat=options_mat, **kwargs
                )

                assert elstruct.reader.has_normal_exit_message(prog, out_str)

                ene = elstruct.reader.energy(prog, method, out_str)
                zma = elstruct.reader.opt_zmatrix(prog, out_str)
                print(ene)
                print(zma)


if __name__ == '__main__':
    # test__feedback_optimization()
    test__robust_run()
