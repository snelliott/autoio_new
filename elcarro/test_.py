""" test elcarro
"""
import tempfile
import elcarro
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
                prog, method, basis, geom, mult, charge,
                orb_restricted=orb_restricted,
                frozen_coordinates=frozen_coordinates,
                job_options=[
                    elstruct.option.specify(elstruct.Option.Opt.MAXITER_, 4)],
            )


if __name__ == '__main__':
    test__feedback_optimization()
