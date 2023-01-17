from setuptools import find_packages, setup
from typing import List

REQUIREMENTS_FILE_NAME = 'requirements.txt'
HYPHEN_E_DOT = '-e .'

def get_requirements()->List[str]:
    """
    This functions returns the list of packages
    names.
    """

    with open(REQUIREMENTS_FILE_NAME) as requirements_file:
        requirements_list = requirements_file.readlines()
    requirements_list = [requirements_name.replace('\n',' ') for requirements_name in requirements_list]

    if HYPHEN_E_DOT in requirements_list:
        requirements_list.remove(HYPHEN_E_DOT)


setup(
    name = 'backorder',
    version = "0.0.1",
    author = 'Shabarish',
    author_email = 'medashabari@gmail.com', 
    packages = find_packages(),
    install_requires = get_requirements()

)