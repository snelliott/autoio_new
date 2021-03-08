""" Runner
"""



def direct(script_str, run_dir,
           geo_str, hess_str, 
           zma=None):
    """ Generates an input file for a ThermP job runs it directly.
    """
    
    input_str = intder_io.writer.input(geo, zma=zma)

    aux_dct = {'file15': hess_str}
    input_name = 'intder.inp'
    output_name = 'intder.out'
    output_str = from_input_string(
        script_str, run_dir, input_str,
        aux_dct=aux_dct,
        output_name=output_name)

    return input_str, output_str
