#!/usr/bin/env bash
#
#  Requires brew install of poppler see: https://github.com/jalan/pdftotext
#
function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}
function checkStatus {

    status=$1
    procName=$2

    if [ ${status} -ne 0 ]
    then
        echo "checkStatus ${procName} -- ${status}"
        exit ${status}
    fi
}

function checkDepInstalled {

  pdftotext -v  > /dev/null 2>&1
  status=$?
  checkStatus ${status} "pdftotext is not installed"
}

changeToProjectRoot

checkDepInstalled

if [ "$#" -ne 2 ]; then
    echo "You must enter exactly 2 command line arguments"
    echo "standardFile generatedFile"
fi

standardFile=${1}
generatedFile=${2}

clear
echo "Standard File:  ${standardFile}"
echo "Generated File: ${generatedFile}"

pdftotext ${standardFile}  standard.txt
pdftotext ${generatedFile} generated.txt

diff standard.txt generated.txt
status=$?

rm -rf standard.txt generated.txt
exit ${status}
