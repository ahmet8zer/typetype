from setuptools import setup, find_packages
import sys

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='typetype',
    version='1.0.8',
    author='Ahmet Ozer',
    url="https://github.com/ahmet8zer/typetype",
    description='A command line typing game',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'typetype=typetype.ahmetsgame:callmain'
        ]
    },
    install_requires=[
] + (['windows-curses','keyboard'] if sys.platform == 'win32' else ['keyboard'])
)