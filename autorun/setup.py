""" Install autorun
"""
from distutils.core import setup


setup(name="autorun",
      version="0.1.0",
      packages=["autorun"],
      package_dir={
        'autorun': 'autorun'},
      package_data={
          'autorun': ['tests/data/*',
                      'aux/*']})
