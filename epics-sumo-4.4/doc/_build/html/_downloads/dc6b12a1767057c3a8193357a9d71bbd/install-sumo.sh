#!/bin/bash
 
# Create and activate python virtual environment:
python3 -m venv venv
source ./venv/bin/activate

# Install sumo with "pip":
pip3 install epics-sumo

# Create sumo build and database directory.
# This is described here:
#   https://epics-sumo.sourceforge.io/migration-examples.html#set-up-the-sumo-directory
mkdir sumo && cd sumo
SUMODIR=$(pwd)
mkdir scan database build
cd ..

# Create sumo configuration file:
sumo config make sumo.config --#opt-preload configure/MODULES.HOST --#opt-preload configure/MODULES --builddir $SUMODIR/build --dbdir $SUMODIR/database --scandb $SUMODIR/database/SCAN.DB

# Move sumo configuration file to sumo library directory:
mv sumo.config $(python3 -c 'import sumolib;from os.path import *; print(dirname(sumolib.__file__))')

