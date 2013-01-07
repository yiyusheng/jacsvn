#!/bin/bash
srcDir=$1
shift
destDir=$1
shift
username=$1
shift
password=$1
shift
makeInc=$1
shift
until [ $# -eq 0 ]
do
    $makeInc/autoscp.sh $srcDir $destDir $username $password $1 1>/dev/null &
    shift
done