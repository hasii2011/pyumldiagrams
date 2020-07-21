#!/usr/bin/env bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot


python3 -m tests.TestAll $*
status=$?

cd -  > /dev/null 2>&1


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

