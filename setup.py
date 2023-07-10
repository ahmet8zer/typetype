from setuptools import setup
import sys

setup(
    name='typetype',
    version='1.0.0',
    author='Ahmet Ozer',
    url="https://github.com/ahmet8zer/typetype",
    description='A command line typing game',
    packages=['typetype'],
    entry_points={
        'console_scripts': [
            'typetype=typetype.ahmetsgame:callmain'
        ]
    },
    install_requires=[
] + (['windows-curses'] if sys.platform == 'win32' else [])
)