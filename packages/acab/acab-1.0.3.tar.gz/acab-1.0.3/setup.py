import setuptools
from setuptools import setup, find_packages

setup(
    name='acab',
    version='1.0.3',
    description='Alignments Comparing and Benchmarking (ACAB): инструмент для сравнения множественных выравниваний',
    author='pirat',
    author_email='piratvanek@gmail.com',
    packages=find_packages(),
    install_requires=[],  
    entry_points={
        'console_scripts': [
            'acab = acab.acab:cli_entry'
        ]
    },
    python_requires='>=3.6',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)