"""
  Read the the ThermP output
"""


def hf298k(output_str):
    """ Read the Heat of Formation at 298 K.

        :param output_str: String for output file of ThermP
        :type output_str: str
        :return hf298k: 298 K Heat of Formation [units]
        :rtype: float
    """

    lines = output_str.splitlines()
    line = lines[-1]
    hf_val = float(line.split()[-1])

    return hf_val
