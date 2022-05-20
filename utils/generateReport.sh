#!/bin/bash

python -m pip install -U .

pushd atest/acceptance && python -m robot.run  -b debug.log -e TODO -e WIN -r none -l none .
popd

python -m robot.libdoc TestToolsMK doc/TestToolsMK.html
