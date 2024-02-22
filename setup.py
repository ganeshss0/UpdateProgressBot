'''Importing typing and setuptools'''
from typing import List

from setuptools import find_packages, setup


HYPEN_E_DOT = '-e .'

def get_requirements(file_path:str)->List[str]:
    '''Return the list of required library.'''

    with open(file_path, encoding='utf-8') as file:
        requirements = file.readlines()

    return [require.strip() for require in requirements if not HYPEN_E_DOT in require]


PROJECT_NAME = 'Update Progress Bot'
VERSION = '0.1.0'
AUTHOR='Ganesh'
AUTHOR_EMAIL = 'swami.ganesh@proton.me'
DESCRIPTION = 'Update Progress Bot is a telegram bot that tracks and shows statistics regarding cigarette, NoFap etc consumptions.'
LICENCE = 'GNU'
REQUIREMENTS_FILE = 'requirements.txt'


setup(
    name=PROJECT_NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENCE,
    install_requires=get_requirements(REQUIREMENTS_FILE),
    packages=find_packages()
)
