""" nwchem6 output reading module """
from elstruct.reader._nwchem6.energ import energy
from elstruct.reader._nwchem6.surface import gradient
from elstruct.reader._nwchem6.molecule import opt_geometry
from elstruct.reader._nwchem6.version import name
from elstruct.reader._nwchem6.version import number


__all__ = [
    'energy',
    'gradient',
    'opt_geometry',
    'name',
    'number'
]
