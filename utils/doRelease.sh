#!/bin/bash


function pause(){
   read -p "$*"
}

echo Start Setup
BASEDIR=$(dirname "${0}")/../


echo "Base Dir :$BASEDIR"
pushd "$BASEDIR" > /dev/null

sudo -H pip install -U .

pushd doc > /dev/null
chmod +711 generate.py
./generate.py
popd > /dev/null

rm dist/*
python setup.py sdist
pause Press any key to continue or Crlt-C to stop
echo Start Upload

twine upload dist/*
echo Upload Finished
