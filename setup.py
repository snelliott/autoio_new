""" install elstruct
"""
from distutils.core import setup


setup(name="elstruct",
      version="0.1.0",
      packages=["elstruct",
                "elstruct.writer",
                "elstruct.reader",
                "elstruct.writer._psi4",
                "elstruct.reader._psi4",
                "elstruct.writer._cfour2",
                "elstruct.reader._cfour2",
                "elstruct.writer._gaussian09",
                "elstruct.reader._gaussian09",
                "elstruct.writer._gaussian16",
                "elstruct.reader._gaussian16",
                "elstruct.writer._mrcc2018",
                "elstruct.reader._mrcc2018",
                "elstruct.writer._nwchem6",
                "elstruct.reader._nwchem6",
                "elstruct.writer._orca4",
                "elstruct.reader._orca4",
                "elstruct.writer._molpro2015",
                "elstruct.reader._molpro2015"],
      package_dir={'elstruct': 'elstruct'},
      package_data={'elstruct': [
          'writer/_psi4/templates/*.mako',
          'writer/_cfour2/templates/*.mako',
          'writer/_gaussian09/templates/*.mako',
          'writer/_gaussian16/templates/*.mako',
          'writer/_mrcc2018/templates/*.mako',
          'writer/_nwchem6/templates/*.mako',
          'writer/_orca4/templates/*.mako',
          'writer/_molpro2015/templates/*.mako',
      ]})
