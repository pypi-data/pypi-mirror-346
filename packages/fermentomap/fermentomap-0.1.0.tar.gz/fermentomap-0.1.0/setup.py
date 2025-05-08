
from setuptools import setup, find_packages

setup(
    name='fermentomap',
    version='0.1.0',
    description='Fermentation trait detection from microbial genomes',
    author='Your Name',
    author_email='your@email.com',
    packages=find_packages(),
    install_requires=['biopython'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
