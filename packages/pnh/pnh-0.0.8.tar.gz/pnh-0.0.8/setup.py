
from setuptools import setup

setup(name='pnh',
      version='0.0.8',
      description='pnh',
      packages=['pnh','pnh.utils'],
      package_dir={
      'pnh':'.','pnh.utils':'utils'},
     )