#!/bin/bash

source ~/Envs/Venv/bin/activate

echo Start Setup
BASEDIR=$(dirname "${0}")/../


echo "Base Dir :$BASEDIR"
pushd "$BASEDIR" > /dev/null

python3 -m pip install -U .

pushd doc > /dev/null
chmod +711 generate.py
python3 ./generate.py
