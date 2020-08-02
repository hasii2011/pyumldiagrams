#!/usr/bin/env bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

find . -type d -name PDFDiagramming.egg-info -exec rm -rf {} \; -print
find . -type f -name "*.pdf" -delete
find . -type f -name "*.png" -delete
rm -rf build dist
