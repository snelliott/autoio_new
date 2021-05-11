"""
  Read the the ThermP output
"""

import autoparse.pattern as app
import autoparse.find as apf


def hf298k(output_str):
    """ Read the Heat of Formation at 298 K.

        :param output_str: string for output file of ThermP
        :type output_str: str
        :rtype: tuple(float)
    """

    ptt = (
        'h298' +
        app.SPACES +
        'final' +
        app.SPACES +
        app.capturing(app.FLOAT)
    )

    caps = apf.all_captures(ptt, output_str)

    if caps:
        hfs = tuple(float(val) for val in caps)
        hfs = hfs[0]
    else:
        hfs = None

    return hfs
