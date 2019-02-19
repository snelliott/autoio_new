""" install elstruct
"""
from distutils.core import setup


setup(name="elstruct",
      version="0.1.0",
      packages=["elstruct",
                "elstruct.writer",
                "elstruct.reader",
                "elstruct.writer._psi4",
                "elstruct.reader._psi4"],
      package_dir={'elstruct': 'elstruct'},
      package_data={'elstruct': [
          'writer/_psi4/templates/*.mako',
      ]})
