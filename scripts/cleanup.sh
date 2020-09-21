#!/usr/bin/env bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot


find . -maxdepth 1 -type f -name '*'.pdf -delete
find . -maxdepth 1 -type f -name '*'.png -delete

rm -rf build dist pyumldiagrams.egg-info -delete
