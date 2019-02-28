""" test elstruct writer/run/reader pipelines
"""
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
                mult=mult, charge=charge, scf_options=''
            )

            # if we have a run script, try running it
            if prog in SCRIPT_STR_DCT:
                out_str = elstruct.run(SCRIPT_STR_DCT[prog], inp_str)

                assert elstruct.reader.has_normal_exit_message(prog, out_str)

                ene = elstruct.reader.energy(prog, method, out_str)

                print(ene)


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
                mult=mult, charge=charge, scf_options='',
            )

            # if we have a run script, try running it
            if prog in SCRIPT_STR_DCT:
                out_str = elstruct.run(SCRIPT_STR_DCT[prog], inp_str)

                assert elstruct.reader.has_normal_exit_message(prog, out_str)

                ene = elstruct.reader.energy(prog, method, out_str)

                zma = elstruct.reader.optimized_zmatrix(prog, out_str)

                geo = elstruct.reader.optimized_geometry(prog, out_str)

                print(ene)
                print(zma)
                print(geo)


if __name__ == '__main__':
    # test__energy()
    test__optimization()
