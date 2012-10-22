from setuptools import setup, find_packages

setup(name='pynfact',
      packages=['pynfact'],
      version='0.1',
      author='Alberte Romero',
      author_email='alberteromero+code@gmail.com',
      description='Blog-oriented static web generator',
      long_description=open('README').read(),
      keywords = ['blog', 'static', 'web', 'generator'],
      license='BSD 3-Clause',
      py_modules=find_packages(),
      scripts = ['bin/run-pynfact'],
      entry_points = { 'console_scripts': [ 'main = pynfact.cli:main' ] } )

