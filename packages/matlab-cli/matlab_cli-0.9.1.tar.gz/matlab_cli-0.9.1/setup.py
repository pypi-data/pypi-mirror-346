from setuptools import setup, find_packages

setup(
   name='matlab-cli',
   version='0.9.1',
   packages=find_packages(),
   entry_points={
       'console_scripts': [
           'matlab-cli=matlab_cli.__main__:main',
       ],
   },
)



