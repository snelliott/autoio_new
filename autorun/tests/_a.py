import mess_io

axes = ((0, 1), (1, 5))
groups = (((2, 3, 4), (5, 6, 7, 8)), ((0, 2, 3, 4, 6, 7), (8,)))
symms = (3, 1)
pots = (
        {0: 0.0, 1: 1.7375, 2: 3.5965, 3: 1.687},
        {0: 0.0, 1: 0.7696, 2: 1.6458, 3: 0.9834, 4: 0.1201, 5: 0.7322,
         6: 1.6143, 7: 1.0721, 8: 0.3468, 9: 0.8933, 10: 1.5189, 11:0.7401}
)


strs = []
for x, y, a, b in zip(axes, groups, symms, pots):
    strs.append(
       mess_io.writer.rotor_hindered(
        y[0], x, a, b,
        hmin=None, hmax=None,
        lvl_ene_max=None,
        therm_pow_max=None,
        geo=None,
        rotor_id=''))
astr = '\n'.join(strs)

print(astr)

