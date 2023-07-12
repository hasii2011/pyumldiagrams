#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

rm -fv ./*.pdf
rm -fv ./*.png

rm -rf build dist pyumldiagrams.egg-info -delete
rm -rf build dist
