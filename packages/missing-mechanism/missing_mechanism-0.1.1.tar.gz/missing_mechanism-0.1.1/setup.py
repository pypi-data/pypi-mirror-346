from setuptools import setup, find_packages

setup(
    name='missing_mechanism',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'pandas'
    ],
    author='Rayan Dayyeh',
    description='A package for handling missing data intelligently',
    python_requires='>=3.6'
)
 
