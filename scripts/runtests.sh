#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot


python -m tests.TestAll
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

