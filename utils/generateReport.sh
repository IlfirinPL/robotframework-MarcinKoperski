#!/bin/bash

echo Start Setup
BASEDIR=$(dirname "${0}")/../


echo "Base Dir :$BASEDIR"
pushd "$BASEDIR" > /dev/null

sudo -H pip install -U .

pushd doc > /dev/null
chmod +711 generate.py
./generate.py
