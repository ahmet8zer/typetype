from setuptools import setup, find_packages
import sys

setup(
    name='typetype',
    version='1.0.6',
    author='Ahmet Ozer',
    url="https://github.com/ahmet8zer/typetype",
    description='A command line typing game',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'typetype=typetype.ahmetsgame:callmain'
        ]
    },
    install_requires=[
] + (['windows-curses'] if sys.platform == 'win32' else [])
)