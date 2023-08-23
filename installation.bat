@echo off
conda create --name Templo-External-Moments python=3.9
conda activate Templo-External-Moments

python -m pip install -r
python setup.py install