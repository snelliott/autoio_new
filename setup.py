""" install elstruct
"""
from distutils.core import setup


setup(name="elstruct",
      version="0.1.0",
      packages=["elstruct",
                "elstruct.write",
                "elstruct.read",
                "elstruct.write._psi4"],
      package_dir={'elstruct': 'elstruct'},
      package_data={'elstruct': [
          'write/_psi4/templates/*.mako',
      ]})
