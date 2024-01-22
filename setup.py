from setuptools import find_packages,setup
from typing import List #No afecta a la ejecución del código pero ayuda con la caridad


HYPEN_E_DOT = '-e .'
#We create a function to import the packages because manually typing them is infeasible in serious projects
def get_requierements(file_path:str)->List[str]:
    '''
    this funcion will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        # "with" avoids having to call "close", closes at the end of the actions
        requirements=file_obj.readlines()
        requirements= [req.replace("\n", " ") for req in requirements] #we avoid the line breaks
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
name='MLProject',
version='0.0.1',
author='Aleph',
packages=find_packages(),
install_requires=get_requierements('requirements.txt')

)