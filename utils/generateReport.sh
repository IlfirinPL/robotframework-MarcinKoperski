#!/bin/bash

python -m pip install -U .

python -m robot.libdoc TestToolsMK list

python -m robot.libdoc TestToolsMK doc/TestToolsMK.html
