""" Install autorun
"""
from distutils.core import setup


setup(name="autorun",
      version="0.1.0",
      packages=["autorun",
                "autorun.tests",
                "autorun.tests.data"],
               # "autorun.aux"])#,
               # "autorun.tests"])
      package_data={
          'autorun': ['autorun/tests/data/*'])
