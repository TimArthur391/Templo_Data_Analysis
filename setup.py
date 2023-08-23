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
    install_requires=[
        'numpy>=1.23.3',
        'opencv-python>=4.7.0.72',
        'pandas>=1.5.0',
        'Pillow>=9.2.0'
    ],
    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

    ],
    python_requires='=3.9',
)