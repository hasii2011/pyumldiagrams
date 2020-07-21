#!/bin/bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

clear

rm -rf dist build
rm -rf PyGMLParser.egg-info
python3 setup.py sdist bdist_wheel

# Check package
twine check dist/*
