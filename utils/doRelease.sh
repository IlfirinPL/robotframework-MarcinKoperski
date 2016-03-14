#!/bin/bash


function pause(){
   read -p "$*"
}

echo Start Setup
BASEDIR=$(dirname "${0}")/../


echo "Base Dir :$BASEDIR"
pushd "$BASEDIR" > /dev/null

sudo -H pip install -U .

pushd $BASEDIR/doc > /dev/null
chmod +711 generate.py
./generate.py
popd > /dev/null

python setup.py sdist
echo Start Upload
pause Press any key to continue or Crlt-C to stop

twine upload dist/*
echo Upload Finished