from setuptools import setup, find_packages
import sys

setup(
    name='typetype',
    version='1.0.5',
    author='Ahmet Ozer',
    url="https://github.com/ahmet8zer/typetype",
    description='A command line typing game',
    packages=find_packages(),
    data_files=[('typetype/words', ['typetype/words/200words.txt', 'typetype/words/5000words.txt', 'typetype/words/25000words.txt', 'typetype/words/text.txt', 'typetype/words/highscores.txt'])],
    entry_points={
        'console_scripts': [
            'typetype=typetype.ahmetsgame:callmain'
        ]
    },
    install_requires=[
] + (['windows-curses'] if sys.platform == 'win32' else [])
)