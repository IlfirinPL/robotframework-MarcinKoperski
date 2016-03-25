#!/bin/bash

source ~/Envs/Venv/bin/activate

echo Start Setup
BASEDIR=$(dirname "${0}")/../


echo "Base Dir :$BASEDIR"
pushd "$BASEDIR" > /dev/null

pip install -U .

pushd doc > /dev/null
chmod +711 generate.py
./generate.py
