#!/bin/bash


function pause(){
   read -p "$*"
}

echo Start Setup
BASEDIR=$(dirname "${0}")/../

pushd "$BASEDIR"
pwd
./utils/generateReport.sh

rm ${BASEDIR}/dist/*
python setup.py sdist
pause Press any key to continue or Crlt-C to stop
echo Start Upload

twine upload dist/*
echo Upload Finished
