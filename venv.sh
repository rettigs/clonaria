#!/bin/bash

# Script for setting up virtualenv.  Can be run from any directory in the repo.

# Run in correct dir
DIR=`dirname $0`/
cd $DIR

# Enable venv
if [ ! -d .virtualenvs/clonaria ]; then
    virtualenv .virtualenvs/clonaria
fi

source .virtualenvs/clonaria/bin/activate

# Update packages
pip install -r requirements.txt
