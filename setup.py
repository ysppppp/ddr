#!/usr/bin/env/python
from setuptools import setup

setup(name='DRR', 
      version='1.0', 
      description='CompE Stub Library', 
      author='Tejus Gowda, Yipeng Sha',
      author_email='trg279@nyu.edu, ys2664@nyu.edu', 
      url='https://github.com/ysppppp', 
      py_modules=['DRR'], 
      install_requires=['pyserial','spidev', 'pyserial', 'Adafruit_BBIO', 'adafruit-circuitpython-amg88xx', 'adafruit-circuitpython-lsm9ds1', 'adafruit-circuitpython-sgp30'])

 
