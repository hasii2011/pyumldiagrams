#!/usr/local/bin/bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

find . -type d -name UNKNOWN.egg-info -exec rm -rf {} \; -print
find . -type f -name "*.pdf" -delete
