""" command-line interface for elstruct
"""
import autocom
from . import write as _write


def main(sysargv):
    """ main function """
    autocom.call_subcommand(
        sysargv, calling_pos=0, subcmd_func_dct={
            'write': write,
            'read': read,
        }
    )


def write(sysargv, calling_pos):
    """ the write subcommand """
    autocom.call_subcommand(
        sysargv, calling_pos, subcmd_func_dct={
            'opt': _write.optimization_input_cli,
        }
    )


def read(sysargv, calling_pos):
    """ the read subcommand """
    raise NotImplementedError
