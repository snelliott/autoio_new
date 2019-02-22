""" test elstruct writer/run/reader pipelines
"""
import elstruct


SCRIPT_STR_DCT = {
    'psi4': "#!/usr/bin/env bash\npsi4"
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
            inp_str = elstruct.writer.energy(
                prog=prog, method=method, basis=basis, geom=geom,
                mult=mult, charge=charge, scf_options=''
            )

            # if we have a run script, try running it
            if prog in SCRIPT_STR_DCT:
                out_str, _ = elstruct.run(SCRIPT_STR_DCT[prog], inp_str)
                ene = elstruct.reader.energy(prog, method, out_str)
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
            inp_str = elstruct.writer.optimization(
                prog=prog, method=method, basis=basis, geom=geom,
                mult=mult, scf_options='',
                zmat_var_dct=zmat_var_dct
            )

            # if we have a run script, try running it
            if prog in SCRIPT_STR_DCT:
                out_str, _ = elstruct.run(SCRIPT_STR_DCT[prog], inp_str)

                ene = elstruct.reader.energy(prog, method, out_str)

                zmat_geom, zmat_var_dct = (
                    elstruct.reader.optimized_zmatrix_geometry(prog, out_str))

                cart_geom = elstruct.reader.optimized_cartesian_geometry(
                    prog, out_str)

                print(ene)
                print(zmat_geom)
                print(zmat_var_dct)
                print(cart_geom)


if __name__ == '__main__':
    # test__energy()
    test__optimization()
