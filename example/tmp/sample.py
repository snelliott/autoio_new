""" elstruct direct run
"""
import tempfile
import numpy
import elstruct
import automol

PROG = 'psi4'
SCRIPT_STR = ("#!/usr/bin/env bash\n"
              "psi4 -i run.inp -o run.out")

# PROG = 'g09'
# SCRIPT_STR = ("#!/usr/bin/env bash\n"
#               "g09 run.inp run.out >> stdout.log &> stderr.log")

METHOD = 'hf'
BASIS = '6-31g'
GEO = automol.geom.from_xyz_string(open('geom.xyz').read())
# ZMA = automol.geom.zmatrix(GEO)

# 3. frequencies
RUN_DIR = tempfile.mkdtemp()
print('hessian:')
print(RUN_DIR)

INP_STR, OUT_STR = elstruct.run.direct(
    # required arguments
    input_writer=elstruct.writer.hessian,
    script_str=SCRIPT_STR,
    run_dir=RUN_DIR,
    geom=GEO,
    charge=0,
    mult=1,
    method=METHOD,
    basis=BASIS,
    prog=PROG,
)

HESS = elstruct.reader.hessian(PROG, OUT_STR)
FREQS = elstruct.util.harmonic_frequencies(GEO, HESS, project=True)
print('frequencies:')
print(FREQS)

NORM_COOS = elstruct.util.normal_coordinates(GEO, HESS, project=True)
SYMS = automol.geom.symbols(GEO)
NATMS = len(SYMS)
XYZS = automol.geom.coordinates(GEO, angstrom=True)
MODE_STR = ''
for freq, norm_coo in zip(FREQS, NORM_COOS.T):
    disp_xyzs = numpy.reshape(norm_coo, (-1, 3))
    xyz_str = '{:d}\n{:>10.2f}\n'.format(NATMS, freq)
    for sym, xyz, disp_xyz in zip(SYMS, XYZS, disp_xyzs):
        xyz_str += (
            sym +
            (3 * '{:10.5f}').format(*xyz) +
            (3 * '{:10.5f}').format(*disp_xyz) +
            '\n'
        )
    MODE_STR += '{}\n'.format(xyz_str)

with open('modes.xyz', 'w') as fle:
    fle.write(MODE_STR)
