#!/usr/bin/env bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

clear
rm -rf html

cd src > /dev/null 2>&1

pdoc3 --force --html --output-dir docs pdfdiagrams/
