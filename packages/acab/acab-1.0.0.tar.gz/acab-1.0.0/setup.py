import setuptools
from setuptools import setup, find_packages

setup(
    name='acab',
    version='1.0.0',
    description='Alignment Comparison And Blocks (ACAB): инструмент для сравнения множественных выравниваний',
    author='Твоё Имя',
    author_email='youremail@example.com',
    packages=find_packages(),
    install_requires=[],  # если нужны сторонние библиотеки, добавь их сюда
    entry_points={
        'console_scripts': [
            'acab = acab.acab:cli_entry'
        ]
    },
    python_requires='>=3.6',
    license='MIT',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourname/acab',  # укажи свой репозиторий
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)