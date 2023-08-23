from setuptools import find_packages
from setuptools import setup

setup(
    name='Templo External Moments',
    version='1.0.0',
    description='taking the video and force plate data from Contemplas Templo, and some user input, calculate external joint moments',
    author='Tim Arthur',
    author_email='arthurt1995@googlemail.com',
    url='https://github.com/TimArthur391/Templo_Data_Analysis',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'Templo-External-Moments = app'
        ]
    },
    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

    ],
    python_requires='=3.9',
)