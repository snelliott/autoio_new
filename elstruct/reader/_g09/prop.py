""" 
reads properties of the molecule
"""


def dipole_moment_reader(output_string):
    """ gets dipole moment
    """
    
    pattern = (app.series(app.one_of_these(['X=', 'Y=', 'Z=']), 
                          app.SPACE, 
                          app.capturing(app.FLOAT)) +
               app.SPACE + 
               'Total=' +
               app.FLOAT)




