""" test elstruct.run.optsmat
"""
import elstruct.run.optsmat as optsmat

KWARGS_DCT = {'comment': '<testing comment line>',
              'scf_options': ('set scf diis false', 'set scf maxiter 15'),
              'opt_options': ('set geom_maxiter 10',)}
OPTS_MAT = [
    [{'scf_options': ('set scf guess huckel',)},
     {'scf_options': ('set scf guess gwh',)},
     {'scf_options': ('set scf diis true', 'set scf guess sad',)}],
    [{'opt_options': ('set opt_coordinates cartesian',)},
     {'opt_options': ('set opt_coordinates internal',)}]
]


def test__optsmat():
    """ test optsmat.current_kwargs
    """
    assert optsmat.updated_kwargs(KWARGS_DCT, OPTS_MAT) == {
        'comment': '<testing comment line>',
        'scf_options': ('set scf diis false', 'set scf maxiter 15',
                        'set scf guess huckel'),
        'opt_options': ('set geom_maxiter 10', 'set opt_coordinates cartesian')
    }

    opts_mat = optsmat.advance(0, OPTS_MAT)
    assert optsmat.updated_kwargs(KWARGS_DCT, opts_mat) == {
        'comment': '<testing comment line>',
        'scf_options': ('set scf diis false', 'set scf maxiter 15',
                        'set scf guess gwh'),
        'opt_options': ('set geom_maxiter 10', 'set opt_coordinates cartesian')
    }

    opts_mat = optsmat.advance(1, opts_mat)
    assert optsmat.updated_kwargs(KWARGS_DCT, opts_mat) == {
        'comment': '<testing comment line>',
        'scf_options': ('set scf diis false', 'set scf maxiter 15',
                        'set scf guess gwh'),
        'opt_options': ('set geom_maxiter 10', 'set opt_coordinates internal')
    }

    assert not optsmat.is_exhausted(opts_mat)
    opts_mat = optsmat.advance(1, opts_mat)
    assert optsmat.is_exhausted(opts_mat)


if __name__ == '__main__':
    test__optsmat()
