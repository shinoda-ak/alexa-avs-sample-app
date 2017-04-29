#!/bin/bash
sudo apt-get install scons swig python-dev
sudo pip install tendo
cd rpi_ws281x-master
sudo scons
cd python
sudo python setup.py install