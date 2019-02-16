""" input writing CLI
"""
import yaml
import autocom
import automol
from ._write import optimization_programs as _optimization_programs
from ._write import method_list as _method_list
from ._write import basis_list as _basis_list
from ._write import optimization_input_string as _optimization_input_string


def optimization_input_cli(sysargv, calling_pos):
    """ makes the program choice a subcommand """
    autocom.call_subcommand(
        sysargv, calling_pos, subcmd_func_dct={
            prog: optimization_input_program_cli
            for prog in _optimization_programs()
        }
    )


def optimization_input_program_cli(sysargv, calling_pos):
    """ calls the input writer for the chosen program
    """
    prog = sysargv[calling_pos]
    first_arg_pos = calling_pos + 1

    (
        method,
        basis,
        geom_path,
        input_path,
        logger,
    ) = autocom.values_with_logger(
        sysargv, first_arg_pos, arg_lst=[
            autocom.arg.required(
                'method', 'method', vals=_method_list(prog),
                msgs=['electronic structure method'],
            ),
            autocom.arg.required(
                'basis', 'basis', vals=_basis_list(prog),
                msgs=['atomic orbital basis set'],
            ),
            autocom.arg.required(
                'geom', 'geom_file',
                msgs=['.xyz or .zmat file specifying molecular geometry'],
            ),
            autocom.arg.optional(
                'inp', 'input_file', 'I', default='input.dat',
                msgs=['the name of the input file to be written'],
            )
        ]
    )

    logger.info("Reading in the geometry")

    geom_str = open(geom_path).read()
    # interpret the geometry based on the file extension
    if geom_path.endswith('.zmat'):
        geom, zmat_var_dct, comment = automol.zmatrix.from_zmat_string(
            geom_str, with_auxinfo=True)
    elif geom_path.endswith('.xyz'):
        geom, comment = automol.geom.from_dxyz_string(
            geom_str, with_comment_line=True)
        zmat_var_dct = None
    else:
        raise ValueError("Unknown geometry file type: {:s}".format(geom_path))

    logger.info("Parsing the geometry comment line for state information")
    state_dct = yaml.load('{{{:s}}}'.format(comment))
    assert 'mult' in state_dct and 'charge' in state_dct
    charge = state_dct['charge']
    mult = state_dct['mult']

    logger.info("Calling the input file generator")
    input_str = _optimization_input_string(
        prog, method, basis, geom, charge, mult, zmat_var_dct=zmat_var_dct)

    logger.info("Writing the input file")
    with open(input_path, 'w') as input_file:
        input_file.write(input_str)
