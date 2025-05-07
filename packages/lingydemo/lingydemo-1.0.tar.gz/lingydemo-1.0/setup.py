from distutils.core import setup
import setuptools

packages = ['lingydemo']
setup(name='lingydemo',
      version='1.0',
      author='lingy',
      packages=packages,
      package_dir={'requests': 'requests'}, )
