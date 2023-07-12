#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

clear
rm -rf html

pdoc3 --template-dir scripts/pdoc3Templates --force --html --output-dir docs pyumldiagrams/
