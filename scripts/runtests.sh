#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    epxort areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot


python3 -m tests.TestAll "$*"
status=$?

while getopts c option
    do
        case "${option}"
        in
        c) ./scripts/cleanup.sh;;
        p) echo;;
    esac
done


echo "Exit with status: ${status}"
exit ${status}

