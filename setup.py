from setuptools import setup
import sys

setup(
    name='typetype',
    version='1.0.0',
    author='Ahmet Ozer',
    description='A command line typing game',
    packages=['typetype'],
    entry_points={
        'console_scripts': [
            'typetype=game.ahmetsgame:callmain'
        ]
    },
    install_requires=[
] + (['windows-curses'] if sys.platform == 'win32' else [])
)