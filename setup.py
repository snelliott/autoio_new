""" install elstruct
"""
from distutils.core import setup


setup(name="elstruct",
      version="0.2.2",
      packages=["elstruct",
                "elstruct.writer",
                "elstruct.reader",
                "elstruct.writer._psi4",
                "elstruct.reader._psi4",
                "elstruct.writer._g09",
                "elstruct.reader._g09",
                "elstruct.run"],
      package_dir={'elstruct': 'elstruct'},
      package_data={'elstruct': [
          'writer/_psi4/templates/*.mako',
          'writer/_g09/templates/*.mako',
      ]})
