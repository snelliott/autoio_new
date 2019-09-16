""" mrcc 2018 output reading module """
from elstruct.reader._mrcc2018.energ import energy
from elstruct.reader._mrcc2018.surface import gradient
from elstruct.reader._mrcc2018.prop import dipole_moment
from elstruct.reader._mrcc2018.status import has_normal_exit_message
from elstruct.reader._mrcc2018.status import error_list
from elstruct.reader._mrcc2018.status import has_error_message
from elstruct.reader._mrcc2018.version import name
from elstruct.reader._mrcc2018.version import number


__all__ = [
    'energy',
    'gradient',
    'dipole_moment',
    'has_normal_exit_message',
    'error_list',
    'has_error_message',
    'name',
    'number'
]
