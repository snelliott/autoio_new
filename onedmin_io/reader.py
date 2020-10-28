"""
reads info
"""

import autoparse.pattern as app
import autoparse.find as apf


def lennard_jones(output_string):
    """ reads the lennard jones params from the output
    """

    print('output_string\n', output_string)

    sigma_ptt = (app.SPACES + app.INTEGER + app.SPACES +
                 app.capturing(app.FLOAT) + app.SPACES +
                 app.FLOAT)
    epsilon_ptt = (app.SPACES + app.INTEGER + app.SPACES +
                   app.FLOAT + app.SPACES +
                   app.capturing(app.FLOAT))

    sigmas = apf.all_captures(sigma_ptt, output_string)
    epsilons = apf.all_captures(epsilon_ptt, output_string)
    if sigmas is not None:
        sigmas = [float(val) for val in sigmas]
    if epsilons is not None:
        epsilons = [float(val) for val in epsilons]
    
    print('sigs', sigmas)
    print('eps', epsilons)

    return sigmas, epsilons


def program_version(output_string):
    """ Read the version
    """

    pattern = (
        'OneDMin' + app.SPACES +
        'version' + app.SPACES +
        app.capturing(app.FLOAT)
    )
    capture = apf.last_capture(pattern, output_string)

    return capture
